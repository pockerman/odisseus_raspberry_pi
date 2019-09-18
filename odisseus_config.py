"""
Configuration file for Odisseus
"""

from multiprocessing import Queue


class OdisseusConfig:

    """
    Configuration class for Odisseus
    """

    # Flag indicating if we are on Pi or simply emulating
    ON_RASP_PI = True
    DEBUG = True
    ENABLE_LOG = True
    ENABLE_WARNINGS = True
    PORT = 5001
    HOST = '0.0.0.0'

    # The address of the I2C bus
    I2CAddr = 0x00000000
    SCREEN_SIZE = (320, 240)
    INDEX_DISPLAY_TEMPLATE_NAME = 'image_server.html'
    CONTROL_SERVER_INDEX_TEMPLATE_NAME = 'control_server_index.html'
    PROPULSION_CONTROL_TEMPLATE_NAME = 'propulsion_control.html'
    CAMERA_SLEEP_TIME = 0.05
    NEEDED_CAMERA_ROTATION = 0.0

    # configuration for multiprocessing
    USE_MULTIPROCESSING = False
    QUEUE_MAX_SIZE = 2

    control_queue = Queue()
    display_queue = Queue(maxsize=QUEUE_MAX_SIZE)

    # Max frequency for motor PWM
    MOTOR_PWM_FREQUENCY = 1000

    # Maximum duty cycle
    MAX_DUTY_CYCLE = 100

    # The Pins Odisseus is using. Pin IDs according to BCM
    PWM_PIN_ID = 18

    # Front right Motor Pins
    IN_PIN_1_MOTOR_1 = 23 # Board pin 16
    IN_PIN_2_MOTOR_1 = 24 # Board pin 18
    ENA_MOTOR_1_PIN_ID = 25 # Board pin 22

    # Front left Motor Pins
    IN_PIN_1_MOTOR_2 = 17 # Board pin 11
    IN_PIN_2_MOTOR_2 = 27 # Board pin 13
    ENA_MOTOR_2_PIN_ID = 22 # Board pin 15

    # the IR sensor PIN ID
    IR_PIN_ID = None  # 18

# the global configuration object for Odisseus
odisseus_config_obj = OdisseusConfig()

#if ON_RASP_PI:
#    import cv2

#if ON_RASP_PI:
#    ENCODE_PARAMS = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    



