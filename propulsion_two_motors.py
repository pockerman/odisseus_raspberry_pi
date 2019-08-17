"""
Handles the propulsion system when having
two motors
"""

import RPi.GPIO as GPIO

class Propulsion2Motors:

    def __init__(self, in_pin_1_motor_1, in_pin_2_motor_1, en_pin_motor_1,
                 in_pin_1_motor_2, in_pin_2_motor_2):

        self._pin_enabled =[False for i in range(4)]

        if in_pin_1_motor_1 is not None:
            GPIO.setup(in_pin_1_motor_1, GPIO.OUT)
            self._pin_enabled[0] = (True, in_pin_1_motor_1)

        if in_pin_2_motor_1 is not None:
            GPIO.setup(in_pin_2_motor_1, GPIO.OUT)
            self._pin_enabled[1] = (True, in_pin_2_motor_1)

        GPIO.setup(en_pin_motor_1, GPIO.OUT)

        if in_pin_1_motor_2 is not None:
            GPIO.setup(in_pin_1_motor_2, GPIO.OUT)
            self._pin_enabled[2] = (True, in_pin_1_motor_2)

        if in_pin_2_motor_2 is not None:
            GPIO.setup(in_pin_2_motor_2, GPIO.OUT)
            self._pin_enabled[3] = (True, in_pin_2_motor_2)


    def forward(self, speed):

        if self._pin_enabled[0] !=False and self._pin_enabled[1][0]:
            GPIO.output(self._pin_enabled[0][1], GPIO.HIGH)

        if self._pin_enabled[1] !=False and self._pin_enabled[1][0]:
            GPIO.output(self._pin_enabled[1][1], GPIO.LOW)

        if self._pin_enabled[2] != False and self._pin_enabled[2][0]:
            GPIO.output(self._pin_enabled[2][1], GPIO.HIGH)

        if self._pin_enabled[3]!= False and self._pin_enabled[3][0]:
            GPIO.output(self._pin_enabled[3][1], GPIO.LOW)

    def backward(self, speed):

        if self._pin_enabled[0] !=False and self._pin_enabled[0][0]:
            GPIO.output(self._pin_enabled[0][1], GPIO.LOW)

        if self._pin_enabled[1] !=False and self._pin_enabled[1][0]:
            GPIO.output(self._pin_enabled[1][1], GPIO.HIGH)

        if self._pin_enabled[2] != False and self._pin_enabled[2][0]:
            GPIO.output(self._pin_enabled[2][1], GPIO.LOW)

        if self._pin_enabled[3]!= False and self._pin_enabled[3][0]:
            GPIO.output(self._pin_enabled[3][1], GPIO.HIGH)


    def stop(self):

        if self._pin_enabled[0] !=False and self._pin_enabled[1][0]:
            GPIO.output(self._pin_enabled[0][1], GPIO.LOW)

        if self._pin_enabled[1] !=False and self._pin_enabled[1][0]:
            GPIO.output(self._pin_enabled[1][1], GPIO.LOW)

        if self._pin_enabled[2] != False and self._pin_enabled[2][0]:
            GPIO.output(self._pin_enabled[2][1], GPIO.LOW)

        if self._pin_enabled[3]!= False and self._pin_enabled[3][0]:
            GPIO.output(self._pin_enabled[3][1], GPIO.LOW)




