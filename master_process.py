"""
The master_process module provides the
implementation of the MasterProcess class. This is the entry
point for controlling Odisseus
"""

from multiprocessing import Queue

from propulsion_process import PropulsionProcess
from ultrasound_sensor_process import UltrasoundSensorProcess
from web_app_process import WebAppProcess

class MasterProcess:

    """
    The MasterProcess is the control point for Odisseus
    """

    def __init__(self, odisseus_configuration, **kwargs):
        self._config = odisseus_configuration
        self._propulsion_control = None
        self._processes = {}
        self._processes_created = False
        self._terminate_process_queue = Queue()
        self._start_process_queue = Queue()
        self._ultrasound_sensor = None

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

        if cmd.__name__ == "TerminateProcessCMD":
            self._terminate_process_queue.put(cmd)
        elif cmd.__name__ == "StartProcessCMD":
            self._start_process_queue.put(cmd)

    def create_processes(self, **kwargs):

        """
        Create the processes needed for Odisseus
        """

        if self._config.ENABLE_MOTORS is True:
            # launch the motor process
            self._create_motors_process(**kwargs)

        if self._config.ENABLE_ULTRASOUND_SENSOR is True:
            # launch the ultrasound sensor process
            self._create_ultrasound_process(**kwargs)

        if self._config.ENABLE_WEB_SERVER is True:
            self._create_web_app_process(**kwargs)

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

        if proc_name == PropulsionProcess.process_name():
            self._create_motors_process(**kwargs)
        elif proc_name == UltrasoundSensorProcess.process_name():
            self._create_ultrasound_process(**kwargs)
        elif proc_name == WebAppProcess.process_name():
            self._create_web_app_process(**kwargs)


    def run(self, **kwargs):

        """
        Start running the master process
        """

        #if self._processes_created is False:
        #    self.create_processes(**kwargs)

        while True:

            # check if a process should die
            while self._terminate_process_queue.empty() is False:
                cmd = self._terminate_process_queue.get()
                self.terminate_process(proc_name=cmd.get_value())

            # check if a process should start
            while self._start_process_queue.empty() is False:
                cmd = self._start_process_queue.get()
                self.start_process(proc_name=cmd.get_value())



            # check if there is any cmd coming from the server
            # this will be high priority



            # poll the sensors to get information about the world state
            #print("Running master process")

    def _create_motors_process(self, **kwargs):

        """
        Create the motor process
        """

        self._processes.update({PropulsionProcess.process_name(): PropulsionProcess(odisseus_config=self._config)})
        self._processes[PropulsionProcess.process_name()].start(**kwargs)

    def _create_ultrasound_process(self, **kwargs):

        """
        Create the ultrasound process
        """

        self._processes.update({UltrasoundSensorProcess.process_name(): UltrasoundSensorProcess(odisseus_config=self._config,
                                                                                                port_max_size=self._config.ULTRASOUND_SENSOR_PORT_MAX_SIZE,
                                                                                                distance_calculator=None)})
        self._processes[UltrasoundSensorProcess.process_name()].start(**kwargs)

    def _create_web_app_process(self, **kwargs):

        """
        Create the web app process
        """

        from web_app_process import WebAppProcess
        self._processes.update(
            {WebAppProcess.process_name(): WebAppProcess(odisseus_config=self._config, master_process=self)})
        self._processes[WebAppProcess.process_name()].start(**kwargs)

