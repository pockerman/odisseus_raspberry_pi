"""
Run all the tests or run a specified test [1, 2, 3, 4, 5]
"""
import sys, getopt
from odisseus_config import odisseus_config_obj

def get_test_id(platform_type, args):

    if platform_type == 'Ubuntu':
        return args[2].split('=')[1]

    return args[3].split('=')[1]

def run():

    try:
        # read in the user properties
        opts, args = getopt.getopt(sys.argv, ["PLATFORM", "ID"])

        if len(args) < 3 :
            raise ValueError("Invalid number of input arguments")

        print("First argument given: ", args[1])
        print("Second argument given: ", args[2])

        PLATFORM = args[1].split('=')[1]

        if PLATFORM =='Ubuntu':
            odisseus_config_obj.ON_RASP_PI = False

        test_id = get_test_id(platform_type=PLATFORM, args=args)

        if test_id =='1':
            print("Executing Propulsion tests")
            import test_propulsion
            test_propulsion.test(odisseus_configuration=odisseus_config_obj)

        if test_id =='2':
            print("IR tests are not here yet...")

        if test_id =='3':
            print("Executing Ultrasound tests")
            import test_ultrasound
            test_ultrasound.test(odisseus_configuration=odisseus_config_obj)

        if test_id =='4':
            print("Camera tests are not here yet...")

        if test_id == '5':
            print("Executing Master Process tests")
            import test_master_process
            test_master_process.test(odisseus_configuration=odisseus_config_obj)

        if test_id == '6':
            print("Executing Propulsion tests")
            import test_propulsion
            test_propulsion.test(odisseus_configuration=odisseus_config_obj)
            print("Executing Ultrasound tests")
            import test_ultrasound
            test_ultrasound.test(odisseus_configuration=odisseus_config_obj)
            print("Executing Master Process tests")
            import test_master_process
            test_master_process.test(odisseus_configuration=odisseus_config_obj)

    except getopt.GetoptError as e:
        print(str(e))
        sys.exit(2)
    except ValueError as e:
        print(str(e))
        sys.exit(2)
    except TypeError as e:
        print(str(e))
        sys.exit(2)
    except KeyError as e:
        print(str(e))
        sys.exit(2)
    except:
        print("Unknown error occured whilst running the tests...")
        sys.exit(2)


if __name__ == '__main__':
    run()
