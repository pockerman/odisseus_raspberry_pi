import time
from odisseus_config import ON_RASP_PI

if ON_RASP_PI:
    import RPi.GPIO as GPIO
else:
    from gpio_mock import GPIOMock as GPIO

from odisseus_config import IN_PIN_1_MOTOR_1
from odisseus_config import IN_PIN_2_MOTOR_1
from odisseus_config import ENA_MOTOR_1_PIN_ID
from propulsion  import Propulsion
from propulsion import PropulsionParams


def test_move_fwd():

    print("Move FWD test...")
    params = PropulsionParams(in_pin_1_motor_1 = IN_PIN_1_MOTOR_1,
                             in_pin_2_motor_1 = IN_PIN_2_MOTOR_1,
                             en_pin_motor_1=ENA_MOTOR_1_PIN_ID,
                             in_pin_1_motor_2 = None, in_pin_2_motor_2=None, en_pin_motor_2=None)

    prop = Propulsion(params=params)

    #p = GPIO.PWM(ENA_MOTOR_1_PIN_ID, 1000)
    #p.start(100)
    prop.forward(speed=100)
    #time.sleep(5)
    prop.stop()


def test_move_bwd():

    print("Move BWD test...")
    params = PropulsionParams(in_pin_1_motor_1=IN_PIN_1_MOTOR_1,
                              in_pin_2_motor_1=IN_PIN_2_MOTOR_1,
                              en_pin_motor_1=ENA_MOTOR_1_PIN_ID,
                              in_pin_1_motor_2=None, in_pin_2_motor_2=None, en_pin_motor_2=None)

    prop = Propulsion(params=params)
    p = GPIO.PWM(ENA_MOTOR_1_PIN_ID, 1000)
    p.start(100)
    prop.backward(speed=100)
    time.sleep(2)
    prop.stop()


if __name__ == '__main__':

    try:

        print("============================")
        print("Executing Propulsion Tests")

        GPIO.setmode(GPIO.BCM)
        test_move_fwd()
        GPIO.cleanup()

        GPIO.setmode(GPIO.BCM)
        test_move_bwd()
        #GPIO.cleanup()

        print("Done Executing Propulsion Tests")
        print("============================")
    except Exception as e:
        print("An exception occured whilst runnning the test..." + str(e))
    finally:
        GPIO.cleanup()
