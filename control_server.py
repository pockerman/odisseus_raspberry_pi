"""
Main module for controlling Odisseus via web
"""

import copy
from multiprocessing import Process

from odisseus import Odisseus


class ControlServer:

    def __init__(self, odisseus_config):

        self._odisseus_config = odisseus_config
        self.__odisseus = None
        self.__odisseus_process = None

    def start(self, propulsion, control_queue):

        self.__odisseus = Odisseus(odisseus_config=self._odisseus_config, propulsion=propulsion, cmd_queue=control_queue)
        self.spawn_odisseus_process()

    def spawn_odisseus_process(self):
        """
        Spawns a new process for Odisseus. Assumes that the
        odisseus robot has been created
        """

        if self.__odisseus is None:
                if self._odisseus_config.ENABLE_LOG:
                    print("Cannot spawn an odisseus process when Odisseus is None")
                return

        # is there a reason to spawn the process if it is active?
        if self.__odisseus_process is not None and self.__odisseus_process.is_alive():
            if self._odisseus_config.ENABLE_LOG:
                print("Odisseus process is alive nothing to do here...")
            return

        # there is no point to start a new procees if Odisseus
        # is interrupted
        self.__odisseus.remove_interrupt()
        self.__odisseus_process = Process(target=self.__odisseus.run, kwargs={})
        self.__odisseus_process.start()

        if self._odisseus_config.ENABLE_LOG:
            print("Spawn a new Odisseus process...")

    def add_cmd(self, cmd):
        self.__odisseus.add_cmd(copy.deepcopy(cmd))

    def terminate_odisseus_process(self):

        if self.__odisseus_process is not None:
            self.__odisseus_process.terminate()
            self.__odisseus_process = None

        # there is not control so be safe
        self.__odisseus.interrupt()
        self.__odisseus.stop_raw()

    def cleanup_pins(self):

        if self._odisseus_config.ON_RASP_PI:
            import RPi.GPIO as GPIO
            GPIO.cleanup()

    def reset_mode(self, mod=None):
        if self._odisseus_config.ON_RASP_PI:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)

