# Ultrasonic Distance Sensor Project

This project uses an ultrasonic distance sensor with a Raspberry Pi to measure distances. It includes both real hardware support and mock modes for development and testing.

## Features

- **Real-time Distance Monitoring**: Continuous distance updates with configurable intervals
- **Mock Mode Support**: Development and testing without actual hardware
- **Configurable Settings**: Easy customization of pins, timing, and display options
- **Statistics Tracking**: Running averages, min/max values, and measurement history
- **Visual Indicators**: Color-coded distance status and emoji indicators
- **Graceful Shutdown**: Clean exit with Ctrl+C

## Setup

### 1. Create Virtual Environment
```bash
python3 -m venv sensor_env
```

### 2. Activate Virtual Environment
```bash
source sensor_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start
```bash
# Clone the repository
git clone https://github.com/kagamirudo/hc-sr04-driver.git
cd hc-sr04-driver

# Activate the environment
source activate_env.sh

# Run the sensor script:
python sensor_hcsr04_lgpio.py     # HC-SR04 with lgpio (recommended for Pi 5)
python test_hcsr04.py             # Test HC-SR04 functionality

# Deactivate when done
deactivate
```

### Manual Activation
```bash
source sensor_env/bin/activate
python sensor_hcsr04_lgpio.py
deactivate
```

### Script Options

1. **`sensor_hcsr04_lgpio.py`** - **HC-SR04 optimized version with lgpio (recommended for Raspberry Pi 5)**
2. **`test_hcsr04.py`** - **HC-SR04 specific testing and validation**
3. **`config.py`** - Configuration file to switch between mock/real modes

## Real-time Monitoring

The project now supports continuous real-time distance monitoring with the following features:

### Continuous Updates
- Distance measurements update every second (configurable)
- Real-time display with timestamps
- Visual status indicators (🟢 Close, 🟡 Medium, 🔴 Far)

### Statistics Tracking
- Running average of recent measurements
- Minimum and maximum distance values
- Distance range analysis
- Session duration and measurement count

### Display Features
- Clear screen updates for better readability
- Formatted output with emojis and status indicators
- Configurable update intervals
- Graceful shutdown with Ctrl+C

### Example Output
```
============================================================
           REAL-TIME DISTANCE SENSOR
============================================================
Mode: MOCK GPIO
Update Interval: 1.0 seconds
Press Ctrl+C to stop
============================================================
[20:52:22] Distance:  96.61 cm 🟡 Medium
[20:52:23] Distance:  20.45 cm 🟢 Very Close
[20:52:24] Distance: 145.32 cm 🟠 Far
```

## HC-SR04 Sensor Support

The project now includes **optimized support for HC-SR04 ultrasonic sensors** with proper timing implementation and error handling.

### HC-SR04 Specific Features
- **Proper Timing**: Correct 10-microsecond trigger pulse and echo timing
- **Error Handling**: Timeout protection and range validation
- **Optimized Configuration**: Reduced settle time and proper echo timeout
- **Distance Validation**: Ensures readings are within HC-SR04's 2-400cm range

### Recommended Script for HC-SR04
```bash
# Use the HC-SR04 optimized version
python sensor_hcsr04.py
```

### Key Configuration for HC-SR04
```python
# HC-SR04 optimized settings in config.py
SETTLE_TIME = 0.1        # seconds (reduced from 2s)
ECHO_TIMEOUT = 0.1       # seconds for echo response
MIN_DISTANCE = 2.0       # cm - HC-SR04 minimum
MAX_DISTANCE = 400.0     # cm - HC-SR04 maximum
```

### Troubleshooting HC-SR04 Issues
If you're experiencing problems with your HC-SR04 sensor:

1. **Distance readings too high/far**: Use `sensor_hcsr04.py` instead of other scripts
2. **No readings**: Check wiring and GPIO permissions
3. **Inaccurate readings**: Verify power supply (5V) and sensor positioning

For detailed troubleshooting, see: **[HC-SR04_TROUBLESHOOTING.md](HC-SR04_TROUBLESHOOTING.md)**

### Testing HC-SR04 Configuration
```bash
# Test HC-SR04 timing and configuration
python test_hcsr04.py

