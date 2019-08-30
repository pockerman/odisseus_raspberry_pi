"""
Basic control cmds
"""

class ControlCmd(object):

    def __index__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name



class PropulsionCmd(ControlCmd):

    def __init__(self, direction, speed_value):
        ControlCmd.__init__("PropulsionCmd")
        self.__direction = direction
        self.__speed_val = speed_value

    def get_direction(self):
        return self.__direction

    def get_speed_value(self):
        return self.__speed_val