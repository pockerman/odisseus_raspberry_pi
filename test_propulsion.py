from propulsion  import Propulsion
from propulsion import PropulsionParams


def test_move_fwd(prop, **kwargs):
    """
    Test Scenario: Application starts the propulsion system in the forward direction.
    """

    print("Move FWD test...")
    prop.forward(speed=100, **kwargs)
    prop.stop()


def test_move_bwd(prop, **kwargs):
    """
    Test Scenario: Application starts the propulsion system in the backward direction.
    """

    print("Move BWD test...")
    prop.backward(speed=100, **kwargs)
    prop.stop()


def test_move_right(prop, **kwargs):

    """
    Test Scenario: Application starts the propulsion system by generating right turn motion.
    """

    print("Move Right test...")
    prop.right(speed=100, **kwargs)
    prop.stop()


def test_move_left(prop, **kwargs):

    """
    Test Scenario: Application starts the propulsion system by generating left turn motion.
    """

    print("Move Left test...")
    prop.left(speed=100, **kwargs)
    prop.stop()


def test(odisseus_configuration):

    try:

        print("============================")
        print("Executing Propulsion Tests")

        if odisseus_configuration.ON_RASP_PI:
            import RPi.GPIO as GPIO
        else:
            from gpio_mock import GPIOMock as GPIO

        # need to set the board mode before doing anything with the pins
        GPIO.setmode(GPIO.BCM)

        kwargs = {'time': 2}
        params = PropulsionParams(in_pin_1_motor_1=odisseus_configuration.IN_PIN_1_MOTOR_1,
                                  in_pin_2_motor_1=odisseus_configuration.IN_PIN_2_MOTOR_1,
                                  en_pin_motor_1=odisseus_configuration.ENA_MOTOR_1_PIN_ID,
                                  in_pin_1_motor_2=odisseus_configuration.IN_PIN_1_MOTOR_2,
                                  in_pin_2_motor_2=odisseus_configuration.IN_PIN_2_MOTOR_2,
                                  en_pin_motor_2=odisseus_configuration.ENA_MOTOR_2_PIN_ID)


        prop = Propulsion(odisseus_config=odisseus_configuration, params=params)

        test_move_fwd(prop=prop, **kwargs)

        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        # since we called cleanup above we need to setup the pins again
        prop.setup()
        test_move_bwd(prop=prop, **kwargs)

        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        # since we called cleanup above we need to setup the pins again
        prop.setup()
        test_move_right(prop=prop, **kwargs)

        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        # since we called cleanup above we need to setup the pins again
        prop.setup()
        test_move_left(prop=prop, **kwargs)

        print("Done Executing Propulsion Tests")
        print("============================")

    except Exception as e:
        print("An exception occured whilst runnning the test..." + str(e))
    finally:
        print("Cleaning up GPIO")
        GPIO.cleanup()


if __name__ == '__main__':
    from odisseus_config import odisseus_config_obj
    test(odisseus_config_obj)
