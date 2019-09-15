"""
Handles the propulsion system when having
two motors
"""
import time


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

    def __init__(self, odisseus_config, params):
        self._odisseus_config = odisseus_config
        self._params = params
        self.setup()

    def get_parameters(self):
        return self._params

    def setup(self):
        """
        Set up the pins using the parameters
        """
        if self._odisseus_config.ON_RASP_PI:
            import RPi.GPIO as GPIO
            self._GPIO = GPIO
        else:
            from gpio_mock import GPIOMock as GPIO
            self._GPIO = GPIO

        if self._params.in_pin_1_motor_1 is not None and \
                self._params.in_pin_2_motor_1 is not None and \
                self._params.en_pin_motor_1 is not None:

            print("Set up PIN_1_MOTOR_1 at: ", self._params.in_pin_1_motor_1)
            print("Set up PIN_2_MOTOR_1 at: ", self._params.in_pin_2_motor_1)
            print("Set up PIN_EN_MOTOR_1 at: ", self._params.en_pin_motor_1)

            self._GPIO.setup(self._params.in_pin_1_motor_1, self._GPIO.OUT)
            self._GPIO.setup(self._params.in_pin_2_motor_1, self._GPIO.OUT)
            self._GPIO.setup(self._params.en_pin_motor_1, self._GPIO.OUT)

        elif self._odisseus_config.ENABLE_WARNINGS:
            print(" Either of the pins for motor 1 is None ")

        if self._params.in_pin_1_motor_2 is not None and \
                self._params.in_pin_2_motor_2 is not None and \
                self._params.en_pin_motor_2 is not None:

            print("Set up PIN_1_MOTOR_2 at: ", self._params.in_pin_1_motor_2)
            print("Set up PIN_2_MOTOR_2 at: ", self._params.in_pin_2_motor_2)
            print("Set up PIN_EN_MOTOR_2 at: ", self._params.en_pin_motor_2)

            # GPIO.setup(self.__params.in_pin_1_motor_2, GPIO.OUT)
            # GPIO.setup(self.__params.in_pin_2_motor_2, GPIO.OUT)
            # GPIO.setup(self.__params.en_pin_motor_2,   GPIO.OUT)

        elif self._odisseus_config.ENABLE_WARNINGS:
            print(" Either of the pins for motor 2 is None ")


    def forward(self, speed, **kwargs):

        # clamp the max speed to 100 as this is the max dutty speed
        if speed > 100:
            speed = 100

        p1 = self._GPIO.PWM(self._params.en_pin_motor_1 , 1000)
        p1.start(speed)

        self._GPIO.output(self._params.in_pin_1_motor_1, self._GPIO.HIGH)
        self._GPIO.output(self._params.in_pin_2_motor_1, self._GPIO.LOW)

        #p2 = GPIO.PWM(self.__params.en_pin_motor_2, 1000)
        #p2.start(speed)
        #GPIO.output(self.__params.in_pin_1_motor_2, GPIO.HIGH)
        #GPIO.output(self.__params.in_pin_2_motor_2, GPIO.LOW)

        time.sleep(kwargs['time'])

    def backward(self, speed, **kwargs):

        # clamp the max speed to 100 as this is the max dutty speed
        if speed > 100:
            speed = 100

        p1 = self._GPIO.PWM(self._params.en_pin_motor_1, 1000)
        p1.start(speed)

        self._GPIO.output(self._params.in_pin_1_motor_1, self._GPIO.LOW)
        self._GPIO.output(self._params.in_pin_2_motor_1, self._GPIO.HIGH)

        #p2 = GPIO.PWM(self.__params.en_pin_motor_2, 1000)
        #p2.start(speed)
        #GPIO.output(self.__params.in_pin_1_motor_2, GPIO.LOW)
        #GPIO.output(self.__params.in_pin_2_motor_2, GPIO.HIGH)

        time.sleep(kwargs['time'])

    def left(self, speed, **kwargs):
        time.sleep(kwargs['time'])
        pass

    def right(self, speed, **kwargs):
        time.sleep(kwargs['time'])
        pass

    def stop(self):

        self._GPIO.output(self._params.in_pin_1_motor_1, self._GPIO.LOW)
        self._GPIO.output(self._params.in_pin_2_motor_1, self._GPIO.LOW)
        #GPIO.output(self.__params.in_pin_1_motor_2, GPIO.LOW)
        #GPIO.output(self.__params.in_pin_2_motor_2, GPIO.LOW)
        #time.sleep(kwargs['time'])




