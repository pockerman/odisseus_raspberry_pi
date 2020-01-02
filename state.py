"""
State describe the state of Odisseus
"""

import numpy as np


class State(object):

    @staticmethod
    def names():
        return ["X", "Y", "Vx", "Vy", "Theta"]

    def __init__(self, init_cond):

        if init_cond:
            self._state = init_cond
        else:
            self._state = np.array([0., 0., 0., 0., 0.])

    def get_value(self):
        return self._state

    def set_value(self, value):
        self._state = value

    def __iadd__(self, other):
        self._state += other
        return self

    def __len__(self):
        return len(self._state)