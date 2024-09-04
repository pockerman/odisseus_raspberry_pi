"""
Main module for controlling Odisseus ultrasound sensor
"""

from multiprocessing import Process

from process_control_base import ProcessControlBase
from ultrasound_sensor import UltrasoundSensor
#from ultrasound_sensor import UltrasoundSensorPort


class UltrasoundSensorProcess(ProcessControlBase):

    def __init__(self, odisseus_config, port_max_size, distance_calculator):

        ProcessControlBase.__init__(self, config=odisseus_config, name=odisseus_config.ULTRASOUND_SENSOR_PROCESS_NAME)
        self._port_inst = UltrasoundSensorPort(odisseus_config=self.get_config(), max_size=port_max_size)
        self._sensor = UltrasoundSensor(odisseus_config=self.get_config(), port_inst=self._port_inst, distance_calculator = distance_calculator)

    def start(self, **kwargs):

        # is there a reason to spawn the process if it is active?
        if self.is_alive():
            if self.get_config().ENABLE_LOG:
                print(self.get_name() + " process is alive nothing to do here...")
            return

        # there is no point to start a new procees if this process is interrupted
        self.remove_interrupt()
        self._sensor.set_sense_flag(value=True)
        self.set_process(proc=Process(target=self._sensor.run, kwargs={"ULTRA_SOUND_TRIGGER_PULSE_TIME":self.get_config().ULTRA_SOUND_TRIGGER_PULSE_TIME}))
        super(UltrasoundSensorProcess, self).start(**kwargs)

    def get(self):
        """
        Returns a measurement
        """
        return self._sensor.get()



