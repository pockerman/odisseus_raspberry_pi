"""
The master_process module provides the
implementation of the MasterProcess class. This is the entry
point for controlling Odisseus
"""

import json
import numpy as np

from multiprocessing import Queue
from process_control_base import ProcessControlBase
from propulsion_process import PropulsionProcess
from ultrasound_sensor_process import UltrasoundSensorProcess
from web_app_process import WebAppProcess

class MasterProcess(ProcessControlBase):

    """
    The MasterProcess is the control point for Odisseus
    """

    @staticmethod
    def read_config(filename):

        """
            Read the json configuration file and
            return a map with the config entries
        """
        with open(filename) as json_file:
            configuration = json.load(json_file)
            return configuration

    def __init__(self, odisseus_configuration, **kwargs):
        ProcessControlBase.__init__(self, config=odisseus_configuration,
                                    name=odisseus_configuration["MASTER_PROCESS_NAME"])

        self._processes = {}
        self._processes_created = False
        self._terminate_process_queue = Queue()
        self._start_process_queue = Queue()
        self._state = np.array([0., 0., 0.])
        self._motion_model = None

    def get_state(self):
        """
        Returns the state of Odisseus
        """
        return self._state

    def run(self, **kwargs):

        """
        Start running the master process
        """

        while True:

            # check if a process should die
            while self._terminate_process_queue.empty() is False:
                cmd = self._terminate_process_queue.get()
                self.terminate_process(proc_name=cmd.get_value())

            # check if a process should start
            while self._start_process_queue.empty() is False:
                cmd = self._start_process_queue.get()
                self.start_process(proc_name=cmd.get_value())

            # query distance from ultrasound
            #if self.get() in self._processes.keys():
            #    dist_msg = self._processes[UltrasoundSensorProcess.process_name()].get()
            #    print(dist_msg)
            #else:
             #   print("No distance received")

            # check if there is any cmd coming from the server
            # this will be high priority
            
            #self

            # poll the sensors to get information about the world state
            #print("Running master process")

            # update state

    def get_processes_names(self):
        """
        Returns all the names of the processes
        """
        return self._processes.keys()

    def get_process(self, name):
        """
        Returns the control instance of the process with the given name
        :param name: the process name
        """
        return self._processes[name]

    def add_cmd(self, cmd):

        if cmd.get_name() == "TerminateProcessCMD":
            self._terminate_process_queue.put(cmd)
        elif cmd.get_name() == "StartProcessCMD":
            self._start_process_queue.put(cmd)

    def create_processes(self, **kwargs):

        """
        Create the processes needed for Odisseus
        """

        if self.get_config()["ENABLE_MOTORS"] is True:
            # launch the motor process
            self._create_motors_process(**kwargs)

        if self.get_config()["ENABLE_ULTRASOUND_SENSOR"] is True:
            # launch the ultrasound sensor process
            self._create_ultrasound_process(**kwargs)

        if self.get_config()["ENABLE_WEB_SERVER"] is True:
            self._create_web_app_process(**kwargs)
            
        # a decision maker should always be created
        # we have it last in order to pass the created 
        # processes
        self._create_decision_maker_process(**kwargs)

        self._processes_created = True

    def terminate_all_processes(self):

        """
        Terminates all the processes handled by the master process
        """

        if self._processes_created:

            for proc_name in self._processes:
                self._processes[proc_name].stop()

    def terminate_process(self, proc_name):

        if proc_name in self._processes:
            self._processes[proc_name].stop()
            return

        raise ValueError("The process with name: {0} does not exist".format(proc_name))

    def start_process(self, proc_name, **kwargs):

        if proc_name == self.get_config()["PROPULSION_PROCESS_NAME"]:
            self._create_motors_process(**kwargs)
        elif proc_name == self.get_config()["ULTRASOUND_SENSOR_PROCESS_NAME"]:
            self._create_ultrasound_process(**kwargs)
        elif proc_name == self.get_config()["WEB_PROCESS_NAME"]:
            self._create_web_app_process(**kwargs)

    def _create_motors_process(self, **kwargs):

        """
        Create the motor process
        """

        self._processes.update({self.get_config()["PROPULSION_PROCESS_NAME"]:
                                    PropulsionProcess(odisseus_config=self._config)})
        self._processes[self.get_config()["PROPULSION_PROCESS_NAME"]].start(**kwargs)

    def _create_ultrasound_process(self, **kwargs):

        """
        Create the ultrasound process
        """

        self._processes.update({self.get_config()["ULTRASOUND_SENSOR_PROCESS_NAME"]:
                                    UltrasoundSensorProcess(odisseus_config=self._config,
                                                            port_max_size=self._config["ULTRASOUND_PORT_MAX_SIZE"],
                                                            distance_calculator=None)})

        self._processes[self.get_config()["ULTRASOUND_SENSOR_PROCESS_NAME"]].start(**kwargs)

    def _create_web_app_process(self, **kwargs):

        """
        Create the web app process
        """

        from web_app_process import WebAppProcess
        self._processes.update(
            {self.get_config()["WEB_PROCESS_NAME"]:
                 WebAppProcess(odisseus_config=self._config, master_process=self)})
        self._processes[self.get_config()["WEB_PROCESS_NAME"]].start(**kwargs)
        
        
    def _create_decision_maker_process(self, **kwargs):
        pass

