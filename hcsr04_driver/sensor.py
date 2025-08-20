#!/usr/bin/env python3
"""
HC-SR04 Ultrasonic Sensor Driver

A professional, production-ready driver for the HC-SR04 ultrasonic distance sensor.
Supports both lgpio (recommended for Pi 5) and RPi.GPIO libraries.
"""

import time
import threading
import random
from typing import Optional, Callable, List

# Handle both package and standalone execution
try:
    from .config import HCSR04Config, DEFAULT_CONFIG
except ImportError:
    # Standalone execution
    from config import HCSR04Config, DEFAULT_CONFIG


class MockGPIO:
    """Mock GPIO class for development and testing"""

    OUT = "OUT"
    IN = "IN"
    BCM = "BCM"

    @staticmethod
    def setmode(mode):
        pass

    @staticmethod
    def setup(pin, direction):
        pass

    @staticmethod
    def output(pin, value):
        pass

    @staticmethod
    def input(pin):
        return random.choice([0, 1])

    @staticmethod
    def cleanup():
        pass


class HCSR04Sensor:
    """
    Professional HC-SR04 ultrasonic sensor driver

    Features:
    - Automatic GPIO library detection (lgpio recommended for Pi 5)
    - Real-time distance monitoring
    - Configurable parameters
    - Comprehensive error handling
    - Statistics tracking
    - Mock mode support
    """

    def __init__(self, config: Optional[HCSR04Config] = None):
        """
        Initialize HC-SR04 sensor

        Args:
            config: Configuration object (uses default if None)
        """
        self.config = config or DEFAULT_CONFIG
        self.config.validate()

        self.gpio = None
        self.gpio_handle = None
        self.gpio_library = None
        self.running = False
        self.measurements: List[float] = []
        self.start_time = None

        # Setup GPIO
        self._setup_gpio()

    def _setup_gpio(self):
        """Setup GPIO library and pins"""
        if self.config.use_mock_gpio:
            self.gpio = MockGPIO()
            self.gpio_library = "mock"
            print("Using MOCK GPIO mode (development/testing)")
            return

        # Try lgpio first (recommended for Pi 5)
        try:
            import lgpio
            self.gpio = lgpio
            self.gpio_library = "lgpio"
            self.gpio_handle = lgpio.gpiochip_open(0)
            print("Using lgpio library (recommended for Raspberry Pi 5)")
        except ImportError:
            # Fallback to RPi.GPIO
            try:
                import RPi.GPIO as GPIO
                self.gpio = GPIO
                self.gpio_library = "RPi.GPIO"
                print("Using RPi.GPIO library (fallback option)")
            except ImportError:
                print(
                    "Error: No GPIO library available. Please install lgpio or RPi.GPIO")
                print("Falling back to mock mode")
                self.gpio = MockGPIO()
                self.gpio_library = "mock"

    def measure_distance(self) -> Optional[float]:
        """
        Measure distance using HC-SR04 sensor

        Returns:
            Distance in centimeters, or None if measurement failed
        """
        if self.gpio_library == "mock":
            return self._measure_distance_mock()
        elif self.gpio_library == "lgpio":
            return self._measure_distance_lgpio()
        elif self.gpio_library == "RPi.GPIO":
            return self._measure_distance_rpi_gpio()
        else:
            return None

    def _measure_distance_mock(self) -> float:
        """Mock distance measurement for testing"""
        time.sleep(0.1)
        distance = random.uniform(
            self.config.mock_min_distance,
            self.config.mock_max_distance
        )
        return round(distance, 2)

    def _measure_distance_lgpio(self) -> Optional[float]:
        """Measure distance using lgpio library"""
        try:
            # Setup GPIO pins
            self.gpio.gpio_claim_output(self.gpio_handle, self.config.trig_pin)
            self.gpio.gpio_claim_input(self.gpio_handle, self.config.echo_pin)

            # Ensure trigger pin is low initially
            self.gpio.gpio_write(self.gpio_handle, self.config.trig_pin, 0)
            time.sleep(self.config.settle_time)

            # Send trigger pulse
            self.gpio.gpio_write(self.gpio_handle, self.config.trig_pin, 1)
            time.sleep(self.config.pulse_duration)
            self.gpio.gpio_write(self.gpio_handle, self.config.trig_pin, 0)

            # Wait for echo start
            timeout_start = time.time()
            while self.gpio.gpio_read(self.gpio_handle, self.config.echo_pin) == 0:
                if time.time() - timeout_start > self.config.echo_timeout:
                    return None
                pulse_start = time.time()

            # Wait for echo end
            timeout_start = time.time()
            while self.gpio.gpio_read(self.gpio_handle, self.config.echo_pin) == 1:
                if time.time() - timeout_start > self.config.echo_timeout:
                    return None
                pulse_end = time.time()

            # Calculate distance
            pulse_duration = pulse_end - pulse_start
            distance = (pulse_duration * self.config.sound_speed) / \
                self.config.round_trip_divisor

            # Validate range
            if distance < self.config.min_distance or distance > self.config.max_distance:
                return None

            return round(distance, 2)

        except Exception as e:
            print(f"Error during lgpio measurement: {e}")
            return None

    def _measure_distance_rpi_gpio(self) -> Optional[float]:
        """Measure distance using RPi.GPIO library"""
        try:
            # Setup GPIO pins
            self.gpio.setup(self.config.trig_pin, self.gpio.OUT)
            self.gpio.setup(self.config.echo_pin, self.gpio.IN)

            # Ensure trigger pin is low initially
            self.gpio.output(self.config.trig_pin, False)
            time.sleep(self.config.settle_time)

            # Send trigger pulse
            self.gpio.output(self.config.trig_pin, True)
            time.sleep(self.config.pulse_duration)
            self.gpio.output(self.config.trig_pin, False)

            # Wait for echo start
            timeout_start = time.time()
            while self.gpio.input(self.config.echo_pin) == 0:
                if time.time() - timeout_start > self.config.echo_timeout:
                    return None
                pulse_start = time.time()

            # Wait for echo end
            timeout_start = time.time()
            while self.gpio.input(self.config.echo_pin) == 1:
                if time.time() - timeout_start > self.config.echo_timeout:
                    return None
                pulse_end = time.time()

            # Calculate distance
            pulse_duration = pulse_end - pulse_start
            distance = (pulse_duration * self.config.sound_speed) / \
                self.config.round_trip_divisor

            # Validate range
            if distance < self.config.min_distance or distance > self.config.max_distance:
                return None

            return round(distance, 2)

        except Exception as e:
            print(f"Error during RPi.GPIO measurement: {e}")
            return None

    def get_distance_status(self, distance: float) -> str:
        """Get status indicator for distance"""
        if distance < 1.0:
            return "🔴 Extremely Close"
        elif distance < self.config.distance_thresholds['very_close']:
            return "🟢 Very Close"
        elif distance < self.config.distance_thresholds['close']:
            return "🟢 Close"
        elif distance < self.config.distance_thresholds['medium']:
            return "🟡 Medium"
        elif distance < self.config.distance_thresholds['far']:
            return "🟠 Far"
        else:
            return "🔴 Very Far"

    def get_statistics(self) -> dict:
        """Get measurement statistics"""
        if not self.measurements:
            return {}

        return {
            'count': len(self.measurements),
            'average': sum(self.measurements) / len(self.measurements),
            'minimum': min(self.measurements),
            'maximum': max(self.measurements),
            'range': max(self.measurements) - min(self.measurements),
            'duration': time.time() - self.start_time if self.start_time else 0
        }

    def start_monitoring(self, callback: Optional[Callable[[float, str], None]] = None):
        """Start continuous distance monitoring"""
        self.running = True
        self.start_time = time.time()
        self.measurements.clear()

        print("=" * 60)
        print("           HC-SR04 REAL-TIME DISTANCE SENSOR")
        print("=" * 60)
        print(f"GPIO Library: {self.gpio_library}")
        print(f"Update Interval: {self.config.update_interval} seconds")
        print(
            f"Trigger Pin: {self.config.trig_pin}, Echo Pin: {self.config.echo_pin}")
        print(
            f"Valid Range: {self.config.min_distance}-{self.config.max_distance} cm")
        print("Press Ctrl+C to stop")
        print("=" * 60)

        try:
            while self.running:
                distance = self.measure_distance()

                if distance is not None:
                    self.measurements.append(distance)
                    if len(self.measurements) > 100:
                        self.measurements.pop(0)

                    status = self.get_distance_status(distance)
                    timestamp = time.strftime("%H:%M:%S")

                    if callback:
                        callback(distance, status)
                    else:
                        print(
                            f"[{timestamp}] Distance: {distance:6.2f} cm {status}")

                    # Show statistics every 5 measurements
                    if len(self.measurements) % 5 == 0 and len(self.measurements) > 0:
                        stats = self.get_statistics()
                        print(
                            f"    Stats: Avg={stats['average']:5.1f}, Min={stats['minimum']:5.1f}, Max={stats['maximum']:5.1f} cm")
                        print(
                            f"    Running for: {stats['duration']:.1f}s, Total: {stats['count']}")
                        print("-" * 40)

                time.sleep(self.config.update_interval)

        except KeyboardInterrupt:
            print("\n" + "=" * 50)
            print("Monitoring stopped by user")
        finally:
            self._show_final_statistics()

    def _show_final_statistics(self):
        """Display final statistics"""
        if self.measurements:
            stats = self.get_statistics()
            print(f"\n📈 FINAL STATISTICS:")
            print(f"   Total measurements: {stats['count']}")
            print(f"   Session duration: {stats['duration']:.1f} seconds")
            print(f"   Final average: {stats['average']:.2f} cm")

    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.running = False

    def cleanup(self):
        """Cleanup GPIO resources"""
        if self.gpio_library == "lgpio" and self.gpio_handle:
            try:
                self.gpio.gpiochip_close(self.gpio_handle)
                print("lgpio cleanup completed")
            except:
                pass
        elif self.gpio_library == "RPi.GPIO":
            try:
                self.gpio.cleanup()
                print("GPIO cleanup completed")
            except:
                pass
        elif self.gpio_library == "mock":
            print("Mock GPIO cleanup completed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()


def main():
    """Main function for command-line usage"""
    sensor = HCSR04Sensor()
    try:
        sensor.start_monitoring()
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        sensor.cleanup()


if __name__ == "__main__":
    main()
