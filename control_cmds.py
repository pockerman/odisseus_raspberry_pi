"""
Basic control cmds
"""


class ControlCmd(object):

    def __init__(self, name, duration, value=None):

        self._name = name
        self._duration = duration
        self._value = value

    def get_name(self):
        return self._name

    def get_duration(self):
        return self._duration

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

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

        """
        Returns the direction that the propulsion should generate motion
        """
        return self._direction

    def get_speed_value(self):

        """
        Returns the speed of the motion
        """
        return self._speed_val

class TerminateProcessCMD(ControlCmd):

    def __init__(self, process_name):
        ControlCmd.__init__(self, name="TerminateProcessCMD", duration=None, value=process_name)

class StartProcessCMD(ControlCmd):

    def __init__(self, process_name):
        ControlCmd.__init__(self, name="StartProcessCMD", duration=None, value=process_name)






