"""
class  Odisseus: API for controlling Odisseus
"""


class Odisseus:
    """
    class that models Odisseus. This is the
    class that applications should use to instruct
    Odisseus to do its tasks
    """

    def __init__(self, odisseus_config, propulsion, cmd_queue):

        self._odisseus_config = odisseus_config
        self._cmd_queue = cmd_queue
        self._interrupted = False
        self._propulsion = propulsion

    def run(self):
        """
        Runs Odisseus indefinitely until the interrupt flag is set
        """
        while self._interrupted is not True:

            # get a CMD off the queue and execute it
            if self._cmd_queue.empty() != True :
                cmd = self._cmd_queue.get()
                cmd.execute(robot=self)
                print("executed cmd")
            #elif ENABLE_WARNINGS:
            #    print("CMD Queue is empty...")

        if self._interrupted:
            print("Odisseus was interrupted")

    def add_cmd(self, cmd):
        """
        Add a new CMD for the robot to be excuted
        """
        self._cmd_queue.put(cmd)

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

    def stop_raw(self):
        """
        Stop Odisseus from moving
        """
        self._propulsion.stop()

    def move_fwd_raw(self, speed):
        """
        Move Odisseus fwd with the given speed
        """
        self._propulsion.forward(speed)

    def move_reverse_raw(self, speed):
        """
        Move Odisseus backward with the given speed
        """
        self._propulsion.backward(speed)

    def move_left_raw(self, speed):
        """
        Turn Odisseus left with the given speed
        """
        self._propulsion.left(speed)

    def move_right_raw(self, speed):
        """
        Turn Odisseus right with the given speed
        """
        self._propulsion.right(speed)




