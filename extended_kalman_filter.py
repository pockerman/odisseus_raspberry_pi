
import numpy as np
from matrix_descriptor import MatrixDescriptor

__all__ = ["ExtendedKalmanFilter",
           "EKFMatrixDescription"]

# Holds the names of the matrices used in the Kalman Filter class
NAMES = ["A", "B", "H", "P", "K", "Q", "R"]

class EKFMatrixDescription(MatrixDescriptor):
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

    def iterate(self, u, z, **kwargs):

        if 'v' in kwargs.keys() :
            v = kwargs['v']
        else:
            v = np.array([0.0, 0.0])

        self.predict(u=u, v=v)

        if 'w' in kwargs.keys():
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
        state_pred = self._motion_model.value(xk=state_val, u=u, v=v )

        self._state.set_value(state_pred)

        P = self._mat_desc["P"]
        Q = self._mat_desc["Q"]

        L = self._motion_model.l_matrix(xk=state_pred, u=u, v=v)
        L_T = L.T

        F = self._motion_model.state_jacobian_matrix(xk=state_pred, u=u, v=v)
        F_T = F.T

        P = F * P * F_T + np.dot(L , np.dot( Q,  L_T))
        self._mat_desc["P"] = P

    def update(self, z, w):

        """
        Performs the update step of the Extended Kalman Filter

        :param z: the sensor measurements
        :type  z:

        :param w: error vector associated with the meansuremnt

        """

        P = self._mat_desc["P"]
        R = self._mat_desc["R"]

        zpred = self._observation_model.sonar_value(xk=self._state.get_value(), point=z, w=w)

        H = self._observation_model.sonar_model_jacobian(xk=self._state.get_value(), point=z, w=w)
        H_T = H.T

        M = self._observation_model.sonar_model_jacobian_wrt_error(xk=self._state.get_value(),
                                                                   point=z, w=w, shape_diagonal=R.shape)

        try:
            # S = H*P*H^T + M*R*M^T
            S_inv = np.linalg.inv(np.dot(H, np.dot( P , H_T)) + np.dot(M, np.dot(R, M.T)))

            # compute the gain matrix
            K = np.dot(P, np.dot( H_T , S_inv))

            # compute gain matrix
            self._mat_desc["K"] = K

            innovation = z - zpred
            self._state += np.dot(self._mat_desc["K"], innovation)

            I = np.zeros(shape=(len(self._state), len(self._state)))
            np.fill_diagonal(I, 1.0)

            # update covariance matrix
            P = (I - np.dot(self._mat_desc["K"], H)) * P
            self._mat_desc["P"] = P

        except np.linalg.linalg.LinAlgError as exception:

            if str(exception) == 'Singular matrix':
                # this is a singular matrix what
                # should we do? Simply use the predicted
                # values and log the fact that there was a singular matrix
                raise

    def get_state(self):
        """
        Returns the state object managed by the filter
        :return: :class.State
        """
        return self._state

    def set_matrix(self, name, mat):
        """
        Set the matrix with name
        :param name: The name of the matrix to set
        :param mat: The matrix
        :return:
        """
        self._mat_desc.set_matrix(name=name, mat=mat)

