"""
Handles the propulsion system when having
two motors
"""
from config.config import ENABLE_WARNINGS
from config.config import ON_RASP_PI

if ON_RASP_PI:
    import RPi.GPIO as GPIO
else:
    from mocks.gpio_mock import GPIOMock as GPIO


class PropulsionParams:

    def __init__(self, in_pin_1_motor_1, in_pin_2_motor_1, en_pin_motor_1,
                 in_pin_1_motor_2, in_pin_2_motor_2, en_pin_motor_2):
        self.in_pin_1_motor_1 = in_pin_1_motor_1
        self.in_pin_2_motor_1 = in_pin_2_motor_1
        self.en_pin_motor_1 = en_pin_motor_1

        self.in_pin_1_motor_2 = in_pin_1_motor_2
        self.in_pin_2_motor_2 = in_pin_2_motor_2
        self.en_pin_motor_2 = en_pin_motor_2


class Propulsion:

    def __init__(self, params):

        self.__params = params

        if self.__params.in_pin_1_motor_1 is not None and \
           self.__params.in_pin_2_motor_1 is not None and \
           self.__params.en_pin_motor_1 is not None:

            print("Set up PIN_1_MOTOR_1 at: ", self.__params.in_pin_1_motor_1)
            print("Set up PIN_2_MOTOR_1 at: ", self.__params.in_pin_2_motor_1)
            print("Set up PIN_EN_MOTOR_1 at: ", self.__params.en_pin_motor_1)

            #if ON_RASP_PI:
            GPIO.setup(self.__params.in_pin_1_motor_1, GPIO.OUT)
            GPIO.setup(self.__params.in_pin_2_motor_1, GPIO.OUT)
            GPIO.setup(self.__params.en_pin_motor_1,   GPIO.OUT)

        elif ENABLE_WARNINGS:
            print(" Either of the pins for motor 1 is None ")

        if self.__params.in_pin_1_motor_2 is not None and \
           self.__params.in_pin_2_motor_2 is not None and \
           self.__params.en_pin_motor_2 is not None:

            print("Set up PIN_1_MOTOR_2 at: ", self.__params.in_pin_1_motor_2)
            print("Set up PIN_2_MOTOR_2 at: ", self.__params.in_pin_2_motor_2)
            print("Set up PIN_EN_MOTOR_2 at: ", self.__params.en_pin_motor_2)

            #if ON_RASP_PI:
            GPIO.setup(self.__params.in_pin_1_motor_2, GPIO.OUT)
            GPIO.setup(self.__params.in_pin_2_motor_2, GPIO.OUT)
            GPIO.setup(self.__params.en_pin_motor_2,   GPIO.OUT)

        elif ENABLE_WARNINGS:
            print(" Either of the pins for motor 2 is None ")

    def forward(self, speed):

        # clapm the max speed to 100 as this is
        # the max dutty speed
        if(speed > 100):
            speed = 100

        #if ON_RASP_PI:
        p1 = GPIO.PWM(self.__params.en_pin_motor_1 , 1000)
        p1.start(speed)

        GPIO.output(self.__params.in_pin_1_motor_1, GPIO.HIGH)
        GPIO.output(self.__params.in_pin_2_motor_1, GPIO.LOW)

        p2 = GPIO.PWM(self.__params.en_pin_motor_2, 1000)
        p2.start(speed)
        GPIO.output(self.__params.in_pin_1_motor_2, GPIO.HIGH)
        GPIO.output(self.__params.in_pin_2_motor_2, GPIO.LOW)


    def backward(self, speed):

        #if ON_RASP_PI:
        p1 = GPIO.PWM(self.__params.en_pin_motor_1, 1000)
        p1.start(speed)

        GPIO.output(self.__params.in_pin_1_motor_1, GPIO.LOW)
        GPIO.output(self.__params.in_pin_2_motor_1, GPIO.HIGH)

        p2 = GPIO.PWM(self.__params.en_pin_motor_2, 1000)
        p2.start(speed)
        GPIO.output(self.__params.in_pin_1_motor_2, GPIO.LOW)
        GPIO.output(self.__params.in_pin_2_motor_2, GPIO.HIGH)

    def left(self, speed):
        pass

    def right(self, speed):
        pass

    def stop(self):

        #if ON_RASP_PI:
        GPIO.output(self.__params.in_pin_1_motor_1, GPIO.LOW)
        GPIO.output(self.__params.in_pin_2_motor_1, GPIO.LOW)
        GPIO.output(self.__params.in_pin_1_motor_2, GPIO.LOW)
        GPIO.output(self.__params.in_pin_2_motor_2, GPIO.LOW)




