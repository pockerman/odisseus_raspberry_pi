"""
Main module for controlling Odisseus via web
"""
import sys, getopt
from multiprocessing import Process

from flask import Flask
from flask import render_template
from flask import Response
from flask import request

from process_control_base import ProcessControlBase
from control_cmds import TerminateProcessCMD
from control_cmds import StartProcessCMD
from control_cmds import PropulsionCmd

app = Flask(__name__)
#web_app_process = None


@app.route('/')
def index():
    """
    Function that serves the index view
    """
    web_app_process = WebAppProcess.web_app_process

    if web_app_process is None:
        raise ValueError("WebApp process is None")

    return render_template(web_app_process.get_config().CONTROL_SERVER_INDEX_TEMPLATE_NAME)


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
    web_app_process = WebAppProcess.web_app_process

    if request.method == 'POST':

        # find out the direction and speed for creating the CMD
        speed = request.form.get('speed', None)
        duration = request.form.get("duration", None)
        direction = request.form.get('direction', None)

        if direction == 'STOP' or direction is None or direction == "":
            speed = 0
            direction = 'STOP'

        if duration is None or duration == "":
            duration = 0
            direction = 'STOP'
            speed = 0

        if web_app_process.get_config().ENABLE_LOG:

            print("direction: ", direction)
            print("speed: ", speed)
            print("duration: ", duration)

        prop_cmd = PropulsionCmd(direction=direction, speed_value=int(speed), duration=int(duration))
        web_app_process.add_propulsion_cmd(cmd=prop_cmd)
    return render_template(web_app_process.get_config().PROPULSION_CONTROL_TEMPLATE_NAME)


@app.route('/control/interrupt')
def interrupt_control():
    """
    Terminates the instance that Odisseus is running on
    """
    web_app_process = WebAppProcess.web_app_process
    web_app_process.terminate_odisseus_process()
    return index()


@app.route('/control/start')
def start_control():
    """
    Recreates the Odisseus process
    """
    web_app_process = WebAppProcess.web_app_process
    web_app_process.spawn_odisseus_process()
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


class WebAppProcess(ProcessControlBase):

    """
    The WebAppProcess allows for web control
    """

    web_app_process = None

    def __init__(self, odisseus_config, master_process):
        ProcessControlBase.__init__(self, config=odisseus_config,
                                    name=odisseus_config.WEB_PROCESS_NAME)
        self._master_process = master_process

    def start(self, **kwargs):

        """
        start the web server process
        """

        # is there a reason to spawn the process if it is active?
        if self.is_alive():
            if self.get_config().ENABLE_LOG:
                print(self.get_name() + " process is alive nothing to do here...")
            return

        self.remove_interrupt()
        WebAppProcess.web_app_process = self
        self.set_process(proc=Process(target=app.run, kwargs={"host": self.get_config().HOST,
                                                              "debug": self.get_config().DEBUG,
                                                              "port": self.get_config().PORT}))
        super(WebAppProcess, self).start(**kwargs)

    def terminate_odisseus_process(self):
        self._master_process.add_cmd(cmd = TerminateProcessCMD(process_name="PropulsionProcess"))

    def spawn_odisseus_process(self):
        self._master_process.add_cmd(cmd=StartProcessCMD(process_name="PropulsionProcess"))

    def add_propulsion_cmd(self, cmd):
        self._master_process.add_cmd(cmd=cmd)


if __name__ == '__main__':
    from odisseus_config import odisseus_config_obj
    from master_process import MasterProcess

    opts, args = getopt.getopt(sys.argv, ["PLATFORM", ])

    print(args)

    if len(args) == 2:
        PLATFORM = args[1].split('=')[1]

        if PLATFORM == 'Ubuntu':
            odisseus_config_obj.ON_RASP_PI = False

    master_process = MasterProcess(odisseus_configuration=odisseus_config_obj)
    master_process.start_process(proc_name=odisseus_config_obj.WEB_PROCESS_NAME)
    web_app_process = master_process.get_process("WebApp")

    if web_app_process is None:
        raise ValueError("Could not create web_app_process")

    master_process.run()

