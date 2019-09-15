"""
class  Odisseus: API for controlling Odisseus
"""


class Odisseus:
    """
    class that models Odisseus. This is the
    class that applications should use to instruct
    Odisseus to do its tasks
    """

    def __init__(self, odisseus_config, propulsion, cmd_executor):

        self._odisseus_config = odisseus_config
        self._cmd_executor = cmd_executor
        self._interrupted = False
        self._propulsion = propulsion

    def set_cmd_executor(self, cmd_executor):
        """
        Set the instance of the cmd executor
        """
        self._cmd_executor = cmd_executor

    def run(self):
        """
        Runs Odisseus indefinitely until the interrupt flag is set
        """
        while self._interrupted is not True:

            # get a CMD off the queue and execute it
            self._cmd_executor.run()

        if self._interrupted:
            print("Odisseus was interrupted")

    def add_cmd(self, cmd):
        """
        Add a new CMD for the robot to be excuted
        """
        self._cmd_executor.add_cmd(cmd)

    def interrupt(self):
        """
        Signal Odisseus for interrupt
        """
        if self._odisseus_config.ENABLE_WARNINGS:
            print("Odisseus was interrupted...")
        self._interrupted = True

    def remove_interrupt(self):
        """
        Set the interrupt flag to false
        """
        if self._odisseus_config.ENABLE_WARNINGS and self._interrupted == True:
            print("Odisseus has interrupt flag removed...")

        self._interrupted = False

    def stop_raw(self, **kwargs):
        """
        Stop Odisseus from moving
        """
        self._propulsion.stop()

    def move_fwd_raw(self, speed, **kwargs):
        """
        Move Odisseus fwd with the given speed
        """
        self._propulsion.forward(speed, **kwargs)

    def move_reverse_raw(self, speed, **kwargs):
        """
        Move Odisseus backward with the given speed
        """
        self._propulsion.backward(speed, **kwargs)

    def move_left_raw(self, speed, **kwargs):
        """
        Turn Odisseus left with the given speed
        """
        self._propulsion.left(speed, **kwargs)

    def move_right_raw(self, speed, **kwargs):
        """
        Turn Odisseus right with the given speed
        """
        self._propulsion.right(speed, **kwargs)




