
import numpy as np
from matrix_descriptor import MatrixDescriptor

__all__ = ["ExtendedKalmanFilter"]

# Holds the names of the matrices used in the Kalman Filter class
NAMES = ["A", "B", "H", "P", "K", "Q", "R"]

class KFMatrixDescription(MatrixDescriptor):
    """
    Matrix description for Kalman Filter class
    """

    def __init__(self):
        MatrixDescriptor.__init__(self, names=NAMES)

    def set_matrix(self, name, item):
        """
        Set the Matrix with the given name to the given value
        """
        self._matrices[name] = item

    def get_matrix(self, name):
        return self._matrices[name]


class ExtendedKalmanFilter(object):

    def __init__(self, state, motion_model, observation_model,
                 matrix_description, odisseus_config):

        # the state vector to estimate
        self._state = state

        # configuration of odisseus
        self._config = odisseus_config

        # the motion model used
        self._motion_model = motion_model

        # the observation model used
        self._observation_model = observation_model

        # the matrix descriptor
        self._mat_desc = matrix_description

        # set the matrices

    def iterate(self, u, z, **kwargs):

        if 'v' in kwargs['v']:
            v = kwargs['v']
        else:
            v = np.array([0.0, 0.0])

        self.predict(u=u, v=v)

        if 'w' in kwargs['w']:
            w = kwargs['w']
        else:
            w = np.array([0.0, 0.0])

        self.update(z=z, w=w)

    def predict(self, u, v):
        """
        Performs the prediction step for Kalman Filter
        """
        state_val = self._state.get_value()

        # use the motion model to predict state
        state_pred = self._motion_model(xk=state_val, u=u, v=v )

        self._state.set_value(state_pred)

        P = self._mat_desc["P"]
        Q = self._mat_desc["Q"]
        L = self._motion_model.control_jacobian_matrix(xk=state_pred, u=u, v=v)
        L_T = L.T
        F = self._motion_model.state_jacobian_matrix(xk=state_pred, u=u, v=v)
        F_T = F.T
        P = F * P * F_T + L * Q * L_T
        self._mat_desc["P"] = P

    def update(self, z, w):
        """
        Performs the update step of the Kalman Filter
        """

        zpred = self._observation_model.value

        H = self._mat_desc["H"]
        H_T = self._mat_desc["H"].T
        P = self._mat_desc["P"]
        R = self._mat_desc["R"]

        S = H * P * H_T + R
        S_inv = np.linalg.inv(S)

        # compute gain matrix
        self._mat_desc["K"] = P * H_T * S_inv

        innovation = z - H * self._state.get_value()
        self._state += self._mat_desc["K"] * innovation
        I = np.identity(self._state.get_value().shape)

        # update covariance matrix
        P = (I - self._mat_desc["K"] * H) * P
        self._mat_desc["P"] = P

    def get_state(self):
        """
        Returns the state object managed by the filter
        :return: :class.State
        """
        return self._state

