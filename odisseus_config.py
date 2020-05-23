"""
Configuration file for Odisseus
"""

from multiprocessing import Queue


class OdisseusConfig:

    """
    Configuration class for Odisseus
    """

    # The name of the MasterProcess
    MASTER_PROCESS_NAME = "MasterProcess"

    # The name of the DecisionMakerProcess
    DECISION_MAKER_PROCESS_NAME = "DecisionMakerProcess"

    # Flag indicating if we are on Pi or simply emulating
    ON_RASP_PI = True

    # sample the sensors very SAMPLE_RATE
    SAMPLING_RATE = 0.5

    # The radius of the wheels (m)
    WHEELS_RADIUS = 2.5/100.0

    # various levels of info to record
    DEBUG = True
    ENABLE_LOG = True
    ENABLE_WARNINGS = True

    # which sensors to enable
    ENABLE_ULTRASOUND_SENSOR = True
    ENABLE_MOTORS = True
    ENABLE_WEB_SERVER = True
    ENABLE_CAMERA = False
    ENABLE_IR_SENSOR = False

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

    # Max frequency for motor PWM
    MOTOR_PWM_FREQUENCY = 1000

    # Maximum duty cycle
    MAX_DUTY_CYCLE = 100

    # Front right Motor Pins
    IN_PIN_1_MOTOR_1 = 23 # Board pin 16
    IN_PIN_2_MOTOR_1 = 24 # Board pin 18
    ENA_MOTOR_1_PIN_ID = 25 # Board pin 22

    # Front left Motor Pins
    IN_PIN_1_MOTOR_2 = 17 # Board pin 11
    IN_PIN_2_MOTOR_2 = 27 # Board pin 13
    ENA_MOTOR_2_PIN_ID = 22 # Board pin 15

    PROPULSION_PROCESS_NAME = "PropulsionProcess"

    # weights of PID controller for Propulsion
    PROPULSION_PID_Kp = 0.1
    PROPULSION_PID_Ki = 0.5
    PROPULSION_PID_Kd = 0.0
    PROPULSION_CONTROLLER_NAME = 'PropulsionProcessController'

    # the IR sensor PIN ID
    IR_PIN_ID = None  # 18

    # Ultrasound sensor pins
    TRIG_PIN = 6 # Board pin 31
    ECHO_PIN = 5 # Board pin 29
    SLEEP_TIME_FOR_SETTING_UP_ULTRA_SENSOR = 2
    ULTRA_SOUND_TRIGGER_PULSE_TIME = 0.00001
    MIN_DISTANCE_FROM_OBSTACLE = 15.0 # cm
    ULTRASOUND_PORT_MAX_SIZE = 20 # maximum size for the Ultrasound sensor port queue
    ULTRASOUND_SENSOR_PROCESS_NAME = "UltrasoundSensorProcess"

    WEB_PROCESS_NAME='WebApp'

    # global tolerance to use
    TOLERANCE = 1.0e-3

    # which method of fusion to use
    SENSOR_FUSION_METHOD = "KalmanFilter"

# the global configuration object for Odisseus
odisseus_config_obj = OdisseusConfig()





