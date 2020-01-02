"""
Unit tests for Kalman Filter
"""

import numpy as np
import csv

from extended_kalman_filter import ExtendedKalmanFilter
from state import State
from utilities import save_state_csv

ITERATIONS = 1000


def get_input_control(k):

    if k == 50:
        return np.array([5.0, 0.5])
    elif k == 100:
        return np.array([5.0, -0.5])

    return np.array([5.0, 0.0])

def get_measurement():
    return np.array([0.0, 0.0])

def test_integration(filter):
    pass

def test(odisseus_configuration):

    # the state vector
    state = State(init_cond=None)

    # KalmanFilter requires the specification
    # of matrices

    filter = ExtendedKalmanFilter(state=state, odisseus_config=odisseus_configuration)

    with open('state.csv', 'w', newline='') as csvfile:
        csv_file_writer = csv.writer(csvfile, delimiter=",")
        csv_file_writer.writerow(state.names())

        for itr in range(ITERATIONS):

            u = get_input_control()
            z = get_measurement()
            filter.iterate(u=u, z=z)

            save_state_csv(filter.get_state(), csv_file=csvfile)

    odisseus_configuration.ON_RASP_PI = False
    # let's plot to see the evolved state
    if odisseus_configuration.ON_RASP_PI == False:
        import matplotlib.pyplot as plt

        with open('state.csv', 'r', newline='') as csvfile:
            csv_file_reader = csv.reader(csvfile, delimiter=",")

            row_count = 0
            est_state = np.zeros((ITERATIONS, len(state)))

            for row in csv_file_reader:

                if row_count == 0:
                    continue
                else:
                    est_state[row_count, : ]  = row

        #plt.figure(figsize=(7, 5))
        #plt.plot(state[:, 0], state[:, 2], '-bo')
        plt.plot(est_state[:, 0], est_state[:, 2], '-ko')
        #plt.plot(meas[:, 0], meas[:, 1], ':rx')
        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        plt.legend(['true state', 'inferred state', 'observed measurement'])
        plt.axis('square')
        plt.tight_layout(pad=0)
        plt.plot()
        plt.show()


if __name__ == '__main__':

    from odisseus_config import odisseus_config_obj
    test(odisseus_configuration=odisseus_config_obj)