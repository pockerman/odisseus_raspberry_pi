"""
The object responsible for generating CMDs based on sensor input
and Odisseus state
"""

from process_control_base import ProcessControlBase
from control_cmds import PropulsionCmd


class DecisionMakerProcess(ProcessControlBase):

    @staticmethod
    def process_name():
        return "DecisionMakerProcess"

    def __init__(self, odisseus_config, process_map):
        ProcessControlBase.__init__(self, config=odisseus_config, name=odisseus_config.DECISION_MAKER_PROCESS_NAME)

        # map holding the processes
        self._process_map = process_map


    def run(self):
        """
        Run the decision maker
        :return:
        """
        pass


    def _get_cmd_based_on_distance(self):

        if self._process_map[self.get_config().ULTRASOUND_SENSOR_PROCESS_NAME] is not None:

            # poll the process for a measurement distance
            dist_msg = self._process_map[self.get_config().ULTRASOUND_SENSOR_PROCESS_NAME].get()

            if self.get_config().ENABLE_LOG:
                print("Received distance: ", dist_msg)

            if dist_msg - self.get_config().MIN_DISTANCE_FROM_OBSTACLE < self.get_config().TOLERANCE:
                # we need to break immediately
                return PropulsionCmd(direction="STOP", speed_value=0, duration=100)
            elif dist_msg - 2.0*self.get_config().MIN_DISTANCE_FROM_OBSTACLE < self.get_config().TOLERANCE:
                return PropulsionCmd(direction="STOP", speed_value=0, duration=100)

        raise ValueError("You should not call this DecisionMaker.get_cmd_based_on_distance when UltrasoundProcess is None.")

    def _get_camera_input(self):
        pass

    def _get_ir_input(self):
        pass