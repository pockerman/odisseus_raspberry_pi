"""
Basic control cmds
"""
import time
from odisseus_config import odisseus_config_obj
ENABLE_WARNINGS = odisseus_config_obj.ENABLE_WARNINGS


class ControlCmd(object):

    def __init__(self, name, duration):
        self._name = name
        self._duration = duration

    def get_name(self):
        return self._name

    def get_duration(self):
        return self._duration


class PropulsionCmd(ControlCmd):

    DIRECTIONS = ["FWD", "REVERSE", "RIGHT", "LEFT", "STOP"]

    def __init__(self, direction, speed_value, duration):
        ControlCmd.__init__(self, name="PropulsionCmd", duration=duration)

        # TODO: Do we really want this here??
        # Perhaps having a safe mode is better
        if direction not in PropulsionCmd.DIRECTIONS:
            raise ValueError("Invalid Direction. Direction: " + direction + " not in " + str(PropulsionCmd.DIRECTIONS))

        self._direction = direction
        self._speed_val = speed_value

    def get_direction(self):
        return self._direction

    def get_speed_value(self):
        return self._speed_val

    def execute(self, robot):

        if self._direction == "STOP":
            robot.stop_raw()
        elif self._direction == "FWD":
            robot.move_fwd_raw(self.get_speed_value())
        elif self._direction == "REVERSE":
            robot.move_reverse_raw(self.get_speed_value())
        elif self._direction == "LEFT":
            robot.move_left_raw(self.get_speed_value())
        elif self._direction == "RIGHT":
            robot.move_right_raw(self.get_speed_value())
        elif ENABLE_WARNINGS:
            print("Direction: ", self._direction, " not in ", str(PropulsionCmd.DIRECTIONS))

        time.sleep(self.get_duration())


