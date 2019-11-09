"""
Main module for controlling Odisseus propulsion
"""

import copy
from multiprocessing import Process
from multiprocessing import Queue

from process_control_base import ProcessControlBase
from odisseus import Odisseus
from propulsion import Propulsion
from cmd_executor import CMDExecutor


class PropulsionProcess(ProcessControlBase):

    def __init__(self, odisseus_config):

        ProcessControlBase.__init__(self, config=odisseus_config, name=odisseus_config.PROPULSION_PROCESS_NAME)
        self._odisseus = None
        self._contorl_queue = Queue()
        self._cmd_executor = CMDExecutor(cmd_queue=self._contorl_queue)
        self._controller = None

    def start(self, **kwargs):

        """
        Start Odisseus: It creates a new instance of the robot and spawns a new process to run
        """
        propulsion = Propulsion.create_from_configuration(self.get_config())

        if 'PropulsionProcessController' not in kwargs.keys():
            raise KeyError("In PropulsionProcess-->start. The PropulsionProcessController has not been set")

        self._controller = kwargs[self.get_config().PROPULSION_CONTROLLER_NAME]

        self._odisseus = Odisseus(odisseus_config=self.get_config(), propulsion=propulsion, cmd_executor=self._cmd_executor)
        self._cmd_executor.set_odisseus_instance(odisseus=self._odisseus)
        self.spawn_odisseus_process()
        super(PropulsionProcess, self).start(**kwargs)

    def stop(self):
        """
            Stop the process  from executing
        """
        super(PropulsionProcess, self).stop()

        # there is not control so be safe
        self._odisseus.interrupt()
        self._odisseus.stop_raw()

    def spawn_odisseus_process(self):

        """
        Spawns a new process for Odisseus. Assumes that the
        odisseus robot has been created
        """

        if self._odisseus is None:
                if self.get_config().ENABLE_LOG:
                    print("Cannot spawn an " + self.get_name()+"  process when Odisseus is None")
                return

        # is there a reason to spawn the process if it is active?
        if self.is_alive():
            if self.get_config().ENABLE_LOG:
                print(self.get_name()+ " process is alive nothing to do here...")
            return

        # there is no point to start a new procees if Odisseus is interrupted
        self.remove_interrupt()
        self.set_process(proc=Process(target=self._odisseus.run, kwargs={}))

    def add_cmd(self, cmd):

        # use the controller before adding the CMD
        # to decide the CMD values

        speed_value = self._controller.execute_from_cmd(self, cmd, odisseus_speed=100)
        new_cmd = cmd.copy(cmd)
        new_cmd.speed_value = speed_value
        self._odisseus.add_cmd(copy.deepcopy(new_cmd))

    def cleanup_pins(self):

        """
        cleanup the pins. Should call reset_mode after this to get functional again
        """

        if self.get_config().ON_RASP_PI:
            import RPi.GPIO as GPIO
            GPIO.cleanup()

    def reset_mode(self, mod=None):

        """
        Reset the pins mode
        """
        if self.get_config().ON_RASP_PI:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)

