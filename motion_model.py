import numpy as np


class MotionModel(object):


    def __init__(self, Dt, tol):
      self._state = np.array([0.0, 0.0, 0.0])
      self._tol = tol


    def value(self, u, werr):
        """
        Computes Odisseus next state dynamics
        The model adopted is a simple kinematic model for
        a differential drive system

        :param u: control input if length 2
        :type  u: array

        :param werr: array of length 2 represents unpredictable process noise
        :type  werr: array

        :return: np.array
        """

        # the angular velocity
        w = u[1]
        theta = self._state[2]

        if np.fabs(w) < self._tol:
          # the orientation has not chenged

          self._state[0] += (u[0]*self._Dt + werr[0])*np.cos(theta +  werr[1])
          self._state[1] += (u[0]*self._Dt + werr[0])*np.sin(theta +  werr[1])
        else:

          self._state[2] += w*self._Dt + werr[1]
          self._state[0] += (u[0]/(2*w) + werr[0])*(np.sin(self._state[2]) - np.sin(theta))
          self._state[1] -= (u[0]/(2*w) + werr[0])*(np.cos(self._state[2]) - np.cos(theta))


        return self._state

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

        return np.array([[1.0, 0.0,  (u[0] + v[0]) * np.sin(xk[2] + u[1] + v[1])],
                         [0.0, 1.0, -(u[0] + v[0]) * np.cos(xk[2] + u[1] + v[1])],
                         [0.0, 0.0, 1.0]])

    def l_matrix(self, xk, u, v):
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

        return np.array([[np.cos(xk[2] + u[1] + v[1]),  (u[0] + v[0])*np.sin(xk[2] + u[1] + v[1])],
                         [np.sin(xk[2] + u[1] + v[1]), -(u[0] + v[0])*np.cos(xk[2] + u[1] + v[1])],
                         [0.0, 1.0]])