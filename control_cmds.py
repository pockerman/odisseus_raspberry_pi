"""
Basic control cmds
"""


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

        """
        Returns the direction that the propulsion should generate motion
        """
        return self._direction

    def get_speed_value(self):

        """
        Returns the speed of the motion
        """
        return self._speed_val




