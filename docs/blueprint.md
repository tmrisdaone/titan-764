# Titan-7 Hardware Blueprint

## ⚠️ MANDATORY REQUIREMENT: SHIZUKU
**Shizuku is NOT optional.** Android aggressively kills background processes and throttles sensor polling to save battery. To achieve the 50Hz+ polling rate required for bipedal balance without the phone putting Termux to sleep, you **must** use Shizuku to grant Termux elevated, battery-optimized permissions. 

1. Install [Shizuku](https://shizuku.rikka.app/) from the Play Store or GitHub.
2. Start Shizuku via Wireless Debugging (Android 11+) or Root.
3. Grant Termux elevated permissions via Shizuku to prevent wakelock penalties and background throttling during sensor polling.

## 🛠️ Bill of Materials (BOM)
**Total Estimated Cost:** ~$121 USD (assuming you already own the Android phone).

| Component | Qty | Estimated Price | Purpose |
|-----------|-----|-----------------|---------|
| ESP32 Dev Board (WROOM-32) | 1 | $6 | Low-latency motor controller & serial bridge |
| MG996R Metal-Gear Servos | 12 | $60 ($5/ea) | Heavy-duty joint actuation (6 per leg) |
| 3S LiPo Battery (11.1V, 2200mAh) | 1 | $20 | Main power for all 12 servos |
| UBEC (5V 5A) | 1 | $8 | Steps 11.1V down to safe 5V for ESP32 & logic |
| USB OTG Adapter | 1 | $3 | Connects phone to ESP32 via serial |
| 3D Printed Chassis (or Aluminum) | 1 | $24 | Structural frame (filament cost / scrap metal) |

## 🔌 Wiring Guide
1. **Power**: LiPo (+) → UBEC (+IN), LiPo (-) → UBEC (-IN).
2. **Servo Power**: All 12 servo VCC → UBEC (+OUT), all servo GND → UBEC (-OUT). *DO NOT power servos from the ESP32.*
3. **Logic Power**: UBEC (+OUT) → ESP32 VIN, UBEC (-OUT) → ESP32 GND.
4. **Signal**: ESP32 GPIO pins (e.g., 12-17 for Left Leg, 18-23 for Right Leg) → Servo PWM signal wires.
5. **Comm**: ESP32 TX/RX → Phone via USB OTG (Serial).

## 📐 Dimensions & Kinematics
- **Leg Configuration**: 6-DOF per leg (Hip Yaw, Hip Roll, Hip Pitch, Knee Pitch, Ankle Pitch, Ankle Roll).
- **Thigh Length**: ~150mm
- **Shin Length**: ~150mm
- **Total Height**: ~400mm (standing)
- **Weight Target**: < 2.5kg (to stay within MG996R torque limits)
