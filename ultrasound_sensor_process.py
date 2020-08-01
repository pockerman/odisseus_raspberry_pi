"""
UltrasoundSensorProcess
"""

from multiprocessing import Process

from process_control_base import ProcessControlBase
from ultrasound_sensor import UltrasoundSensor
from ultrasound_sensor import UltrasoundSensorPort


class UltrasoundSensorProcess(ProcessControlBase):
    """
    UltrasoundSensorProcess class handles the ultrasound sensor
    HC-SR04. Odisseus can query the interface of this class to get
    measurements of distances from objects
    """

    def __init__(self, odisseus_config, sonar):
        """
        Constructor. create an instance by passing Odisseus configuration map and the
        sonar instance that is handled by the process.
        :param odisseus_config: The configuration map for Odisseus
        :param sonar: The sonar instance handled by the process
        """

        if sonar is None:
            raise ValueError("SensorProcess needs a sonar object")

        ProcessControlBase.__init__(self, config=odisseus_config,
                                    name=odisseus_config["ULTRASOUND_SENSOR_PROCESS_NAME"])
        self._sonar = sonar

    def start(self, **kwargs):

        # is there a reason to spawn the process if it is active?
        if self.is_alive():
            if self.get_config()["ENABLE_LOG"]:
                print(self.get_name() + " process is alive nothing to do here...")
            return

        # there is no point to start a new procees if this process is interrupted
        self.remove_interrupt()

        self.set_process(proc=Process(target=self._sonar.run,
                                      kwargs={"ULTRA_SOUND_TRIGGER_PULSE_TIME": self.get_config()["ULTRA_SOUND_TRIGGER_PULSE_TIME"]}))
        super(UltrasoundSensorProcess, self).start(**kwargs)

    def get(self):
        """
        Returns a measurement
        """
        return self._sonar.get()



