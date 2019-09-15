"""
CMDExecutor class: Given a robot and a queue of commands
it applies the CMDs on the robot
"""


class CMDExecutor:

    def __init__(self, cmd_queue, odisseus=None):
        self._cmd_queue = cmd_queue
        self._odisseus = odisseus

    def set_odisseus_instance(self, odisseus):
        """
        Set the instance of odisseus
        """
        self._odisseus = odisseus

    def run(self):

        if self._cmd_queue.empty() is not True:

            # get the next available CMD
            cmd = self._cmd_queue.get()

            if cmd.get_name() == 'PropulsionCmd':
                self._handle_propulsion_cmd(cmd=cmd)
            else:
                raise ValueError("Can only handle PropulsionCmd currently...")

            print("executed cmd")

    def add_cmd(self, cmd):
        """
         Add a new CMD to be queued for execution
        """

        if cmd is None:
            raise ValueError('Cannot queue None cmd...')

        self._cmd_queue.put(cmd)

    def _handle_propulsion_cmd(self, cmd):
        """
        Handle the propulsion CMD
        """

        if cmd.get_direction() == "STOP":
            self._odisseus.stop_raw()

        elif cmd.get_direction() == "FWD":
            self._odisseus.move_fwd_raw(cmd.get_speed_value(), **{'time': cmd.get_duration()})

        elif cmd.get_direction() == "REVERSE":
            self._odisseus.move_reverse_raw(cmd.get_speed_value(), **{'time': cmd.get_duration()})

        elif cmd.get_direction() == "LEFT":
            self._odisseus.move_left_raw(cmd.get_speed_value(), **{'time': cmd.get_duration()})

        elif cmd.get_direction() == "RIGHT":
            self._odisseus.move_right_raw(cmd.get_speed_value(), **{'time': cmd.get_duration()})

