"""
Unit tests for Kalman Filter
"""

import numpy as np
import csv
import collections

from extended_kalman_filter import ExtendedKalmanFilter
from extended_kalman_filter import EKFMatrixDescription
from motion_model import MotionModel
from observation_model import ObservationModel
from state import State
from utilities import save_state_csv

ITERATIONS = 1000
RUN_SIM = True
SAVE_SIM = True
SHOW_SIM = True

motion_model = MotionModel()

def get_input_control(arg1, arg2, error):

    return np.array([arg1 + error[0], arg2 + error[1]])


def get_measurement(time, vt, state, error):
    """
    The poin that the sonar measured
    :param time:
    :param vt:
    :return:
    """
    u = get_input_control(vt , 0.0, [0.0, 0.0])
    state_true = motion_model.value(state, u=u, v=[0.0, 0.0])
    print("\tState true is: ", state_true)
    return np.array([state_true[0] + error[0], state_true[1] + error[1]])


def test_straight_line(odisseus_configuration):

    sigma2_d = 0.1
    sigma2_delta = 0.1
    delta_theta = 0.0

    # the state vector
    state = State(init_cond=None)

    # ExtendedKalmanFilter requires the specification of matrices
    matrix_description = EKFMatrixDescription()
    matrix_description["P"] = np.eye(state.size())

    matrix_description["Q"] = np.array([[sigma2_d, 0.0],
                                        [0.0, sigma2_delta*delta_theta]])

    matrix_description["R"] = np.array([[0.01, 0.0],
                                        [0.0, 0.01]])

    filter = ExtendedKalmanFilter(state=state,
                                  motion_model=MotionModel(),
                                  observation_model=ObservationModel(),
                                  matrix_description=matrix_description,
                                  odisseus_config=odisseus_configuration)

    if RUN_SIM:
        with open('state.csv', 'w', newline='') as csvfile:

            csv_file_writer = csv.writer(csvfile, delimiter=",")
            csv_file_writer.writerow(state.names())

            time = 0.0
            Dt = odisseus_configuration.SAMPLING_RATE

            w_L = 50 # (RPM)
            w_R = 50 # RPM

            R = odisseus_configuration.WHEELS_RADIUS
            vt = (w_L * R + w_R * R)/2.0

            measurement_error = [0.0, 0.0]
            contorl_error = [0.0, 0.0]

            for itr in range(ITERATIONS):

                print("At iteration: ", itr)
                print("\tInput speed: ", vt)
                print("\tState is: ", filter.get_state())

                time += Dt
                state.set_value(motion_model.value(state.get_value(), u=[vt, 0.0], v=[0.0, 0.0]))

                """
                u = get_input_control(arg1=vt, arg2=0.0, error=contorl_error)

                print("\tInput control is: ", u)

                z = get_measurement(time=Dt, vt=vt, error=measurement_error, state=filter.get_state().get_value())
                print("\tMeasurement is: ", z)
                filter.iterate(u=u, z=z)
                """
                if SAVE_SIM:
                    save_state_csv(filter.get_state(), csv_file=csvfile)


    if SHOW_SIM:

        odisseus_configuration.ON_RASP_PI = False
        # let's plot to see the evolved state
        if odisseus_configuration.ON_RASP_PI == False:
            import matplotlib.pyplot as plt

            with open('state.csv', 'r', newline='') as csvfile:
                csv_file_reader = csv.reader(csvfile, delimiter=",")

                row_count = 0
                est_state = np.zeros((ITERATIONS, len(state)))

                for row in csv_file_reader:

                    if row_count != 0:
                        est_state[row_count-1, :] = row
                    row_count += 1

            #plt.figure(figsize=(7, 5))
            #plt.plot(state[:, 0], state[:, 2], '-bo')
            plt.plot(est_state[:, 0], est_state[:, 2], '-ko')
            #plt.plot(meas[:, 0], meas[:, 1], ':rx')
            plt.xlabel('x [m]')
            plt.ylabel('y [m]')
            plt.legend(['true state', ]) #'inferred state', 'observed measurement'])
            plt.axis('square')
            plt.tight_layout(pad=0)
            plt.plot()
            plt.show()



def test(odisseus_configuration):
    test_straight_line(odisseus_configuration=odisseus_configuration)


if __name__ == '__main__':

    from odisseus_config import odisseus_config_obj
    test(odisseus_configuration=odisseus_config_obj)