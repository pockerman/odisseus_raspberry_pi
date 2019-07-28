"""
Handles the four motors collectively
"""

from adafruit_motorkit import MotorKit

class Propulsion:

    def __init__(self):
        self.__motor_kit = MotorKit()


    def forward(self,  throttle):
        """
        Instruct the four motors to drive forward with throttle
        :param throttle: throttle should be in [0,1]
        """
        self.__motor_kit.motor1.throttle = throttle
        self.__motor_kit.motor2.throttle = throttle
        self.__motor_kit.motor3.throttle = throttle
        self.__motor_kit.motor4.throttle = throttle

    def reverse(self, throttle):
        """
        Instruct the four motors to drive backward with throttle
        :param throttle: throttle should be in [0,1]
        """
        self.__motor_kit.motor1.throttle = -throttle
        self.__motor_kit.motor2.throttle = -throttle
        self.__motor_kit.motor3.throttle = -throttle
        self.__motor_kit.motor4.throttle = -throttle

    def stop(self):
        """
        Instruct the four motors to stop. This is done by setting the
        throttle to zero
        """
        self.__motor_kit.motor1.throttle = 0
        self.__motor_kit.motor2.throttle = 0
        self.__motor_kit.motor3.throttle = 0
        self.__motor_kit.motor4.throttle = 0

    def stop_motor(self, motor_id):
        """
        Instruct the motor with the given motor_id to stop.
        This is done by setting the throttle of the motor to zero
        :param motor_id should be in [0, 3]
        """

        if motor_id not in [0, 1, 2, 3]:
            raise ValueError("Invalid motor id")

        if motor_id == 0:
            self.__motor_kit.motor1.throttle = 0
        elif motor_id == 1:
            self.__motor_kit.motor2.throttle = 0
        elif motor_id == 2:
            self.__motor_kit.motor3.throttle = 0
        elif motor_id == 3:
            self.__motor_kit.motor4.throttle = 0


