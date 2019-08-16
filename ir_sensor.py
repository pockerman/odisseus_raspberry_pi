"""
The IR sensor
"""

import RPi.GPIO as GPIO


class IRSensor:

    def __init__(self, pin_id):
        GPIO.setup(pin_id, GPIO.IN)
