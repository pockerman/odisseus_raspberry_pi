"""
The master_process module provides the
implementation of the MasterProcess class. This is the entry
point for controlling Odisseus
"""

from multiprocessing import Queue

from propulsion_process import PropulsionProcess
from ultrasound_sensor_process import UltrasoundSensorProcess

class MasterProcess:

    """
    The MasterProcess is the control point for Odisseus
    """

    def __init__(self, odisseus_configuration, **kwargs):
        self._config = odisseus_configuration
        self._propulsion_control = None
        self._processes = {}
        self._processes_created = False

    def get_processes_names(self):
        return self._processes.keys()

    def create_processes(self):
        """
        Create the processes needed for Odisseus
        """

        if self._config.ENABLE_MOTORS is True:
            # launch the motor process
            self._create_motors_process()

        if self._config.ENABLE_ULTRASOUND_SENSOR is True:
            # launch the ultrasound sensor process
            self._create_ultrasound_process()
        self._processes_created = True

    def terminate_all_processes(self):
        if self._processes_created:

            for proc_name in self._processes:
                self._processes[proc_name].stop()

    def run(self):

        """
        Start running the master process
        """

        if self._processes_created is False:
            self.create_processes()

        while True:

            # check if there is any cmd coming from the server
            # this will be high priority

            # poll the sensors to get information about the world state
            print("Running master process")


    def _create_motors_process(self):

        """
        Create the motor process
        """

        self._processes.update({"PropulsionControlProcess": PropulsionProcess(odisseus_config=self._config)})
        self._processes["PropulsionControlProcess"].start(propulsion=None)

    def _create_ultrasound_process(self):

        self._processes.update({UltrasoundSensorProcess.process_name(): UltrasoundSensorProcess(odisseus_config=self._config,
                                                                                                port_max_size=self._config.ULTRASOUND_SENSOR_PORT_MAX_SIZE,
                                                                                                distance_calculator=None)})
        self._processes[UltrasoundSensorProcess.process_name()].start()

