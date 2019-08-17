import time

from config import IN_PIN_1_MOTOR_1
from config import IN_PIN_2_MOTOR_1
from propulsion_two_motors  import Propulsion2Motors


def test_move_fwd():

    print("Move FWD test...")
    prop = Propulsion2Motors(in_pin_1_motor_1 = IN_PIN_1_MOTOR_1, in_pin_2_motor_1 = IN_PIN_2_MOTOR_1, in_pin_1_motor_2 = None, in_pin_2_motor_2=None)
    prop.forward(10)
    time.sleep(2)
    prop.stop()


def test_move_bwd():

    print("Move BWD test...")
    prop = Propulsion2Motors(in_pin_1_motor_1 = IN_PIN_1_MOTOR_1, in_pin_2_motor_1 = IN_PIN_2_MOTOR_1, in_pin_1_motor_2 = None, in_pin_2_motor_2=None)
    prop.reverse()
    time.sleep(2)
    prop.stop()


if __name__ == '__main__':
    test_move_fwd()
    test_move_bwd()