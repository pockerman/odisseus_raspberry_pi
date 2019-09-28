"""
Module that handles the data from the ultrasound sensor
"""
import copy
import time
from multiprocessing import Queue


class UltrasoundSensorMsg:

    def __init__(self, distance, id, timestamp):
        self.distance = distance
        self.id = id
        self.timestamp = timestamp

    def __str__(self):
        return "Id: "+self.id+", Distance: "+self.distance+", Timestamp: "+self.timestamp


class UltrasoundSensorPort:

    """
    A deposit for distance calculations performed by the Ultrasound sensor.
    The Control server or any other application should use this API to acquire
    any distance calculation from the sensor
    """

    def __init__(self, odisseus_config, max_size):

        self._odisseus_config = odisseus_config
        self._queue = Queue(maxsize=max_size)
        self._next_available_id = 0
        self._max_size = max_size

    def put(self, distance):

        """
        Create a new distance msg and put it into the underlying queue
        """

        if distance is None:
            raise ValueError("Cannot queue None item...")

        # if we have reached the maximum size then throw away the
        # oldest measurement
        if self._queue.qsize() == self._max_size:
            msg = self._queue.get()
            if self._odisseus_config.ENABLE_LOG:
                print("Removing measurement: ", msg.id)

        if self._odisseus_config.ENABLE_LOG:
            print("Adding distance...to queue")

        msg = UltrasoundSensorMsg(distance=distance, id=self._next_available_id, timestamp=time.time())
        self._queue.put(copy.deepcopy(msg))
        self._next_available_id +=1

    def get(self):

        """
        Returns the top distance calculation in the queue
        """
        return self._queue.get()

    def size(self):

        """
        Returns how many messages are currently in the queue
        """
        return self._queue.qsize()

    def max_size(self):
        """
        :return the maximum size of messages the port supports
        """
        return self._max_size


class UltrasoundSensor:

    """
    Models the HC-SR04 ultrasound sensor
    """

    @staticmethod
    def default_distance_calculator(Gpio, ECHO_PIN):

        """
        Default distance calculator. Uses default speed of sound 34300 cm/sec
        """

        SPEED_OF_SOUND = 34300.0 #cm/sec

        while Gpio.input(ECHO_PIN) == 0:
            pulse_start = time.time()

        while Gpio.input(ECHO_PIN) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = 0.5*pulse_duration * SPEED_OF_SOUND
        distance = round(distance, 2)
        return distance

    def __init__(self, odisseus_config, port_inst, distance_calculator = None):

        self._odisseus_config = odisseus_config
        self._port_inst = port_inst
        self._is_setup = False
        self._sense = False

        if distance_calculator is None:
            self._distance_calculator = UltrasoundSensor.default_distance_calculator
        else:
            self._distance_calculator = distance_calculator

        if self._odisseus_config.ON_RASP_PI:
            import RPi.GPIO as GPIO
            self._GPIO = GPIO
        else:
            from gpio_mock import GPIOMock as GPIO
            self._GPIO = GPIO

        self.setup()

    def is_setup(self):

        """
        Returns true if the setup of the port is finished
        """
        return self._is_setup

    def set_sense_flag(self, value):
        self._sense = value

    def setup(self):

        """
        Setup the pins for the ultrasound sensor
        """

        if self._odisseus_config.ENABLE_LOG:
            print("Setting up Ultrasound sensor...this will take: {0} seconds".format(self._odisseus_config.SLEEP_TIME_FOR_SETTING_UP_ULTRA_SENSOR))

        self._GPIO.setup(self._odisseus_config.TRIG_PIN, self._GPIO.OUT)
        self._GPIO.setup(self._odisseus_config.ECHO_PIN, self._GPIO.IN)

        # Ensure that the Trigger pin is set low, and give the sensor a second to settle
        self._GPIO.output(self._odisseus_config.TRIG_PIN, self._GPIO.LOW)
        time.sleep(self._odisseus_config.SLEEP_TIME_FOR_SETTING_UP_ULTRA_SENSOR)

        if self._odisseus_config.ENABLE_LOG:
            print("Setting up Ultrasound sensor finished")

        self._is_setup = True

    def run(self, **kwargs):

        """
        Sense any obstacles around
        """
        while self._sense is True:
            self._GPIO.output(self._odisseus_config.TRIG_PIN, self._GPIO.LOW)
            time.sleep(self._odisseus_config.SLEEP_TIME_FOR_SETTING_UP_ULTRA_SENSOR)

            self._GPIO.output(self._odisseus_config.TRIG_PIN, self._GPIO.HIGH)
            time.sleep(kwargs['ULTRA_SOUND_TRIGGER_PULSE_TIME'])
            self._GPIO.output(self._odisseus_config.TRIG_PIN, self._GPIO.LOW)

            distance = self._distance_calculator(Gpio=self._GPIO,
                                                 ECHO_PIN=self._odisseus_config.ECHO_PIN)
            print("Distance calculated: ",distance)
            self._port_inst.put(distance=distance)