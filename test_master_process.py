"""
Unit tests for master process
"""

from master_process import MasterProcess
from pid import PIDControl

"""
Test Scenario: Application starts Odisseus MasterProcess
Expected Output: All Odisseus processes should be started
"""
def test_create_processes(odisseus_config_obj):

    error_msg = "No Erro in test"+test_create_processes.__name__
    master = MasterProcess(odisseus_configuration=odisseus_config_obj)

    pid_control = PIDControl(Kp = odisseus_config_obj.PROPULSION_PID_Kp, Ki=odisseus_config_obj.PROPULSION_PID_Ki, Kd=odisseus_config_obj.PROPULSION_PID_Kd)
    kwargs = dict()
    kwargs[odisseus_config_obj.PROPULSION_CONTROLLER_NAME] = pid_control
    master.create_processes(**kwargs)

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


def test(odisseus_configuration):
    errors = []
    error_msg = test_create_processes(odisseus_config_obj=odisseus_configuration)

    if error_msg[0:5] == "ERROR":
        errors.append(error_msg)

    if len(errors) != 0:
        print("ERRORS Occurred")

        for error in errors:
            print(error)

if __name__ == '__main__':

    from odisseus_config import odisseus_config_obj
    test(odisseus_configuration=odisseus_config_obj)

