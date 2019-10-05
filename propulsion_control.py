"""
Main module for controlling Odisseus via web
"""

import copy
from multiprocessing import Process
from multiprocessing import Queue

from odisseus import Odisseus
from propulsion import Propulsion
from cmd_executor import CMDExecutor



class PropulsionControl:

    def __init__(self, odisseus_config):

        self._odisseus_config = odisseus_config
        self._odisseus = None
        self._odisseus_process = None
        self._contorl_queue = Queue()
        self._cmd_executor = CMDExecutor(cmd_queue=self._contorl_queue)

    def start(self, propulsion):

        """
        Start Odisseus: It creates a new instance of the robot and spawns a new process to run
        """

        if propulsion is None:
            propulsion = Propulsion.create_from_configuration(self._odisseus_config)

        self._odisseus = Odisseus(odisseus_config=self._odisseus_config, propulsion=propulsion, cmd_executor=self._cmd_executor)
        self._cmd_executor.set_odisseus_instance(odisseus=self._odisseus)
        self.spawn_odisseus_process()

    def stop(self):
        """
        Stop this controller from executing
        """
        self._odisseus_process.terminate()


    def spawn_odisseus_process(self):

        """
        Spawns a new process for Odisseus. Assumes that the
        odisseus robot has been created
        """

        if self._odisseus is None:
                if self._odisseus_config.ENABLE_LOG:
                    print("Cannot spawn an odisseus process when Odisseus is None")
                return

        # is there a reason to spawn the process if it is active?
        if self._odisseus_process is not None and self._odisseus_process.is_alive():
            if self._odisseus_config.ENABLE_LOG:
                print("Odisseus process is alive nothing to do here...")
            return

        # there is no point to start a new procees if Odisseus is interrupted
        self._odisseus.remove_interrupt()
        self._odisseus_process = Process(target=self._odisseus.run, kwargs={})
        self._odisseus_process.start()

        if self._odisseus_config.ENABLE_LOG:
            print("Spawn a new Odisseus process...")

    def add_cmd(self, cmd):
        self._odisseus.add_cmd(copy.deepcopy(cmd))

    def terminate_odisseus_process(self):

        if self._odisseus_process is not None:
            self._odisseus_process.terminate()
            self._odisseus_process = None

        # there is not control so be safe
        self._odisseus.interrupt()
        self._odisseus.stop_raw()

    def cleanup_pins(self):

        """
        cleanup the pins. Should call reset_mode after this to get functional again
        """

        if self._odisseus_config.ON_RASP_PI:
            import RPi.GPIO as GPIO
            GPIO.cleanup()

    def reset_mode(self, mod=None):

        """
        Reset the pins mode
        """
        if self._odisseus_config.ON_RASP_PI:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)

