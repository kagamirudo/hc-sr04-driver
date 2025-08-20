#!/usr/bin/env python3
"""
HC-SR04 Ultrasonic Sensor Driver Package

A professional Python driver for HC-SR04 ultrasonic distance sensors on Raspberry Pi.
Supports both lgpio (recommended for Pi 5) and RPi.GPIO (fallback) libraries.

Features:
- Real-time distance monitoring
- Configurable update intervals
- Automatic library detection
- Comprehensive error handling
- Distance range validation (0.5-400cm)
- Statistics and logging
- Mock mode for development

Author: Gary Pham
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Gary Pham"
__email__ = "hoangvuph03@gmail.com"
__license__ = "MIT"
__url__ = "https://github.com/kagamirudo/hc-sr04-driver"

# Import main classes and functions
from .sensor import HCSR04Sensor
from .config import HCSR04Config

# Make main classes available at package level
__all__ = [
    "HCSR04Sensor",
    "HCSR04Config",
    "__version__",
    "__author__",
    "__license__",
]
