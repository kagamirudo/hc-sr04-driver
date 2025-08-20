#!/usr/bin/env python3
"""
Configuration module for HC-SR04 Ultrasonic Sensor Driver
"""

import os
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class HCSR04Config:
    """
    Configuration class for HC-SR04 ultrasonic sensor
    
    Attributes:
        trig_pin: GPIO pin for trigger signal
        echo_pin: GPIO pin for echo signal
        settle_time: Time to wait for sensor to settle (seconds)
        pulse_duration: Duration of trigger pulse (seconds)
        echo_timeout: Timeout for echo response (seconds)
        update_interval: Interval between measurements (seconds)
        sound_speed: Speed of sound in cm/s
        min_distance: Minimum reliable distance (cm)
        max_distance: Maximum reliable distance (cm)
        use_mock_gpio: Whether to use mock GPIO mode
        mock_min_distance: Minimum mock distance (cm)
        mock_max_distance: Maximum mock distance (cm)
        distance_thresholds: Distance thresholds for status indicators
    """
    
    # GPIO pin configuration
    trig_pin: int = 23
    echo_pin: int = 24
    
    # Sensor timing settings
    settle_time: float = 0.1
    pulse_duration: float = 0.00001  # 10 microseconds
    echo_timeout: float = 0.1
    
    # Update settings
    update_interval: float = 1.0
    
    # Distance calculation constants
    sound_speed: float = 34300  # cm/s at 20°C
    round_trip_divisor: int = 2
    
    # Distance range
    min_distance: float = 0.5
    max_distance: float = 400.0
    
    # Mock mode settings
    use_mock_gpio: bool = False
    mock_min_distance: float = 10.0
    mock_max_distance: float = 200.0
    
    # Distance thresholds for status indicators (cm)
    distance_thresholds: Dict[str, float] = None
    
    def __post_init__(self):
        """Set default distance thresholds if not provided"""
        if self.distance_thresholds is None:
            self.distance_thresholds = {
                'very_close': 5.0,
                'close': 30.0,
                'medium': 100.0,
                'far': 200.0
            }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'HCSR04Config':
        """Create configuration from dictionary"""
        return cls(**config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'trig_pin': self.trig_pin,
            'echo_pin': self.echo_pin,
            'settle_time': self.settle_time,
            'pulse_duration': self.pulse_duration,
            'echo_timeout': self.echo_timeout,
            'update_interval': self.update_interval,
            'sound_speed': self.sound_speed,
            'round_trip_divisor': self.round_trip_divisor,
            'min_distance': self.min_distance,
            'max_distance': self.max_distance,
            'use_mock_gpio': self.use_mock_gpio,
            'mock_min_distance': self.mock_min_distance,
            'mock_max_distance': self.mock_max_distance,
            'distance_thresholds': self.distance_thresholds.copy()
        }
    
    def validate(self) -> bool:
        """Validate configuration parameters"""
        if self.min_distance < 0:
            raise ValueError("min_distance must be positive")
        if self.max_distance <= self.min_distance:
            raise ValueError("max_distance must be greater than min_distance")
        if self.settle_time < 0:
            raise ValueError("settle_time must be positive")
        if self.pulse_duration < 0:
            raise ValueError("pulse_duration must be positive")
        if self.echo_timeout < 0:
            raise ValueError("echo_timeout must be positive")
        if self.update_interval < 0:
            raise ValueError("update_interval must be positive")
        if self.sound_speed <= 0:
            raise ValueError("sound_speed must be positive")
        return True


# Default configuration instance
DEFAULT_CONFIG = HCSR04Config()
