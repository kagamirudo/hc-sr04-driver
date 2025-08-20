#!/usr/bin/env python3
"""
Setup script for HC-SR04 Ultrasonic Sensor Driver
A professional Python driver for HC-SR04 ultrasonic distance sensors on Raspberry Pi
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hc-sr04-driver",
    version="1.0.0",
    author="Gary Pham",
    author_email="hoangvuph03@gmail.com",
    description="Professional HC-SR04 ultrasonic sensor driver for Raspberry Pi",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/kagamirudo/hc-sr04-driver",
    project_urls={
        "Bug Reports": "https://github.com/kagamirudo/hc-sr04-driver/issues",
        "Source": "https://github.com/kagamirudo/hc-sr04-driver",
        "Documentation": "https://github.com/kagamirudo/hc-sr04-driver#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "hc-sr04=sensor_hcsr04_lgpio:main",
            "hc-sr04-test=test_hcsr04:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="raspberry-pi, gpio, ultrasonic, sensor, distance, hc-sr04, lgpio",
)
