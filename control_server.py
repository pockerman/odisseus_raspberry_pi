"""
Main module for controlling Odisseus via web
"""

from flask import Flask
from flask import render_template
from flask import Response

from config import HOST
from config import DEBUG
from config import PORT
from config import CONTROL_SERVER_INDEX_TEMPLATE_NAME
from config import PROPULSION_CONTROL_TEMPLATE_NAME

app = Flask(__name__)


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


@app.route('/control/propulsion-control')
def propulsion_control_view():
    return render_template(PROPULSION_CONTROL_TEMPLATE_NAME)


@app.route('/control/<control_name>')
def control(control_name):
    """
    Returns the view for the control
    :param control_name:
    :return:
    """

    if control_name == 'propulsion':
        return propulsion_control_view()

    #control_queue.put(control_name)
    return Response('Error...')



if __name__ == '__main__':
    app.run(host=HOST, debug=DEBUG, port=PORT)
