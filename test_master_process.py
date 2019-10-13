"""
Unit tests for master process
"""

import sys
import getopt

from odisseus_config import odisseus_config_obj
from master_process import MasterProcess

"""
Test Scenario: Application starts Odisseus MasterProcess
Expected Output: All Odisseus processes should be started
"""
def test_create_processes(odisseus_config_obj):

    error_msg = "No Erro in test"+test_create_processes.__name__
    master = MasterProcess(odisseus_configuration=odisseus_config_obj)
    master.create_processes()

    names = master.get_processes_names()

    count = 0

    if odisseus_config_obj.ENABLE_IR_SENSOR:
        count += 1

    if odisseus_config_obj.ENABLE_CAMERA:
        count += 1

    if odisseus_config_obj.ENABLE_MOTORS:
        count +=1

    if odisseus_config_obj.ENABLE_ULTRASOUND_SENSOR:
        count += 1

    if odisseus_config_obj.ENABLE_WEB_SERVER:
        count += 1

    master.terminate_all_processes()
    if count != len(names):
        error_msg = "ERROR in {0}: Not all processes were started. Should be {1} but started only {2} ".format(test_create_processes.__name__, count, len(names))

    return error_msg


if __name__ == '__main__':

    opts, args = getopt.getopt(sys.argv, ["PLATFORM",])

    print(args)

    if len(args) == 2:
        PLATFORM = args[1].split('=')[1]

        if PLATFORM == 'Ubuntu':
            odisseus_config_obj.ON_RASP_PI = False

    errors = []
    error_msg = test_create_processes(odisseus_config_obj=odisseus_config_obj)

    if error_msg[0:5] == "ERROR":
        errors.append(error_msg)

    if len(errors) != 0:
        print("ERRORS Occurred")

        for error in errors:
            print(error)