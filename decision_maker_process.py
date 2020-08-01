"""
The object responsible for generating CMDs based on sensor input
and Odisseus state
"""

import time
from multiprocessing import Process
import numpy as np

from process_control_base import ProcessControlBase
from control_cmds import PropulsionCmd
from extended_kalman_filter import ExtendedKalmanFilter


class DecisionMakerProcess(ProcessControlBase):

    @staticmethod
    def process_name():
        return "DecisionMakerProcess"

    def __init__(self, odisseus_config, process_map,
                 state_estimator, state_vector):

        """
        Constructor for the DecisionMakerProcess
        :param odisseus_config:
        :param process_map:
        :param state_estimator:
        :param state_vector: list()
        """

        ProcessControlBase.__init__(self, config=odisseus_config,
                                    name=odisseus_config["DECISION_MAKER_PROCESS_NAME"])

        # map holding the processes
        self._process_map = process_map
        self._state_estimator = state_estimator
        self._state_vector = state_vector

    def run(self):
        """
        Run the decision maker
        :return:
        """

        while not self.is_interrupted():

            # get all the input from the sensors
            # understand the world
            # create input for state estimator
            # run state estimator

            # sonar default value
            sonar_val = 0.0

            # we may not have sonar enabled..however even if it is
            # enabled this may not be working properly
            if self.get_config()["ULTRASOUND_SENSOR_PROCESS_NAME"] in self._process_map:
                sonar_val = self._process_map[self.get_config()["ULTRASOUND_SENSOR_PROCESS_NAME"]].get()

            # IR sensor
            ir_sensor_val = 0.0

            self.estimate_state(sonar_val.distance, ir_val=ir_sensor_val, camera_val=None)

            # make decision based on state and world
            # given the state have the RL agent to decide upon
            # the behavior

            # sleep for half a second
            time.sleep(0.5)

    def start(self, **kwargs):

        """
        Start the DecisionMakerProcess
        """

        # is there a reason to spawn the process if it is active?
        if self.is_alive():
            if self.get_config().ENABLE_LOG:
                print(self.get_name() + " process is alive nothing to do here...")
            return

        # there is no point to start a new procees if Odisseus is interrupted
        self.remove_interrupt()
        self.set_process(proc=Process(target=self.run, kwargs={}))
        super(DecisionMakerProcess, self).start(**kwargs)

    @property
    def state(self):
        return self._state_estimator.state


    def estimate_state(self, sonar_val, ir_val, camera_val):
        """
        Estimate the state of Odisseus
        :return:
        """

        u = np.array([1.0, 0.0])
        w = np.array([0.0, 0.0])
        z = np.array([sonar_val, ir_sensor_val])
        v = np.array([0.0, 0.0])
        self._state_estimator.iterate(u=u, z=z, w=w, v=v)

        # update the state vector
        for i in range(len(self._state_estimator.state)):
            self._state_vector[i] = self._state_estimator.state[i]

    def _get_cmd_based_on_distance(self):

        if self._process_map[self.get_config().ULTRASOUND_SENSOR_PROCESS_NAME] is not None:

            # poll the process for a measurement distance
            dist_msg = self._process_map[self.get_config()["ULTRASOUND_SENSOR_PROCESS_NAME"]].get()

            if self.get_config()["ENABLE_LOG"]:
                print("Received distance: ", dist_msg)

            if dist_msg - self.get_config()["MIN_DISTANCE_FROM_OBSTACLE"] < self.get_config()["TOLERANCE"]:
                # we need to break immediately
                return PropulsionCmd(direction="STOP", speed_value=0, duration=100)
            elif dist_msg - 2.0*self.get_config()["MIN_DISTANCE_FROM_OBSTACLE"] < self.get_config()["TOLERANCE"]:
                return PropulsionCmd(direction="STOP", speed_value=0, duration=100)

        raise ValueError("You should not call this DecisionMaker.get_cmd_based_on_distance when UltrasoundProcess is None.")

    def _get_camera_input(self):
        pass

    def _get_ir_input(self):
        pass