"""
Basic control cmds
"""
import time
from config.config import ENABLE_WARNINGS
class ControlCmd(object):

    def __init__(self, name, duration):
        self.__name = name
        self.__duration = duration

    def get_name(self):
        return self.__name

    def get_duration(self):
        return self.__duration


class PropulsionCmd(ControlCmd):

    DIRECTIONS = ["FWD", "REVERSE", "RIGHT", "LEFT", "STOP"]

    def __init__(self, direction, speed_value, duration):
        ControlCmd.__init__("PropulsionCmd", duration=duration)

        if direction not in PropulsionCmd.DIRECTIONS:
            raise ValueError("Invalid Direction. Direction: " + direction + " not in " + str(PropulsionCmd.DIRECTIONS))

        self.__direction = direction
        self.__speed_val = speed_value

    def get_direction(self):
        return self.__direction

    def get_speed_value(self):
        return self.__speed_val

    def execute(self, robot):

        if self.__direction == "STOP":
            robot.stop_raw()
        elif self.__direction == "FWD":
            robot.move_fwd_raw(self.get_speed_value())
        elif self.__direction == "REVERSE":
            robot.move_reverse_raw(self.get_speed_value())
        elif self.__direction == "LEFT":
            robot.move_left_raw(self.get_speed_value())
        elif self.__direction == "RIGHT":
            robot.move_right_raw(self.get_speed_value())
        elif ENABLE_WARNINGS:
            print("Direction: ", self.__direction, " not in ", str(PropulsionCmd.DIRECTIONS))

        time.sleep(self.get_duration())


