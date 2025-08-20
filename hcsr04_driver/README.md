# HC-SR04 Ultrasonic Sensor Driver

A professional Python driver for HC-SR04 ultrasonic distance sensors on Raspberry Pi.

## Features

- 🚀 **Automatic GPIO Detection**: Automatically detects and uses the best available GPIO library
- 📏 **Extended Range**: Supports distances from 0.5cm to 400cm
- ⚡ **Real-time Monitoring**: Configurable update intervals for continuous monitoring
- 🎯 **Smart Fallbacks**: lgpio (Pi 5) → RPi.GPIO → Mock mode
- 📊 **Statistics Tracking**: Built-in measurement statistics and logging
- 🔧 **Fully Configurable**: Customizable pins, timing, and thresholds
- 🧪 **Mock Mode**: Development and testing without hardware
- 🎨 **Professional API**: Clean, intuitive interface with context managers

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/kagamirudo/hc-sr04-driver.git
cd hc-sr04-driver

# Install the package
pip install -e .
```

### Basic Usage

```python
from hcsr04_driver import HCSR04Sensor

# Create sensor with default configuration
sensor = HCSR04Sensor()

# Single measurement
distance = sensor.measure_distance()
if distance:
    print(f"Distance: {distance} cm")

# Cleanup
sensor.cleanup()
```

### Real-time Monitoring

```python
from hcsr04_driver import HCSR04Sensor

# Start continuous monitoring
sensor = HCSR04Sensor()
try:
    sensor.start_monitoring()
except KeyboardInterrupt:
    print("Monitoring stopped")
finally:
    sensor.cleanup()
```

### Custom Configuration

```python
from hcsr04_driver import HCSR04Sensor, HCSR04Config

# Create custom configuration
config = HCSR04Config(
    trig_pin=17,           # Different GPIO pin
    echo_pin=27,           # Different GPIO pin
    update_interval=0.5,   # Faster updates
    min_distance=1.0,      # Custom minimum distance
    max_distance=300.0,    # Custom maximum distance
)

# Use custom configuration
sensor = HCSR04Sensor(config)
```

### Context Manager

```python
from hcsr04_driver import HCSR04Sensor

# Automatic cleanup with context manager
with HCSR04Sensor() as sensor:
    distance = sensor.measure_distance()
    print(f"Distance: {distance} cm")
# GPIO automatically cleaned up
```

## API Reference

### HCSR04Sensor

Main sensor class for HC-SR04 ultrasonic sensors.

#### Methods

- `measure_distance()`: Take a single distance measurement
- `start_monitoring(callback=None)`: Start continuous monitoring
- `stop_monitoring()`: Stop continuous monitoring
- `get_statistics()`: Get measurement statistics
- `cleanup()`: Cleanup GPIO resources

#### Properties

- `config`: Current configuration
- `gpio_library`: Active GPIO library name
- `running`: Whether monitoring is active

### HCSR04Config

Configuration class for sensor parameters.

#### Key Parameters

- `trig_pin`: GPIO pin for trigger signal (default: 23)
- `echo_pin`: GPIO pin for echo signal (default: 24)
- `update_interval`: Interval between measurements (default: 1.0s)
- `min_distance`: Minimum reliable distance (default: 0.5cm)
- `max_distance`: Maximum reliable distance (default: 400cm)
- `use_mock_gpio`: Use mock mode for testing (default: False)

## Examples

See `examples.py` for comprehensive usage examples:

```bash
python -m hcsr04_driver.examples
```

## Hardware Setup

### Wiring

```
HC-SR04    Raspberry Pi
VCC    ->  5V (Pin 2)
GND    ->  Ground (Pin 6)
TRIG   ->  GPIO 23 (Pin 16)
ECHO   ->  GPIO 24 (Pin 18)
```

### Requirements

- Raspberry Pi (any model)
- HC-SR04 ultrasonic sensor
- Jumper wires
- Python 3.8+

## GPIO Library Support

| Library | Pi Model | Status | Notes |
|---------|----------|---------|-------|
| lgpio | Pi 5 | ✅ Recommended | Best performance, modern API |
| RPi.GPIO | Pi 1-4 | ✅ Supported | Fallback option |
| Mock | Any | ✅ Development | Testing without hardware |

## Development

### Install Development Dependencies

```bash
pip install -e .[dev]
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black hcsr04_driver/
flake8 hcsr04_driver/
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
