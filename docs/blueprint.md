# TITAN-7 ARM64: Hardware Blueprint

## 📏 Physical Specifications
- **Height:** ~38 cm (15 inches)
- **Weight:** ~1.2 kg (2.6 lbs) - *Must stay under 1.5kg for MG996R torque limits*
- **Degrees of Freedom (DOF):** 12 (6 per leg: Hip Yaw, Hip Roll, Hip Pitch, Knee Pitch, Ankle Pitch, Ankle Roll)
- **Battery Life:** ~45 mins continuous walking

## 💰 Bill of Materials (BOM) & Pricing

| Component | Spec | Qty | Est. Price (USD) | Total |
|-----------|------|-----|------------------|-------|
| **Brain** | Your existing Android Phone (ARM64) | 1 | $0 (Owned) | $0 |
| **MCU** | ESP32-WROOM-32 (WiFi + BT) | 1 | $6.00 | $6.00 |
| **Servos** | MG996R Metal Gear (13kg/cm torque) | 12 | $5.50 | $66.00 |
| **Power** | 3S LiPo Battery (11.1V, 2200mAh) | 1 | $15.00 | $15.00 |
| **Regulator**| UBEC 5V 3A (Steps 11.1V down to 5V for ESP32/Servos) | 1 | $4.00 | $4.00 |
| **Frame** | 3mm Aluminum U-Channel + 3D Printed PLA joints | 1 | $15.00 | $15.00 |
| **Cabling** | Silicone servo extension wires, XT60 connectors | 1 | $10.00 | $10.00 |
| **Mount** | Universal phone clamp + Velcro | 1 | $5.00 | $5.00 |
| **TOTAL** | | | | **~$121.00** |

## 🔌 Wiring Diagram (Conceptual)
```
[ 3S LiPo 11.1V ] 
       │
       ├──(Main Power)──→ [ UBEC 5V 3A ] ──→ [ ESP32 5V/VIN ]
       │                                     └──→ [ Servo VCC (All 12 in parallel) ]
       │
       └──(Balance Lead)─→ [ Phone USB-C OTG ] (Charges phone slowly while running)
```
*⚠️ WARNING: Do NOT power 12 MG996R servos directly from the ESP32 3.3V pin. It will fry the board. Use the UBEC.*

## 📱 Termux Sensor Mapping
With `termux-api` installed, the phone provides:
- `termux-sensor -s "Accelerometer"` → Z-axis gravity for ankle pitch correction.
- `termux-sensor -s "Gyroscope"` → Yaw/Pitch/Roll for dynamic balance (complementary filter).
- `termux-sensor -s "Orientation"` → Absolute heading for navigation.
