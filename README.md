# TITAN-7 ARM64 🤖

Smartphone-centric bipedal robot framework. Your Android phone is the brain, Termux is the OS, a quantized local LLM (0.5B-1B) is the cognitive cortex, and an ESP32 handles real-time motor control.

## 🧠 Architecture
```
[ User / Voice ] 
       ↓
[ Termux (Android) ] ←→ [ termux-sensor API (IMU, Gyro) ]
       ↓                        ↓
[ Ollama (0.8B Model) ]  [ Python Gait/Balance Controller ]
       ↓                        ↓
       └──────→ [ WebSocket / Serial ] ←──────┘
                      ↓
               [ ESP32 Microcontroller ]
                      ↓
               [ 12x MG996R Servos (6 DOF per leg) ]
```

## 🛠️ Quick Start (Termux)
```bash
# 1. Clone and setup
cd ~/titan-7arm64
chmod +x setup.sh
./setup.sh

# 2. Install local 0.8B model (Qwen 0.5B or Llama 3.2 1B)
ollama pull qwen2:0.5b

# 3. Run the brain
python3 brain/main.py
```

## 🔌 Hardware Bridge
- **Phone to ESP32:** USB OTG (Serial) or Bluetooth Classic (RFCOMM). USB recommended for lowest latency (<10ms).
- **Shizuku:** Optional, but grants Termux direct access to high-frequency sensor polling without battery-draining wakelocks.

See `docs/blueprint.md` for the full BOM, pricing, and physical dimensions.
