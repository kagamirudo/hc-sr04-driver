#!/usr/bin/env python3
"""
HC-SR04 Ultrasonic Distance Sensor Implementation using lgpio
Optimized for Raspberry Pi 5 and newer models with proper timing
"""

import sys
import time
import lgpio
import random
import signal
import RPi.GPIO as GPIO
from config import *

# Global flag for graceful shutdown
running = True


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    global running
    print("\n" + "="*50)
    print("Shutting down gracefully...")
    running = False


def get_gpio():
    """Get GPIO module - try lgpio first, then fall back to RPi.GPIO"""
    if USE_MOCK_GPIO:
        print("Using MOCK GPIO mode (development/testing)")
        return None, None  # Return None for both gpio module and handle
    else:
        print("Using REAL GPIO mode with HC-SR04 sensor")
        try:
            # Open GPIO chip
            h = lgpio.gpiochip_open(0)
            print("Using lgpio library (recommended for Raspberry Pi 5)")
            return lgpio, h
        except ImportError:
            print("lgpio not available, trying RPi.GPIO...")
            try:
                print("Using RPi.GPIO library")
                return GPIO, None
            except ImportError:
                print(
                    "Error: No GPIO library available. Please install lgpio or RPi.GPIO")
                return None, None


def measure_distance_lgpio(lgpio, h):
    """
    Measure distance using HC-SR04 with lgpio library
    """
    try:
        # Setup GPIO pins
        lgpio.gpio_claim_output(h, TRIG_PIN)
        lgpio.gpio_claim_input(h, ECHO_PIN)

        # Ensure trigger pin is low initially
        lgpio.gpio_write(h, TRIG_PIN, 0)
        time.sleep(SETTLE_TIME)

        # Send trigger pulse (10 microseconds high)
        lgpio.gpio_write(h, TRIG_PIN, 1)
        time.sleep(PULSE_DURATION)
        lgpio.gpio_write(h, TRIG_PIN, 0)

        # Wait for echo pin to go high (start of echo)
        timeout_start = time.time()
        while lgpio.gpio_read(h, ECHO_PIN) == 0:
            if time.time() - timeout_start > ECHO_TIMEOUT:
                print("    ⚠️  Echo start timeout")
                return None
            pulse_start = time.time()

        # Wait for echo pin to go low (end of echo)
        timeout_start = time.time()
        while lgpio.gpio_read(h, ECHO_PIN) == 1:
            if time.time() - timeout_start > ECHO_TIMEOUT:
                print("    ⚠️  Echo end timeout")
                return None
            pulse_end = time.time()

        # Calculate pulse duration
        pulse_duration = pulse_end - pulse_start

        # Calculate distance using speed of sound
        distance = (pulse_duration * SOUND_SPEED_CM_S) / ROUND_TRIP_DIVISOR

        # Validate distance range for HC-SR04
        if distance < MIN_DISTANCE or distance > MAX_DISTANCE:
            print(
                f"    ⚠️  Distance {distance:.1f} cm outside valid range ({MIN_DISTANCE}-{MAX_DISTANCE} cm)")
            return None

        return round(distance, 2)

    except Exception as e:
        print(f"    ❌ Error during measurement: {e}")
        return None


def measure_distance_rpi_gpio(gpio):
    """
    Measure distance using HC-SR04 with RPi.GPIO library
    """
    try:
        # Setup GPIO pins
        gpio.setup(TRIG_PIN, gpio.OUT)
        gpio.setup(ECHO_PIN, gpio.IN)

        # Ensure trigger pin is low initially
        gpio.output(TRIG_PIN, False)
        time.sleep(SETTLE_TIME)

        # Send trigger pulse (10 microseconds high)
        gpio.output(TRIG_PIN, True)
        time.sleep(PULSE_DURATION)
        gpio.output(TRIG_PIN, False)

        # Wait for echo pin to go high (start of echo)
        timeout_start = time.time()
        while gpio.input(ECHO_PIN) == 0:
            if time.time() - timeout_start > ECHO_TIMEOUT:
                print("    ⚠️  Echo start timeout")
                return None
            pulse_start = time.time()

        # Wait for echo pin to go low (end of echo)
        timeout_start = time.time()
        while gpio.input(ECHO_PIN) == 1:
            if time.time() - timeout_start > ECHO_TIMEOUT:
                print("    ⚠️  Echo end timeout")
                return None
            pulse_end = time.time()

        # Calculate pulse duration
        pulse_duration = pulse_end - pulse_start

        # Calculate distance using speed of sound
        distance = (pulse_duration * SOUND_SPEED_CM_S) / ROUND_TRIP_DIVISOR

        # Validate distance range for HC-SR04
        if distance < MIN_DISTANCE or distance > MAX_DISTANCE:
            print(
                f"    ⚠️  Distance {distance:.1f} cm outside valid range ({MIN_DISTANCE}-{MAX_DISTANCE} cm)")
            return None

        return round(distance, 2)

    except Exception as e:
        print(f"    ❌ Error during measurement: {e}")
        return None


