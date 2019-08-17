"""
Handles the propulsion system when having
two motors
"""

import RPi.GPIO as GPIO

class Propulsion2Motors:

    def __init__(self, in_pin_1_motor_1, in_pin_2_motor_1, in_pin_1_motor_2, in_pin_2_motor_2):

        self._pin_enabled =[False for i in range(4)]

        if in_pin_1_motor_1 is not None:
            GPIO.setup(in_pin_1_motor_1, GPIO.OUT)
            self._pin_enabled[0] = (True, in_pin_1_motor_1)

        if in_pin_2_motor_1 is not None:
            GPIO.setup(in_pin_2_motor_1, GPIO.OUT)
            self._pin_enabled[1] = (True, in_pin_2_motor_1)

        if in_pin_1_motor_2 is not None:
            GPIO.setup(in_pin_1_motor_2, GPIO.OUT)
            self._pin_enabled[2] = (True, in_pin_1_motor_2)

        if in_pin_2_motor_2 is not None:
            GPIO.setup(in_pin_2_motor_2, GPIO.OUT)
            self._pin_enabled[3] = (True, in_pin_2_motor_2)


    def forward(self, speed):

        if self._pin_enabled[0] !=False and self._pin_enabled[1][0]:
            GPIO.output(self._pin_enabled[0][1], True)

        if self._pin_enabled[1] !=False and self._pin_enabled[1][0]:
            GPIO.output(self._pin_enabled[1][1], False)

        if self._pin_enabled[2] != False and self._pin_enabled[2][0]:
            GPIO.output(self._pin_enabled[2][1], True)

        if self._pin_enabled[3]!= False and self._pin_enabled[3][0]:
            GPIO.output(self._pin_enabled[3][1], False)

    def backward(self, speed):

        if self._pin_enabled[0] !=False and self._pin_enabled[0][0]:
            GPIO.output(self._pin_enabled[0][1], False)

        if self._pin_enabled[1] !=False and self._pin_enabled[1][0]:
            GPIO.output(self._pin_enabled[1][1], True)

        if self._pin_enabled[2] != False and self._pin_enabled[2][0]:
            GPIO.output(self._pin_enabled[2][1], False)

        if self._pin_enabled[3]!= False and self._pin_enabled[3][0]:
            GPIO.output(self._pin_enabled[3][1], True)


    def stop(self):

        if self._pin_enabled[0] !=False and self._pin_enabled[1][0]:
            GPIO.output(self._pin_enabled[0][1], False)

        if self._pin_enabled[1] !=False and self._pin_enabled[1][0]:
            GPIO.output(self._pin_enabled[1][1], False)

        if self._pin_enabled[2] != False and self._pin_enabled[2][0]:
            GPIO.output(self._pin_enabled[2][1], False)

        if self._pin_enabled[3]!= False and self._pin_enabled[3][0]:
            GPIO.output(self._pin_enabled[3][1], False)




