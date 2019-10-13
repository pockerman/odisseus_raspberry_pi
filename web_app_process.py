"""
Main module for controlling Odisseus via web
"""
import sys, getopt

from flask import Flask
from flask import render_template
from flask import Response
from flask import request

# configuration parameters
from odisseus_config import odisseus_config_obj

HOST = odisseus_config_obj.HOST
DEBUG = odisseus_config_obj.DEBUG
PORT = odisseus_config_obj.PORT
CONTROL_SERVER_INDEX_TEMPLATE_NAME =  odisseus_config_obj.CONTROL_SERVER_INDEX_TEMPLATE_NAME
PROPULSION_CONTROL_TEMPLATE_NAME = odisseus_config_obj.PROPULSION_CONTROL_TEMPLATE_NAME

IN_PIN_1_MOTOR_1 = odisseus_config_obj.IN_PIN_1_MOTOR_1
IN_PIN_2_MOTOR_1 = odisseus_config_obj.IN_PIN_2_MOTOR_1
ENA_MOTOR_1_PIN_ID = odisseus_config_obj.ENA_MOTOR_1_PIN_ID
IN_PIN_1_MOTOR_2 = odisseus_config_obj.IN_PIN_1_MOTOR_2
IN_PIN_2_MOTOR_2 = odisseus_config_obj.IN_PIN_2_MOTOR_2
ENA_MOTOR_2_PIN_ID = odisseus_config_obj.ENA_MOTOR_2_PIN_ID

ENABLE_LOG = odisseus_config_obj.ENABLE_LOG
control_queue = odisseus_config_obj.control_queue

from propulsion_process import PropulsionProcess
from propulsion import PropulsionParams
from propulsion import Propulsion
from control_cmds import PropulsionCmd


app = Flask(__name__)

# the control server used
control_server = PropulsionProcess(odisseus_config=odisseus_config_obj)


@app.route('/')
def index():
    """
    Function that serves the index view
    """
    return render_template(CONTROL_SERVER_INDEX_TEMPLATE_NAME)


"""
@app.route('/display')
def display():
    if USE_MULTIPROCESSING:
        return Response(frame_generator_from_queue(display_queue=display_queue, sleep_time=CAMERA_SLEEP_TIME),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return  Response(frame_generator(rotation=NEEDED_CAMERA_ROTATION, sleep_time=CAMERA_SLEEP_TIME),
                         mimetype='multipart/x-mixed-replace; boundary=frame')
"""


@app.route('/control/propulsion-control', methods=['GET', 'POST'])
def propulsion_control_view():

    """
    Returns the view for the propulsion control
    """

    if request.method == 'POST':

        # find out the direction and speed for creating the CMD
        direction = request.form.get('direction')
        speed = request.form.get('speed')
        duration = request.form.get("duration")

        if ENABLE_LOG:
            print("direction: ", direction)
            print("speed: ", speed)
            print("duration: ", duration)

        prop_cmd = PropulsionCmd(direction=direction, speed_value=int(speed), duration=int(duration))
        control_server.add_cmd(cmd=prop_cmd)

    return render_template(PROPULSION_CONTROL_TEMPLATE_NAME)


@app.route('/control/interrupt')
def interrupt_control():
    """
    Terminates the instance that Odisseus is running on
    """
    control_server.terminate_odisseus_process()
    return index()


@app.route('/control/start')
def start_control():
    """
    Recreates the Odisseus process
    """
    control_server.spawn_odisseus_process()
    return index()


@app.route('/control/<control_name>')
def control(control_name):
    """
    Returns the view for the control
    """

    if control_name == 'propulsion':
        return propulsion_control_view()
    elif control_name == 'interrupt':
        return interrupt_control()
    elif control_name == 'start':
        return start_control()

    return Response('Error...')


def start_odisseus_web_app():

    try:

        opts, args = getopt.getopt(sys.argv, ["PLATFORM"])

        if len(args) >= 2 and args[1].split('=')[1] == 'Ubuntu':
            odisseus_config_obj.ON_RASP_PI = False

        # reset the mode
        control_server.reset_mode()

        prop_params = PropulsionParams(in_pin_1_motor_1=IN_PIN_1_MOTOR_1, in_pin_2_motor_1=IN_PIN_2_MOTOR_1, en_pin_motor_1=ENA_MOTOR_1_PIN_ID,
                                       in_pin_1_motor_2=IN_PIN_1_MOTOR_2, in_pin_2_motor_2=IN_PIN_2_MOTOR_2, en_pin_motor_2=ENA_MOTOR_2_PIN_ID)

        propulsion = Propulsion(odisseus_config=odisseus_config_obj, params=prop_params)
        #cmd_executor = CMDExecutor(cmd_queue=control_queue)

        # initialize Odisseus
        if ENABLE_LOG:
            print("Initializing Odisseus...")

        control_server.start(propulsion=propulsion) # cmd_executor=cmd_executor)

        # finally start the web application
        app.run(host=HOST, debug=DEBUG, port=PORT)

    finally:

        control_server.terminate_odisseus_process()
        control_server.cleanup_pins()


if __name__ == '__main__':
    start_odisseus_web_app()
