import time
import RPi.GPIO as GPIO

from config import IN_PIN_1_MOTOR_1
from config import IN_PIN_2_MOTOR_1
from config import ENA_MOTOR_1_PIN_ID
from propulsion_two_motors  import Propulsion2Motors


def test_move_fwd():

    print("Move FWD test...")
    prop = Propulsion2Motors(in_pin_1_motor_1 = IN_PIN_1_MOTOR_1, in_pin_2_motor_1 = IN_PIN_2_MOTOR_1, en_pin_motor_1=ENA_MOTOR_1_PIN_ID,
                             in_pin_1_motor_2 = None, in_pin_2_motor_2=None)
    prop.forward(10)
    time.sleep(2)
    #GPIO.cleanup()
    prop.stop()


def test_move_bwd():

    print("Move BWD test...")
    prop = Propulsion2Motors(in_pin_1_motor_1 = IN_PIN_1_MOTOR_1, in_pin_2_motor_1 = IN_PIN_2_MOTOR_1, en_pin_motor_1=ENA_MOTOR_1_PIN_ID,
                             in_pin_1_motor_2 = None, in_pin_2_motor_2=None)
    prop.backward()
    time.sleep(2)
    #GPIO.cleanup()
    prop.stop()


if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)

    test_move_fwd()
    GPIO.cleanup()

    GPIO.setmode(GPIO.BCM)
    test_move_bwd()
    GPIO.cleanup()