# Configuration file for sensor project
import os

# Set to True to use mock GPIO (for development/testing)
# Set to False to use real GPIO (for actual Raspberry Pi)
USE_MOCK_GPIO = False  # Changed to False for real HC-SR04 sensor

# GPIO pin configuration
TRIG_PIN = 23
ECHO_PIN = 24

# HC-SR04 Sensor settings (optimized for accuracy)
SETTLE_TIME = 0.1  # seconds - reduced from 2s to 0.1s for HC-SR04
PULSE_DURATION = 0.00001  # 10 microseconds (correct for HC-SR04)
ECHO_TIMEOUT = 0.1  # seconds - timeout for echo response

# Real-time update settings
UPDATE_INTERVAL = 1.0  # seconds between measurements

# Display settings
CLEAR_SCREEN = True  # Whether to clear screen between updates
SHOW_STATISTICS = True  # Whether to show measurement statistics
SHOW_TIMESTAMPS = True  # Whether to show timestamps

# Distance calculation constants (optimized for HC-SR04)
SOUND_SPEED_CM_S = 34300  # Speed of sound in cm/s at 20°C
ROUND_TRIP_DIVISOR = 2    # Divide by 2 for round trip

# HC-SR04 specific settings
MIN_DISTANCE = 0.5    # cm - minimum reliable distance for HC-SR04
MAX_DISTANCE = 400.0  # cm - maximum reliable distance for HC-SR04

# Mock settings (for development)
MOCK_MIN_DISTANCE = 10.0   # cm
MOCK_MAX_DISTANCE = 200.0  # cm

# Distance thresholds for status indicators (cm)
DISTANCE_THRESHOLDS = {
    'very_close': 5,    # cm - adjusted for new 0.5cm minimum
    'close': 30,        # cm
    'medium': 100,      # cm
    'far': 200          # cm
}
