from config.config import ENABLE_WARNINGS
from propulsion import Propulsion


class Odisseus:
    """
    class that models Odisseus. This is the
    class that applications should use to instruct
    Odisseus to do its tasks
    """

    def __init__(self, cmd_queue, prop_params):
        self.__cmd_queue = cmd_queue
        self.__interrupted = False
        self.__propulsion = Propulsion(params=prop_params)


    def run(self):

        """
        Runs Odisseus indefinitely
        """

        while(self.__interrupted == False):

            # get a CMD off the queue and execute it
            if( self.__cmd_queue.empty() != True ):
                cmd = self.__cmd_queue.get()
                cmd.execute(robot=self)
                print("executed cmd")
            #elif ENABLE_WARNINGS:
            #    print("CMD Queue is empty...")

        if(self.__interrupted):
            print("Odisseus was interrupted")

    def add_cmd(self, cmd):
        """
        Add a new CMD for the robot to be excuted
        """
        self.__cmd_queue.put(cmd)

    def interrupt(self):
        """
        Signal Odisseus for interrupt
        """
        if ENABLE_WARNINGS:
            print("Odisseus was interrupted...")
        self.__interrupted = True

    def remove_interrupt(self):

        """
        Set the interrupt flag to false
        """

        if ENABLE_WARNINGS and self.__interrupted == True:
            print("Odisseus has interrupt removed...")
        self.__interrupted = False

    def stop_raw(self):
        self.__propulsion.stop()

    def move_fwd_raw(self, speed):
        self.__propulsion.stop()
        self.__propulsion.forward(speed)

    def move_reverse_raw(self, speed):
        self.__propulsion.stop()
        self.__propulsion.backward(speed)

    def move_left_raw(self, speed):
        self.__propulsion.stop()
        self.__propulsion.left(speed)

    def move_right_raw(self, speed):
        self.__propulsion.stop()
        self.__propulsion.right(speed)




