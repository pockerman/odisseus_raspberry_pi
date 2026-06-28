"""
Main module for controlling Odisseus propulsion
"""

import copy
from multiprocessing import Process
from multiprocessing import Queue
import serial

from processes.process_base import ProcessBase
from odisseus import Odisseus
from propulsion import Propulsion
from cmd_executor import CMDExecutor


class PropulsionProcess(ProcessBase):

    def __init__(self, config: dict):

        super().__init__(self, config=config,
                         name=config["PROPULSION_PROCESS_NAME"])

        self._odisseus = None
        self._contorl_queue = Queue()
        self._cmd_executor = CMDExecutor(cmd_queue=self._contorl_queue)
        self._controller = None
        self._arduino_serial = None

    def start(self, **kwargs):

        """
        Start Odisseus: It creates a new instance of the
        robot and spawns a new process to run
        """

        arduino_port = self.arduino_serial_port
        arduino_serial_port_rate = self.arduino_serial_port_rate
        self._arduino_serial = serial.Serial(arduino_port, arduino_serial_port_rate)

    def execute_cmd(self, cmd) -> None:
        """Executes the given motor cmd

        """
        pass 

    def stop(self):
        """
            Stop the process  from executing
        """
        super(PropulsionProcess, self).stop()

        # there is not control so be safe
        self._odisseus.interrupt()
        self._odisseus.stop_raw()

    def cleanup_pins(self) -> None:

        """
        cleanup the pins. Should call reset_mode after this to get functional again
        """

        if self.get_config()["ON_RASP_PI"]:
            import RPi.GPIO as GPIO
            GPIO.cleanup()
        else:
            import GPIOMock as GPIO
            GPIO.cleanup()

    def reset_mode(self, mod=None) -> None:

        """
        Reset the pins mode
        """
        if self.get_config()["ON_RASP_PI"]:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
        else:
            import GPIOMock as GPIO
            GPIO.setmode(GPIO.BCM)
