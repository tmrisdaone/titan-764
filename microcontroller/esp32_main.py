# TITAN-7 ESP32 Motor Controller (MicroPython)
# Flash this to your ESP32 using ampy or Thonny.
# Listens for high-level commands from the Termux brain and executes servo PWM.

import machine
import time
import sys

# --- CONFIG ---
# Define servo pins (GPIO) for 6 DOF right leg (example)
# 0: Hip Yaw, 1: Hip Roll, 2: Hip Pitch, 3: Knee Pitch, 4: Ankle Pitch, 5: Ankle Roll
SERVO_PINS = [12, 13, 14, 25, 26, 27]
BAUD_RATE = 115200

# Initialize PWM for servos (50Hz for standard servos)
servos = [machine.PWM(machine.Pin(pin), freq=50) for pin in SERVO_PINS]

# Center position (1.5ms pulse width = ~75 duty cycle for 16-bit PWM at 50Hz)
# Note: MicroPython ESP32 PWM duty is 0-65535. 1.5ms / 20ms = 7.5% -> ~4915
CENTER_DUTY = 4915

def set_servo(servo_idx, angle_deg):
    """Converts -90 to 90 degrees to PWM duty cycle."""
    # Clamp angle
    angle_deg = max(-90, min(90, angle_deg))
    # Map -90..90 to ~2400..7400 duty cycle
    duty = int(4915 + (angle_deg / 90.0) * 2500)
    servos[servo_idx].duty_u16(duty)

def stand_neutral():
    """All joints to 0 degrees (neutral standing pose)."""
    for i in range(len(servos)):
        set_servo(i, 0)
    print("POSE: NEUTRAL_STAND")

def step_forward():
    """Simple 2-phase walk cycle for demonstration."""
    print("POSE: STEP_FORWARD")
    # Phase 1: Shift weight to left leg, lift right leg
    set_servo(2, 15)  # Right hip pitch forward
    set_servo(3, -30) # Right knee bend
    
    time.sleep(0.3)
    
    # Phase 2: Plant right leg, shift body forward
    set_servo(2, -10) # Right hip pitch back (push)
    set_servo(3, 0)   # Right knee straight
    
    time.sleep(0.3)
    stand_neutral()

def hold():
    """Freeze current position."""
    print("POSE: HOLD")
    # In a real implementation, this would maintain current PWM duty cycles
    pass

def main():
    print("TITAN-7 ESP32 Firmware Booted.")
    stand_neutral()
    
    # Setup UART (USB Serial)
    uart = machine.UART(0, baudrate=BAUD_RATE)
    
    while True:
        if uart.any():
            # Read line until newline
            cmd = uart.readline().decode('utf-8').strip()
            
            if cmd:
                print(f"RX: {cmd}")
                
                if cmd.startswith("CMD:"):
                    action = cmd.split(":")[1].upper()
                    
                    if action == "STEP_FORWARD":
                        step_forward()
                    elif action == "STEP_BACKWARD":
                        print("POSE: STEP_BACKWARD")
                        # Implement reverse kinematics here
                        stand_neutral()
                    elif action == "HOLD":
                        hold()
                    else:
                        print(f"UNKNOWN CMD: {action}")
                        
        time.sleep(0.05) # 20Hz polling

if __name__ == "__main__":
    main()
