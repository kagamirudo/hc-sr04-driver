#!/usr/bin/env python3
"""
Examples for using the HC-SR04 Ultrasonic Sensor Driver

This module demonstrates various ways to use the sensor driver:
1. Basic usage
2. Custom configuration
3. Callback-based monitoring
4. Context manager usage
5. Advanced configuration
"""

# Handle both package and standalone execution
try:
    from .sensor import HCSR04Sensor
    from .config import HCSR04Config
except ImportError:
    # Standalone execution
    from sensor import HCSR04Sensor
    from config import HCSR04Config


def basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===")
    
    # Create sensor with default configuration
    sensor = HCSR04Sensor()
    
    # Single measurement
    distance = sensor.measure_distance()
    if distance:
        print(f"Distance: {distance} cm")
    else:
        print("Measurement failed")
    
    # Cleanup
    sensor.cleanup()


def custom_configuration():
    """Custom configuration example"""
    print("\n=== Custom Configuration Example ===")
    
    # Create custom configuration
    config = HCSR04Config(
        trig_pin=17,           # Different GPIO pin
        echo_pin=27,           # Different GPIO pin
        update_interval=0.5,   # Faster updates
        min_distance=1.0,      # Custom minimum distance
        max_distance=300.0,    # Custom maximum distance
        use_mock_gpio=True     # Use mock mode for testing
    )
    
    # Create sensor with custom config
    sensor = HCSR04Sensor(config)
    
    # Take a few measurements
    for i in range(3):
        distance = sensor.measure_distance()
        if distance:
            print(f"Measurement {i+1}: {distance} cm")
        else:
            print(f"Measurement {i+1}: Failed")
    
    sensor.cleanup()


def callback_monitoring():
    """Callback-based monitoring example"""
    print("\n=== Callback Monitoring Example ===")
    
    def distance_callback(distance: float, status: str):
        """Custom callback function"""
        print(f"📏 {distance:6.2f} cm - {status}")
    
    # Create sensor and start monitoring with callback
    sensor = HCSR04Sensor()
    
    try:
        # Start monitoring with custom callback
        sensor.start_monitoring(callback=distance_callback)
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
    finally:
        sensor.cleanup()


def context_manager_usage():
    """Context manager usage example"""
    print("\n=== Context Manager Example ===")
    
    # Use context manager for automatic cleanup
    with HCSR04Sensor() as sensor:
        # Take a few measurements
        for i in range(3):
            distance = sensor.measure_distance()
            if distance:
                print(f"Measurement {i+1}: {distance} cm")
            else:
                print(f"Measurement {i+1}: Failed")
    
    # GPIO is automatically cleaned up


def advanced_configuration():
    """Advanced configuration example"""
    print("\n=== Advanced Configuration Example ===")
    
    # Create advanced configuration
    config = HCSR04Config(
        trig_pin=23,
        echo_pin=24,
        settle_time=0.05,      # Faster settling
        pulse_duration=0.00001, # 10 microseconds
        echo_timeout=0.05,     # Faster timeout
        update_interval=0.2,   # Very fast updates
        sound_speed=34300,     # Speed of sound at 20°C
        min_distance=0.5,      # Very close detection
        max_distance=400.0,    # Maximum range
        distance_thresholds={
            'very_close': 2.0,   # Custom thresholds
            'close': 20.0,
            'medium': 80.0,
            'far': 150.0
        }
    )
    
    # Create sensor with advanced config
    sensor = HCSR04Sensor(config)
    
    # Take measurements
    for i in range(5):
        distance = sensor.measure_distance()
        if distance:
            status = sensor.get_distance_status(distance)
            print(f"Measurement {i+1}: {distance:6.2f} cm - {status}")
        else:
            print(f"Measurement {i+1}: Failed")
    
    sensor.cleanup()


def statistics_example():
    """Statistics tracking example"""
    print("\n=== Statistics Example ===")
    
    sensor = HCSR04Sensor()
    
    # Take several measurements
    measurements = []
    for i in range(10):
        distance = sensor.measure_distance()
        if distance:
            measurements.append(distance)
            print(f"Measurement {i+1}: {distance} cm")
        else:
            print(f"Measurement {i+1}: Failed")
    
    # Get statistics
    if measurements:
        stats = sensor.get_statistics()
        print(f"\n📊 Statistics:")
        print(f"   Count: {stats['count']}")
        print(f"   Average: {stats['average']:.2f} cm")
        print(f"   Minimum: {stats['minimum']:.2f} cm")
        print(f"   Maximum: {stats['maximum']:.2f} cm")
        print(f"   Range: {stats['range']:.2f} cm")
    
    sensor.cleanup()


def run_all_examples():
    """Run all examples"""
    print("HC-SR04 Driver Examples")
    print("=" * 50)
    
    try:
        basic_usage()
        custom_configuration()
        callback_monitoring()
        context_manager_usage()
        advanced_configuration()
        statistics_example()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")


if __name__ == "__main__":
    run_all_examples()
