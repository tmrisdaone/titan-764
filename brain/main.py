#!/usr/bin/env python3
"""
TITAN-7 ARM64 Brain Controller
Runs on Termux. Reads phone sensors, queries local Ollama, and sends motor commands to ESP32.
"""

import subprocess
import json
import requests
import serial
import time
import math

# --- CONFIG ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2:0.5b"  # or llama3.2:1b
SERIAL_PORT = "/dev/ttyUSB0"  # Change to /dev/ttyACM0 or Bluetooth RFCOMM as needed
BAUD_RATE = 115200

class TermuxSensor:
    @staticmethod
    def get_imu():
        """Reads gyroscope and accelerometer via termux-sensor CLI."""
        try:
            # Requesting 1 reading, 100ms delay
            cmd = ['termux-sensor', '-s', 'Gyroscope,Accelerometer', '-n', '1', '-d', '100']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1)
            data = json.loads(result.stdout)
            
            # Extract values (structure varies slightly by device, this is standard)
            gyro = data['sensors'].get('Gyroscope', {}).get('values', [0,0,0])
            accel = data['sensors'].get('Accelerometer', {}).get('values', [0,0,0])
            
            return {
                "pitch_rate": gyro[0],
                "roll_rate": gyro[1],
                "yaw_rate": gyro[2],
                "x_accel": accel[0],
                "y_accel": accel[1],
                "z_accel": accel[2]
            }
        except Exception as e:
            return {"error": str(e)}

class LLMCortex:
    @staticmethod
    def get_action_intent(sensor_data, current_state="standing"):
        """Queries 0.8B model for high-level gait decision based on sensor drift."""
        prompt = f"""
        Robot is {current_state}. Sensor data: {json.dumps(sensor_data)}.
        If z_accel < 8.0, robot is tilting forward. 
        Output ONLY ONE JSON object: {{"action": "step_forward" | "step_backward" | "lean_left" | "lean_right" | "hold", "confidence": 0.0-1.0}}
        """
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.1
            }, timeout=5)
            res_json = response.json()
            # Basic extraction (0.8B models might be messy, so we fallback)
            import re
            match = re.search(r'\{.*\}', res_json.get('response', '{}'), re.DOTALL)
            if match:
                return json.loads(match.group())
            return {"action": "hold", "confidence": 0.5}
        except Exception as e:
            return {"action": "hold", "confidence": 0.0, "error": str(e)}

class MotorController:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud, timeout=1)
        time.sleep(2) # Wait for ESP32 to reset

    def send_command(self, action):
        """Sends high-level command to ESP32 firmware."""
        cmd = f"CMD:{action.upper()}\n"
        self.ser.write(cmd.encode('utf-8'))
        print(f"[TX] {cmd.strip()}")

def main():
    print("🔋 TITAN-7 ARM64 Brain Initializing...")
    
    # Check termux-api
    if subprocess.run(['termux-sensor', '-l'], capture_output=True).returncode != 0:
        print("❌ termux-api not installed. Run: pkg install termux-api")
        return

    try:
        mc = MotorController(SERIAL_PORT, BAUD_RATE)
        print(f"✅ Connected to ESP32 on {SERIAL_PORT}")
    except Exception as e:
        print(f"⚠️ Could not connect to serial: {e}")
        print("Running in SIMULATION mode (no motor output).")
        mc = None

    state = "standing"
    loop_count = 0

    try:
        while True:
            loop_count += 1
            
            # 1. Read Sensors (10Hz loop)
            sensors = TermuxSensor.get_imu()
            
            # 2. LLM Decision (Every 10 loops to save CPU, ~1Hz)
            if loop_count % 10 == 0:
                intent = LLMCortex.get_action_intent(sensors, state)
                action = intent.get("action", "hold")
                
                if action != "hold" and mc:
                    print(f"🧠 LLM Decision: {action} (Conf: {intent.get('confidence')})")
                    mc.send_command(action)
                    state = action
                else:
                    print(f"🧠 LLM Decision: hold")
            
            time.sleep(0.1) # 10Hz main loop

    except KeyboardInterrupt:
        print("\n🛑 Shutting down TITAN-7 Brain...")
        if mc:
            mc.send_command("HOLD")
            mc.ser.close()

if __name__ == "__main__":
    main()