# This will show:
# - Timing parameters validation
# - Distance calculation examples
# - Configuration verification
```

## 🔌 **Wiring Instructions**

### **Hardware Requirements:**
- HC-SR04 Ultrasonic Sensor
- Raspberry Pi (any model)
- Breadboard
- 4x Male-to-Female jumper wires (Red, Blue, Yellow, Black)
- 1x 1kΩ resistor (R1)
- 1x 2kΩ resistor (R2)

### **Connection Steps:**

1. **Connect sensor to jumper wires:**
   - **Red** → Vcc (Power)
   - **Blue** → TRIG (Trigger)
   - **Yellow** → ECHO (Echo)
   - **Black** → GND (Ground)

2. **Power connections:**
   - **Vcc (Red)** → Breadboard positive rail
   - **GND (Black)** → Breadboard negative rail
   - **GPIO 5V [Pin 2]** → Breadboard positive rail
   - **GPIO GND [Pin 6]** → Breadboard negative rail

3. **Signal connections:**
   - **TRIG (Blue)** → Breadboard rail → **GPIO 23 [Pin 16]**
   - **ECHO (Yellow)** → Breadboard rail → **1kΩ resistor (R1)** → **GPIO 24 [Pin 18]**
   - **R1 rail** → **2kΩ resistor (R2)** → **GND rail**

### **Important Notes:**
- The voltage divider (R1 + R2) protects the Pi from the 5V ECHO signal
- GPIO 23 = Pin 16 (BCM numbering)
- GPIO 24 = Pin 18 (BCM numbering)
- Use BCM pin numbering in your code

*Wiring instructions based on [The Pi Hut's official HC-SR04 tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi)*

## Hardware Requirements

- Raspberry Pi (or compatible board)
- Ultrasonic distance sensor (HC-SR04 or similar)
- Jumper wires

## Pin Connections

- TRIG: GPIO 23 (BCM)
- ECHO: GPIO 24 (BCM)

## Configuration

Edit `config.py` to customize:
- GPIO pin assignments
- Timing parameters
- Mock mode settings
- Distance calculation constants
- Real-time update intervals
- Display preferences
- Distance thresholds for status indicators

### Real-time Settings
```python
# Update frequency
UPDATE_INTERVAL = 1.0  # seconds between measurements

# Display options
CLEAR_SCREEN = True      # Clear screen between updates
SHOW_STATISTICS = True   # Show measurement statistics
SHOW_TIMESTAMPS = True   # Show timestamps

# Distance thresholds for status indicators
DISTANCE_THRESHOLDS = {
    'very_close': 30,   # cm
    'close': 60,        # cm
    'medium': 120,      # cm
    'far': 200          # cm
}
```

To switch between mock and real modes:
```python
# For development/testing (no hardware required)
USE_MOCK_GPIO = True

# For actual Raspberry Pi hardware
USE_MOCK_GPIO = False
```

## Troubleshooting

- **"Cannot determine SOC peripheral base address"**: This error occurs when running on non-Raspberry Pi hardware or without proper GPIO permissions
- **Permission denied**: Run with `sudo` or add your user to the `gpio` group
- **Package installation issues**: Always use the virtual environment to avoid system Python conflicts
- **Development without hardware**: Use mock mode with `USE_MOCK_GPIO = True` in `config.py`
- **Real-time updates too slow**: Adjust `UPDATE_INTERVAL` in `config.py` for faster updates
- **Display issues**: Set `CLEAR_SCREEN = False` if you prefer scrolling output

## Dependencies

- RPi.GPIO: GPIO library for Raspberry Pi
- yapf: Python code formatter
- platformdirs: Platform-specific directory utilities
