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

from odisseus import Odisseus
from propulsion import PropulsionParams
from control_cmds import PropulsionCmd

app = Flask(__name__)
odisseus = None

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

    if request.method == 'POST':

        # find out the direction and speed for creating the CMD
        direction = request.form.get('direction')
        print(direction)
        speed = request.form.get('speed')

        print("direction: ", direction)
        print("speed: ", speed)

        prop_cmd = PropulsionCmd(direction=direction, speed_value=int(speed))
        odisseus.add_cmd(copy.deepcopy(prop_cmd))

    return render_template(PROPULSION_CONTROL_TEMPLATE_NAME)


@app.route('/control/interrupt')
def interrupt_control():
    odisseus.interrupt()
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

    #control_queue.put(control_name)
    return Response('Error...')



if __name__ == '__main__':

    try:
        prop_params = PropulsionParams(in_pin_1_motor_1=IN_PIN_1_MOTOR_1, in_pin_2_motor_1=IN_PIN_2_MOTOR_1, en_pin_motor_1=ENA_MOTOR_1_PIN_ID,
                                   in_pin_1_motor_2=None, in_pin_2_motor_2=None, en_pin_motor_2=None)

        # initialize Odisseus
        print("Initializing Odisseus")
        odisseus = Odisseus(cmd_queue=control_queue, prop_params=prop_params)

        odiseus_process = Process(target=odisseus.run, kwargs={})
        odiseus_process.start()

        app.run(host=HOST, debug=DEBUG, port=PORT)
    finally:
        odiseus_process.terminate()