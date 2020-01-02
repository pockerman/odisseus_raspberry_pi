
import numpy as np
class ObservationModel(object):
    """
    Observation model assumed of
    """

    def sonar_value(self, xk,  point, w):
        """
        """

        return np.sqrt((xk[0] - point[0])**2 + (xk[1] - point[1])**2)