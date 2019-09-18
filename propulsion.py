"""
Handles the propulsion system when having two motors
"""
import time


class PropulsionParams:

    """
    Assembles the PIN IDs for the propulsion
    """

    MOTOR_NAMES = ['FRONT_RIGHT', 'FRONT_LEFT']

    def __init__(self, in_pin_1_motor_1, in_pin_2_motor_1, en_pin_motor_1,
                 in_pin_1_motor_2, in_pin_2_motor_2, en_pin_motor_2):
        self.in_pin_1_motor_1 = in_pin_1_motor_1
        self.in_pin_2_motor_1 = in_pin_2_motor_1
        self.en_pin_motor_1 = en_pin_motor_1

        self.in_pin_1_motor_2 = in_pin_1_motor_2
        self.in_pin_2_motor_2 = in_pin_2_motor_2
        self.en_pin_motor_2 = en_pin_motor_2

    def get_motor_params(self, motor_name):

        """
           Returns the PIN IDs for the motor with the given name.
           Names supported are  ['FRONT_RIGHT', 'FRONT_LEFT']
        """

        if motor_name == 'FRONT_RIGHT':
            return self.in_pin_1_motor_1, self.in_pin_2_motor_1, self.en_pin_motor_1
        elif motor_name == 'FRONT_LEFT':
            return self.in_pin_1_motor_2, self.in_pin_2_motor_2, self.en_pin_motor_2

        raise ValueError("Motor name "+motor_name+" not in: "+str(PropulsionParams.MOTOR_NAMES))


class Motor:

    """
    Models a DC motor
    """

    def __init__(self, odisseus_config, name, params):

        self._odisseus_config = odisseus_config
        self._name = name
        self._params = params

        if self._odisseus_config.ON_RASP_PI:
            import RPi.GPIO as GPIO
            self._GPIO = GPIO
        else:
            from gpio_mock import GPIOMock as GPIO
            self._GPIO = GPIO

    def setup(self):

        """
        Set up the motor according to the parameters
        """

        if self._params[0] is not None and \
           self._params[1] is not None and \
           self._params[2] is not None:

            print("Set up motor: ", self._name)
            print("Set up PIN_1_MOTOR at: ", self._params[0])
            print("Set up PIN_2_MOTOR at: ", self._params[1])
            print("Set up PIN_EN_MOTOR at: ", self._params[2])

            self._GPIO.setup(self._params[0], self._GPIO.OUT)
            self._GPIO.setup(self._params[1], self._GPIO.OUT)
            self._GPIO.setup(self._params[2], self._GPIO.OUT)

        elif self._odisseus_config.ENABLE_WARNINGS:
            print(" Either of the pins for motor ", self._name, " is None ")

    def forward(self, **kwargs):

        """
        Set the PIN level such that forward motion is generated
        """

        p1 = self._GPIO.PWM(self._params[2], self._odisseus_config.MOTOR_PWM_FREQUENCY)
        self._GPIO.output(self._params[0], self._GPIO.HIGH)
        self._GPIO.output(self._params[1], self._GPIO.LOW)
        return p1

    def backward(self, **kwargs):

        """
        Set the PIN level such that backward motion is generated
        """

        p1 = self._GPIO.PWM(self._params[2], self._odisseus_config.MOTOR_PWM_FREQUENCY)
        self._GPIO.output(self._params[0], self._GPIO.LOW)
        self._GPIO.output(self._params[1], self._GPIO.HIGH)
        return p1

    def stop(self):

        """
        Set the PIN level such that the motor stops operating
        """
        self._GPIO.output(self._params[0], self._GPIO.LOW)
        self._GPIO.output(self._params[1], self._GPIO.LOW)


class Propulsion:

    def __init__(self, odisseus_config, params):

        self._odisseus_config = odisseus_config
        self.motor_A = Motor(odisseus_config=odisseus_config, name="FRONT_RIGHT", params=params.get_motor_params("FRONT_RIGHT"))
        self.motor_B = Motor(odisseus_config=odisseus_config, name="FRONT_LEFT",  params=params.get_motor_params("FRONT_LEFT"))
        self.setup()

    def setup(self):

        """
        Set up the pins using the parameters
        """

        self.motor_A.setup()
        self.motor_B.setup()

    def forward(self, speed, **kwargs):

        """
        Instructs underlying motors to generate forward motion
        """

        # clamp the max speed to 100 as this is the max dutty speed
        if speed > self._odisseus_config.MAX_DUTY_CYCLE:
            speed = self._odisseus_config.MAX_DUTY_CYCLE

        p1 = self.motor_A.forward(**kwargs)
        p2 = self.motor_B.forward(**kwargs)
        p1.start(speed)
        p2.start(speed)
        time.sleep(kwargs['time'])

    def backward(self, speed, **kwargs):

        """
        Instructs underlying motors to generate backward motion
        """

        # clamp the max speed to 100 as this is the max dutty speed
        if speed > self._odisseus_config.MAX_DUTY_CYCLE:
            speed = self._odisseus_config.MAX_DUTY_CYCLE

        p1 = self.motor_A.backward(**kwargs)
        p2 = self.motor_B.backward(speed=speed, **kwargs)
        p1.start(speed)
        p2.start(speed)
        time.sleep(kwargs['time'])

    def left(self, speed, **kwargs):

        """
        Fix PINs so that odisseus makes a left turn
        """

        # clamp the max speed to 100 as this is the max dutty speed
        if speed > self._odisseus_config.MAX_DUTY_CYCLE:
            speed = self._odisseus_config.MAX_DUTY_CYCLE

        self.motor_B.stop()
        p1 = self.motor_A.forward(**kwargs)
        p1.start(speed)
        time.sleep(kwargs['time'])

    def right(self, speed, **kwargs):

        """
        Fix PINs so that odisseus makes a right turn
        """

        # clamp the max speed to 100 as this is the max dutty speed
        if speed > self._odisseus_config.MAX_DUTY_CYCLE:
            speed = self._odisseus_config.MAX_DUTY_CYCLE

        self.motor_A.stop()
        p1 = self.motor_B.forward(**kwargs)
        p1.start(speed)
        time.sleep(kwargs['time'])

    def stop(self):

        """
        Stop both motors
        """
        self.motor_A.stop()
        self.motor_B.stop()





