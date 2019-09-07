"""
Configuration file for Odisseus
"""

# Flag indicating if we are on Pi or simply emulating
ON_RASP_PI = False

if ON_RASP_PI:
    import cv2



DEBUG = True
ENABLE_LOG = True
ENABLE_WARNINGS = True
PORT =  5001
HOST = '0.0.0.0'

# The address of the I2C bus
I2CAddr = 0x00000000


SCREEN_SIZE = (320, 240)

if ON_RASP_PI:
    ENCODE_PARAMS = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    
INDEX_DISPLAY_TEMPLATE_NAME = 'image_server.html'
CONTROL_SERVER_INDEX_TEMPLATE_NAME = 'control_server_index.html'
PROPULSION_CONTROL_TEMPLATE_NAME = 'propulsion_control.html'
CAMERA_SLEEP_TIME = 0.05
NEEDED_CAMERA_ROTATION = 0.0

# configuration for multiprocessing
USE_MULTIPROCESSING = False
QUEUE_MAX_SIZE=2

display_queue = None
control_queue = None

from multiprocessing import Queue

control_queue = Queue()
display_queue = Queue(maxsize=QUEUE_MAX_SIZE)


# the Pins Odisseus is using

IN_PIN_1_MOTOR_1 = 23
IN_PIN_2_MOTOR_1 = 24
ENA_MOTOR_1_PIN_ID = 25
IN_PIN_1_MOTOR_2 = None
IN_PIN_2_MOTOR_2 = None
ENA_MOTOR_2_PIN_ID = None
#IN_PIN_3 = 20
#IN_PIN_4 = 21

# the IR sensor PIN ID
IR_PIN_ID = None #18

