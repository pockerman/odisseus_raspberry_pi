import numpy as np


class MotionModel(object):




    def value(self, xk, u, v):
        """
        Computes Odisseus next state dynamics
        The model adopted is a simple kinematic model for
        a differential drive system

        :param xk: array of length 3 storing the previous state
        :type  xk: array

        :param u: control input if length 2
        :type  u: array

        :param v: array of length 2 represents unpredictable process noise
        :type  v: array

        :return: np.array
        """

        x_next = xk[0] + (u[0] + v[0]) * np.cos(xk[2] + u[1] * 0.5 + v[1])
        y_next = xk[1] + (u[0] + v[0]) * np.sin(xk[2] + u[1] * 0.5 + v[1])
        psi_next = xk[2] + u[1] + v[1]

        return np.array([x_next, y_next, psi_next])

    def state_jacobian_matrix(self, xk, u, v):
        """
        Returns a 3x3 jacobian matrix of the dynamics matrix

        :param xk: array of length 3 storing the previous state
        :type  xk: array

        :param u: control input if length 2
        :type  u: array

        :param v: array of length 2 represents unpredictable process noise
        :type  v: array

        :return:
        """

        return np.array([[1.0, 0.0, (u[0] + v[0]) * np.sin(np.cos(xk[2] + u[1] * 0.5 + v[1]))],
                         [0.0, 1.0, -(u[0] + v[0]) * np.cos(xk[2] + u[1] * 0.5 + v[1])],
                         [0.0, 0.0, 1.0]])


    def control_jacobian_matrix(self, xk, u, v):
        """
        Returns a 3x3 jacobian matrix of the dynamics matrix

        :param xk: array of length 3 storing the previous state
        :type  xk: array

        :param u: control input if length 2
        :type  u: array

        :param v: array of length 2 represents unpredictable process noise
        :type  v: array

        :return:
        """

        return np.array([[np.cos(xk[2] + u[1] *0.5  + v[1]), 0.5*(u[0] + v[0])*np.sin(np.cos(xk[2] + u[1] * 0.5 + v[1]))],
                         [np.sin(xk[2] + u[1] * 0.5 + v[1]), -0.5**(u[0] + v[0])*np.cos(np.cos(xk[2] + u[1] * 0.5 + v[1]))],
                         [0.0, 1.0]])