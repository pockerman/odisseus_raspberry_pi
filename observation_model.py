
import numpy as np
class ObservationModel(object):
    """
    Observation model assumed of
    """

    def sonar_value(self, xk,  point, w):
        """
        """

        return np.sqrt((xk[0] - point[0])**2 + (xk[1] - point[1])**2) + w

    def sonar_model_jacobian(self, xk, point, w):

        return np.array([1.0/np.sqrt((xk[0] - point[0])**2 + (xk[1] - point[1])**2),
                         1.0/np.sqrt((xk[0] - point[0])**2 + (xk[1] - point[1])**2),
                         0.0])

    def sonar_model_jacobian_wrt_error(self, xk, point, w, shape_diagonal=None):
        """
        Compute \frac{\partial h}{\partial w}
        :param xk:
        :param point:
        :param w:
        :return:
        """
        if shape_diagonal is None:
            return np.array([1.0, 1.0])

        x = np.zeros(shape=shape_diagonal)
        np.fill_diagonal(x, 1.0)
        return x


