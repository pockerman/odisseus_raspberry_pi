"""
Base class for deriving process control
"""

class ProcessControlBase(object):

    def __init__(self, config, name):
        self._config = config
        self._name = name
        self._process = None
        self._interrupted = False

    def set_config(self, config):
        self._config = config

    def interrupt(self):
        """
        Signal the process for interrupt
        """
        if self._config["ENABLE_WARNINGS"]:
            print("Process: " + self._name + " was interrupted...")
        self._interrupted = True

    def remove_interrupt(self):
        """
        Set the interrupt flag to false
        """
        if self._config["ENABLE_WARNINGS"] and self._interrupted is True:
            print("Process: "+self._name+" has interrupt flag removed...")
        self._interrupted = False

    def is_interrupted(self):
        return self._interrupted

    def is_alive(self):

        if self._process is not None:
            return self._process.is_alive()

        return False

    def get_name(self):
        return self._name

    def get_config(self):
        return self._config

    def set_process(self, proc):
        self._process = proc

    def start(self, **kwargs):

        if self._process is not None:
            self._process.start()

            if self.get_config()["ENABLE_LOG"]:
                print("Spawn a new " + self.get_name() + " process...")
        else:
            raise Exception("Low level  process instance is None")

    def stop(self):

        if self._process is not None:
            self._process.terminate()
            self._process = None

