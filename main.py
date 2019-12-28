"""
Main driver for Odisseus
"""

from odisseus_config import odisseus_config_obj
from master_process import MasterProcess

def main():

    """
    Main driver for Odisseus
    """

    if odisseus_config_obj.ON_RASP_PI:
        import RPi.GPIO as GPIO
    else:
        from gpio_mock import GPIOMock as GPIO

    # need to set the board mode before doing anything with the pins
    GPIO.setmode(GPIO.BCM)

    master = MasterProcess(odisseus_configuration=odisseus_config_obj)
    master.create_processes()
    master.run()

    # once done clean up the pins
    GPIO.cleanup()


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        if odisseus_config_obj.ON_RASP_PI:
            import RPi.GPIO as GPIO
        else:
            from gpio_mock import GPIOMock as GPIO
        GPIO.cleanup()