def measure_distance_mock():
    """Mock distance measurement for testing"""
    time.sleep(0.1)
    mock_distance = random.uniform(MOCK_MIN_DISTANCE, MOCK_MAX_DISTANCE)
    return round(mock_distance, 2)


def measure_distance(gpio, h):
    """Measure distance using the appropriate method"""
    if USE_MOCK_GPIO:
        return measure_distance_mock()
    elif gpio.__name__ == 'lgpio':
        return measure_distance_lgpio(gpio, h)
    else:
        return measure_distance_rpi_gpio(gpio)


def get_distance_indicator(distance):
    """Get visual indicator for distance ranges"""
    if distance is None:
        return "❌ Error"
    elif distance < 1.0:
        return "🔴 Extremely Close"
    elif distance < DISTANCE_THRESHOLDS['very_close']:
        return "🟢 Very Close"
    elif distance < DISTANCE_THRESHOLDS['close']:
        return "🟢 Close"
    elif distance < DISTANCE_THRESHOLDS['medium']:
        return "🟡 Medium"
    elif distance < DISTANCE_THRESHOLDS['far']:
        return "🟠 Far"
    else:
        return "🔴 Very Far"


def continuous_measurement(gpio, h, update_interval=1.0):
    """Continuously measure and display distance with HC-SR04"""
    global running

    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Initial setup for RPi.GPIO
    if gpio and not USE_MOCK_GPIO and gpio.__name__ != 'lgpio':
        gpio.setmode(gpio.BCM)
        print("GPIO mode set to BCM")

    # Statistics tracking
    measurements = []
    start_time = time.time()

    print("=" * 60)
    print("           HC-SR04 REAL-TIME DISTANCE SENSOR")
    print("=" * 60)
    print(f"Mode: {'MOCK GPIO' if USE_MOCK_GPIO else 'REAL GPIO with HC-SR04'}")
    print(
        f"GPIO Library: {'lgpio' if gpio and gpio.__name__ == 'lgpio' else 'RPi.GPIO' if gpio else 'Mock'}")
    print(f"Update Interval: {UPDATE_INTERVAL} seconds")
    print(f"Trigger Pin: {TRIG_PIN}, Echo Pin: {ECHO_PIN}")
    print(f"Valid Range: {MIN_DISTANCE}-{MAX_DISTANCE} cm")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    try:
        while running:
            # Measure distance
            distance = measure_distance(gpio, h)

            # Update statistics
            if distance is not None:
                measurements.append(distance)
                if len(measurements) > 100:
                    measurements.pop(0)

            # Get current timestamp
            timestamp = time.strftime("%H:%M:%S")

            # Display current measurement
            if distance is not None:
                print(
                    f"[{timestamp}] Distance: {distance:6.2f} cm {get_distance_indicator(distance)}")
            else:
                print(f"[{timestamp}] Distance: ❌ Measurement failed")

            # Show running statistics every 5 measurements
            if len(measurements) % 5 == 0 and len(measurements) > 0:
                avg = sum(measurements) / len(measurements)
                min_val = min(measurements)
                max_val = max(measurements)
                print(
                    f"    Stats: Avg={avg:5.1f}, Min={min_val:5.1f}, Max={max_val:5.1f} cm")
                print(
                    f"    Running for: {time.time() - start_time:.1f}s, Total: {len(measurements)}")
                print("-" * 40)

            # Wait for next measurement
            time.sleep(update_interval)

    except Exception as e:
        print(f"\n❌ Error during measurement: {e}")

    finally:
        # Display final statistics
        if measurements:
            print(f"\n📈 FINAL STATISTICS:")
            print(f"   Total measurements: {len(measurements)}")
            print(
                f"   Session duration: {time.time() - start_time:.1f} seconds")
            if measurements:
                print(
                    f"   Final average: {sum(measurements) / len(measurements):.2f} cm")


def main():
    """Main function to run HC-SR04 distance measurement"""
    print("HC-SR04 Distance Sensor Starting...")

    try:
        # Get appropriate GPIO module
        gpio, h = get_gpio()

        if gpio is None and not USE_MOCK_GPIO:
            print("❌ Cannot proceed without GPIO. Please:")
            print("   1. Install lgpio: pip install lgpio")
            print("   2. Or install RPi.GPIO: pip install RPi.GPIO")
            print("   3. Or set USE_MOCK_GPIO = True in config.py")
            return

        # Run continuous measurement
        continuous_measurement(gpio, h, UPDATE_INTERVAL)

    except Exception as e:
        print(f"Fatal error: {e}")

    finally:
        # Cleanup GPIO
        if gpio and not USE_MOCK_GPIO:
            try:
                if gpio.__name__ == 'lgpio' and h is not None:
                    lgpio.gpiochip_close(h)
                    print("lgpio cleanup completed")
                else:
                    gpio.cleanup()
                    print("GPIO cleanup completed")
            except Exception as e:
                print(f"Cleanup error: {e}")

        print("\n✅ HC-SR04 measurement completed!")


if __name__ == "__main__":
    main()
