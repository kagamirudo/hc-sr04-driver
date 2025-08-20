#!/usr/bin/env python3
"""
Test script for HC-SR04 sensor functionality
Tests the sensor with proper timing and error handling
"""

import time
import random
from config import *


def test_hcsr04_timing():
    """Test HC-SR04 timing parameters"""
    print("HC-SR04 Timing Test")
    print("=" * 40)
    print(f"SETTLE_TIME: {SETTLE_TIME} seconds")
    print(
        f"PULSE_DURATION: {PULSE_DURATION} seconds ({PULSE_DURATION * 1000000:.1f} microseconds)")
    print(f"ECHO_TIMEOUT: {ECHO_TIMEOUT} seconds")
    print(f"SOUND_SPEED: {SOUND_SPEED_CM_S} cm/s")
    print(f"Valid Range: {MIN_DISTANCE}-{MAX_DISTANCE} cm")
    print("=" * 40)


def test_distance_calculation():
    """Test distance calculation with sample timing values"""
    print("\nDistance Calculation Test")
    print("=" * 40)
    
    # Test cases with realistic timing values for HC-SR04
    # For 0.5cm: time = (0.5 * 2) / 34300 = 0.000029 seconds = 0.029ms
    test_cases = [
        (0.000029, "0.5cm object"),    # 0.029ms = ~0.5cm (round trip)
        (0.000058, "1cm object"),      # 0.058ms = ~1cm (round trip)
        (0.000583, "10cm object"),     # 0.583ms = ~10cm (round trip)
        (0.001166, "20cm object"),     # 1.166ms = ~20cm (round trip)
        (0.002915, "50cm object"),     # 2.915ms = ~50cm (round trip)
        (0.005831, "100cm object"),    # 5.831ms = ~100cm (round trip)
        (0.011662, "200cm object"),    # 11.662ms = ~200cm (round trip)
    ]
    
    for pulse_duration, description in test_cases:
        # Calculate distance: (time * speed) / ROUND_TRIP_DIVISOR
        distance = (pulse_duration * SOUND_SPEED_CM_S) / ROUND_TRIP_DIVISOR
        print(f"{description:12}: {pulse_duration*1000:6.3f}ms → {distance:6.1f} cm")
    
    print("\nNote: These are round-trip times for the specified distances")
    print("Actual HC-SR04 timing may vary based on sensor quality and environment")
    
    # Show the reverse calculation
    print("\nReverse calculation (distance to timing):")
    test_distances = [0.5, 1, 10, 20, 50, 100, 200]
    for dist in test_distances:
        # Time = (distance * ROUND_TRIP_DIVISOR) / speed
        timing = (dist * ROUND_TRIP_DIVISOR) / SOUND_SPEED_CM_S
        print(f"{dist:4.1f}cm object: {timing*1000:6.3f}ms round-trip time")


def test_mock_mode():
    """Test mock mode functionality"""
    print("\nMock Mode Test")
    print("=" * 40)

    # Simulate several measurements
    for i in range(5):
        distance = random.uniform(MOCK_MIN_DISTANCE, MOCK_MAX_DISTANCE)
        print(f"Mock measurement {i+1}: {distance:6.2f} cm")


def main():
    """Main test function"""
    print("HC-SR04 Sensor Test Suite")
    print("=" * 50)

    # Test timing parameters
    test_hcsr04_timing()

    # Test distance calculations
    test_distance_calculation()

    # Test mock mode
    test_mock_mode()

    print("\n" + "=" * 50)
    print("Test completed!")
    print("\nTo test with real HC-SR04 sensor:")
    print("1. Ensure USE_MOCK_GPIO = False in config.py")
    print("2. Connect HC-SR04 to GPIO 23 (TRIG) and GPIO 24 (ECHO)")
    print("3. Run: python sensor_hcsr04.py")


if __name__ == "__main__":
    main()
