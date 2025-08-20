# HC-SR04 Ultrasonic Sensor Troubleshooting Guide

## Common Issues and Solutions

### 1. **Distance Readings Too High/Far**
**Symptoms**: Sensor shows objects as very far even when they're close
**Causes**:
- Incorrect timing implementation
- Missing timeout protection
- GPIO pin configuration issues
- Power supply problems

**Solutions**:
- Use the optimized `sensor_hcsr04_lgpio.py` script (recommended for Pi 5)
- Ensure proper GPIO pin setup
- Check power supply (5V recommended)
- Verify trigger pulse timing (10 microseconds)

### 2. **No Readings or Constant Errors**
**Symptoms**: Sensor returns no distance or constant error messages
**Causes**:
- Incorrect wiring
- GPIO permission issues
- Sensor not powered properly
- Echo pin not responding

**Solutions**:
```bash
# Check GPIO permissions
sudo usermod -a -G gpio $USER
# Or run with sudo
sudo python sensor_hcsr04_lgpio.py

# Verify wiring:
# VCC -> 5V (not 3.3V)
# GND -> Ground
# TRIG -> GPIO 23
# ECHO -> GPIO 24
```

### 3. **Inaccurate Readings**
**Symptoms**: Readings are inconsistent or inaccurate
**Causes**:
- Environmental factors (temperature, humidity)
- Sensor positioning
- Interference from other electronics
- Sensor quality issues

**Solutions**:
- Keep sensor away from moving air
- Ensure stable mounting
- Use multiple readings and average them
- Check for electromagnetic interference

## 🔌 **Wiring Verification**

### **Correct Wiring (Based on Official Pi Hut Tutorial):**

1. **Sensor Connections:**
   - **Vcc** → 5V power rail (Red wire)
   - **GND** → Ground rail (Black wire)
   - **TRIG** → GPIO 23 [Pin 16] (Blue wire)
   - **ECHO** → GPIO 24 [Pin 18] via voltage divider (Yellow wire)

2. **Voltage Divider (Required for ECHO pin):**
   - **ECHO** → 1kΩ resistor → GPIO 24
   - **1kΩ rail** → 2kΩ resistor → GND
   - This protects the Pi from 5V ECHO signal

3. **Power Connections:**
   - **GPIO 5V [Pin 2]** → Power rail
   - **GPIO GND [Pin 6]** → Ground rail

### **Common Wiring Mistakes:**
- ❌ **Missing voltage divider** - ECHO pin outputs 5V, Pi expects 3.3V
- ❌ **Wrong GPIO pins** - Must use BCM numbering (23, 24)
- ❌ **Reversed TRIG/ECHO** - Check wire colors carefully
- ❌ **Loose connections** - Ensure all wires are firmly seated

### **Pin Reference:**
- **BCM 23** = Physical Pin 16 (TRIG)
- **BCM 24** = Physical Pin 18 (ECHO)
- **5V** = Physical Pin 2
- **GND** = Physical Pin 6

*Reference: [The Pi Hut HC-SR04 Tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi)*

## Software Configuration

### Key Settings in `config.py`
```python
# HC-SR04 optimized settings
SETTLE_TIME = 0.1        # seconds - sensor settling time
PULSE_DURATION = 0.00001 # 10 microseconds trigger pulse
ECHO_TIMEOUT = 0.1       # seconds - echo response timeout
SOUND_SPEED_CM_S = 34300 # cm/s at 20°C
ROUND_TRIP_DIVISOR = 2   # for round-trip calculation
```

### Testing Commands
```bash
# Test configuration
python test_hcsr04.py

# Run real-time monitoring
python sensor_hcsr04_lgpio.py

# Test with mock mode (for development)
# Edit config.py: USE_MOCK_GPIO = True
```

## Performance Optimization

### Update Intervals
- **Real-time monitoring**: 1 second (configurable)
- **High-speed monitoring**: 0.5 seconds
- **Battery saving**: 2-5 seconds

### Distance Range
- **Minimum**: 0.5 cm (reliable)
- **Maximum**: 400 cm (reliable)
- **Optimal**: 10-200 cm

### Accuracy Factors
- **Temperature**: Speed of sound varies with temperature
- **Humidity**: Minimal effect
- **Air pressure**: Minimal effect
- **Object surface**: Hard surfaces work best

## Debugging Steps

### 1. Check GPIO Status
```bash
# Check if lgpio is available (recommended for Pi 5)
python -c "import lgpio; print('lgpio available')"

# Check if RPi.GPIO is available (fallback option)
python -c "import RPi.GPIO as GPIO; print('RPi.GPIO available')"
```

### 2. Test Individual Components
```bash
# Test with lgpio (recommended for Pi 5)
python -c "
import lgpio
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, 23)
lgpio.gpio_write(h, 23, 1)
print('Trigger pin set high with lgpio')
lgpio.gpiochip_close(h)
"

# Test with RPi.GPIO (fallback)
python -c "
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, True)
print('Trigger pin set high with RPi.GPIO')
GPIO.cleanup()
"
```

### 3. Monitor GPIO Activity
```bash
# Watch GPIO pins in real-time
watch -n 0.1 'gpio readall'
```

### 4. Check System Logs
```bash
# Check for GPIO errors
dmesg | grep -i gpio
journalctl -f | grep -i gpio
```

## Common Error Messages

### "Cannot determine SOC peripheral base address"
- **Cause**: Running RPi.GPIO on Raspberry Pi 5 or newer models
- **Solution**: Use `sensor_hcsr04_lgpio.py` with lgpio library instead

### "Permission denied"
- **Cause**: User not in gpio group
- **Solution**: 
```bash
sudo usermod -a -G gpio $USER
# Then log out and back in
```

### "Echo timeout"
- **Cause**: Sensor not responding or wiring issue
- **Solution**: Check wiring, power supply, and sensor orientation

### "Distance outside valid range"
- **Cause**: Measurement error or sensor malfunction
- **Solution**: Check sensor positioning and environmental factors

### "lgpio not available"
- **Cause**: lgpio library not installed
- **Solution**: Install with `sudo apt install python3-lgpio` or use mock mode

## Advanced Troubleshooting

### Using Oscilloscope
If available, monitor:
- Trigger pulse (should be 10μs high)
- Echo response timing
- Signal quality and noise

### Alternative GPIO Pins
If pins 23/24 have issues:
```python
# Try different pins
TRIG_PIN = 17  # GPIO 17
ECHO_PIN = 27  # GPIO 27
```

### Multiple Sensors
For multiple HC-SR04 sensors:
- Use different GPIO pins
- Ensure adequate power supply
- Avoid interference between sensors

## Performance Benchmarks

### Typical Response Times
- **Trigger to echo start**: 0.1-1ms
- **Echo duration**: 0.03-12ms (0.5-400cm)
- **Total measurement time**: 1-15ms

### Accuracy
- **Close range (0.5-50cm)**: ±2-3mm
- **Medium range (50-200cm)**: ±5-10mm
- **Long range (200-400cm)**: ±10-20mm

### Reliability
- **Success rate**: >95% in good conditions
- **Failure modes**: Timeout, out of range, interference
- **Recovery**: Automatic retry on next measurement

## Support and Resources

### Documentation
- [HC-SR04 Datasheet](https://www.microchip.com/en-us/product/HCSR04)
- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)

### Community Resources
- Raspberry Pi Forums
- GitHub Issues
- Stack Overflow

### Testing Tools
- `test_hcsr04.py` - Configuration testing and validation
- `sensor_hcsr04_lgpio.py` - Real-time monitoring (recommended for Pi 5)
