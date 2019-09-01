"""
Main module for controlling Odisseus via web
"""

import copy
from multiprocessing import Process

from flask import Flask
from flask import render_template
from flask import Response
from flask import request

# configuration parameters
from config import HOST
from config import DEBUG
from config import PORT
from config import CONTROL_SERVER_INDEX_TEMPLATE_NAME
from config import PROPULSION_CONTROL_TEMPLATE_NAME
from config import IN_PIN_1_MOTOR_1
from config import IN_PIN_2_MOTOR_1
from config import ENA_MOTOR_1_PIN_ID
from config import control_queue
from config import ENABLE_LOG

from odisseus import Odisseus
from propulsion import PropulsionParams
from control_cmds import PropulsionCmd

app = Flask(__name__)


class ControlServer:

    def __init__(self):

        self.__odisseus = None
        self.__odisseus_process = None

    def start(self, prop_params):

        self.__odisseus = Odisseus(cmd_queue=control_queue, prop_params=prop_params)
        self.spawn_odisseus_process()

    def spawn_odisseus_process(self):
        """
        Spawns a new process for Odisseus. Assumes that the
        odisseus robot has been created
        """

        if self.__odisseus is None:
                if  ENABLE_LOG:
                    print("Cannot spawn an odisseus process when Odisseus is None")
                return

        # is there a reason to spawn the process if it is active?
        if self.__odisseus_process is not None and self.__odisseus_process.is_alive():
            if ENABLE_LOG:
                print("Odisseus process is alive nothing to do here...")
            return

        # there is no point to start a new procees if Odisseus
        # is interrupted
        self.__odisseus.remove_interrupt()
        self.__odisseus_process = Process(target=self.__odisseus.run, kwargs={})
        self.__odisseus_process.start()

        if ENABLE_LOG:
            print("Spawn a new Odisseus process...")

    def add_cmd(self, cmd):
        self.__odisseus.add_cmd(copy.deepcopy(cmd))

    def terminate_odisseus_process(self):

        if self.__odisseus_process is not None:
            self.__odisseus_process.terminate()
            self.__odisseus_process = None

        # there is not control so be safe
        self.__odisseus.interrupt()
        self.__odisseus.stop_raw()

# the control server used
control_server = ControlServer()


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

    #control_queue.put(control_name)
    return Response('Error...')


if __name__ == '__main__':

    try:


        prop_params = PropulsionParams(in_pin_1_motor_1=IN_PIN_1_MOTOR_1, in_pin_2_motor_1=IN_PIN_2_MOTOR_1, en_pin_motor_1=ENA_MOTOR_1_PIN_ID,
                                       in_pin_1_motor_2=None, in_pin_2_motor_2=None, en_pin_motor_2=None)

        # initialize Odisseus
        if ENABLE_LOG:
            print("Initializing Odisseus...")

        #control_server = ControlServer()
        control_server.start(prop_params=prop_params)

        # finally start the web application
        app.run(host=HOST, debug=DEBUG, port=PORT)

    finally:

        control_server.terminate_odisseus_process()