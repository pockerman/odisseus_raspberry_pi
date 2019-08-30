"""
Handles the propulsion system when having
two motors
"""

import RPi.GPIO as GPIO
from config import ENABLE_WARNINGS

class Propulsion2Motors:

    def __init__(self, in_pin_1_motor_1, in_pin_2_motor_1, en_pin_motor_1,
                 in_pin_1_motor_2, in_pin_2_motor_2, en_pin_motor_2):

        self.__in_pin_1_motor_1 = in_pin_1_motor_1
        self.__in_pin_2_motor_1 = in_pin_2_motor_1
        self.__en_pin_motor_1  = en_pin_motor_1

        self.__in_pin_1_motor_2 = in_pin_1_motor_2
        self.__in_pin_2_motor_2 = in_pin_2_motor_2
        self.__en_pin_motor_2 = en_pin_motor_2


        if self.__in_pin_1_motor_1 is not None and \
           self.__in_pin_2_motor_1 is not None and \
           self.__en_pin_motor_1 is not None:

            print("Set up PIN_1_MOTOR_1 at: ", in_pin_1_motor_1)
            print("Set up PIN_2_MOTOR_1 at: ", in_pin_2_motor_1)

            GPIO.setup(self.__in_pin_1_motor_1, GPIO.OUT)
            GPIO.setup(self.__in_pin_2_motor_1, GPIO.OUT)
            GPIO.setup(self.__en_pin_motor_1,   GPIO.OUT)
        elif ENABLE_WARNINGS:
            print(" Either of the pins for motor 1 is None ")

        if self.__in_pin_1_motor_2 is not None and \
           self.__in_pin_2_motor_2 is not None and \
           self.__en_pin_motor_2 is not None:

            print("Set up PIN_1_MOTOR_2 at: ",  self.__in_pin_1_motor_2)
            print("Set up PIN_2_MOTOR_2 at: ",  self.__in_pin_2_motor_2)

            GPIO.setup(self.__in_pin_1_motor_2, GPIO.OUT)
            GPIO.setup(self.__in_pin_2_motor_2, GPIO.OUT)
            GPIO.setup(self.__en_pin_motor_2,   GPIO.OUT)
        elif ENABLE_WARNINGS:
            print(" Either of the pins for motor 2 is None ")

    def forward(self, speed):

        # clapm the max speed to 100 as this is
        # the max dutty speed
        if(speed > 100):
            speed = 100

        p1 = GPIO.PWM(self.__en_pin_motor_1 , 1000)
        p1.start(speed)

        GPIO.output(self.__in_pin_1_motor_1, GPIO.HIGH)
        GPIO.output(self.__in_pin_2_motor_1, GPIO.LOW)

        p2 = GPIO.PWM(self.__en_pin_motor_2, 1000)
        p2.start(speed)
        GPIO.output(self.__in_pin_1_motor_2, GPIO.HIGH)
        GPIO.output(self.__in_pin_2_motor_2, GPIO.LOW)

    def backward(self, speed):

        p1 = GPIO.PWM(self.__en_pin_motor_1, 1000)
        p1.start(speed)

        GPIO.output(self.__in_pin_1_motor_1, GPIO.LOw)
        GPIO.output(self.__in_pin_2_motor_1, GPIO.HIGH)

        p2 = GPIO.PWM(self.__en_pin_motor_2, 1000)
        p2.start(speed)
        GPIO.output(self.__in_pin_1_motor_2, GPIO.LOw)
        GPIO.output(self.__in_pin_2_motor_2, GPIO.HIGH)

    def stop(self):

        GPIO.output(self.__in_pin_1_motor_1, GPIO.LOw)
        GPIO.output(self.__in_pin_2_motor_1, GPIO.LOW)
        GPIO.output(self.__in_pin_1_motor_2, GPIO.LOW)
        GPIO.output(self.__in_pin_2_motor_2, GPIO.LOW)




