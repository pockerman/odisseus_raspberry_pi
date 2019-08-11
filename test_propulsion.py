import time

from propulsion import Propulsion


def test_move_fwd():

    print("Move FWD test...")
    prop = Propulsion()
    prop.forward()
    time.sleep(0.5)
    prop.stop()


def test_move_bwd():

    print("Move BWD test...")
    prop = Propulsion()
    prop.reverse()
    time.sleep(0.5)
    prop.stop()


if __name__ == '__name__':
    test_move_fwd()
    test_move_bwd()