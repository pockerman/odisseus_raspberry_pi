
import time
from multiprocessing import Process

from ultrasound_sensor import UltrasoundSensor
from ultrasound_sensor import UltrasoundSensorPort
from ultrasound_sensor import UltrasoundSensorMsg


def distance_calculator(Gpio, ECHO_PIN):

    """
    dummy distance calculator
    """
    return 0.0


def test_setup(odisseus_configuration):
    """
    Test the setup method
    """

    print("\t test_setup")

    port_inst = UltrasoundSensorPort(max_size = odisseus_configuration.ULTRASOUND_PORT_MAX_SIZE)

    # this will trigger the setup
    sensor = UltrasoundSensor(odisseus_config=odisseus_configuration, port_inst=port_inst)
    assert sensor.is_setup(), "Sensor is not setup properly"


def test_assign_msg(odisseus_configuration):

    """
    Test assign message
    """

    print("\t test_assign_msg")

    port_inst = UltrasoundSensorPort(max_size = odisseus_configuration.ULTRASOUND_PORT_MAX_SIZE)

    dist_calculator = distance_calculator

    if odisseus_configuration.ON_RASP_PI:
        dist_calculator = UltrasoundSensor.default_distance_calculator

    sensor = UltrasoundSensor(odisseus_config=odisseus_configuration,
                              port_inst=port_inst,
                              distance_calculator=dist_calculator)

    assert sensor.is_setup(), "Sensor is not setup properly"

    sensor.set_sense_flag(value=True)

    kwargs = dict()
    kwargs['ULTRA_SOUND_TRIGGER_PULSE_TIME'] = odisseus_configuration.ULTRA_SOUND_TRIGGER_PULSE_TIME

    sensor_process = Process(target=sensor.run, kwargs=kwargs)
    sensor_process.start()

    # sleep this process for a three seconds
    time.sleep(3)
    sensor.set_sense_flag(value=False)

    sensor_process.join()

    # terminate the sensor process
    sensor_process.terminate()

    assert port_inst.size() == 1, "No distance message was set"
    msg = port_inst.get()
    print("Message: ",msg)


def test(odisseus_configuration):

    try:

        print("============================")
        print("Executing Ultrasound Tests...")

        if odisseus_configuration.ON_RASP_PI:
            import RPi.GPIO as GPIO
        else:
            from gpio_mock import GPIOMock as GPIO

        # need to set the board mode before doing anything with the pins
        GPIO.setmode(GPIO.BCM)

        test_setup(odisseus_configuration=odisseus_configuration)
        test_assign_msg(odisseus_configuration=odisseus_configuration)

        print("Done Executing Ultrasound Tests...")
        print("============================")
        print("============================")

    except Exception as e:
        print("An exception occured whilst running the test..." + str(e))
    finally:
        print("Cleaning up GPIO")


if __name__ == '__main__':
    from odisseus_config import odisseus_config_obj
    test(odisseus_config_obj)
