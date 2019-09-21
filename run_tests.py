"""
Run all the tests or run a specified test [1, 2, 3, 4, 5]
"""
import sys, getopt
from odisseus_config import odisseus_config_obj


def run():

    try:
        # read in the user properties
        opts, args = getopt.getopt(sys.argv, ["PLATFORM", "ID"])

        if len(args) < 3 :
            raise ValueError("Invalid number of input arguments")

        print("First argument given: ", args[1])
        print("Second argument given: ", args[2])

        if args[1].split('=')[1]=='Ubuntu':
            odisseus_config_obj.ON_RASP_PI = False

        if args[2].split('=')[1]=='1':
            import test_propulsion
            test_propulsion.test(odisseus_configuration=odisseus_config_obj)

        if args[2].split('=')[1]=='2':
            print("IR tests are not here yet...")

        if args[2].split('=')[1]=='3':
            import test_ultrasound
            test_ultrasound.test(odisseus_configuration=odisseus_config_obj)

        if args[2].split('=')[1]=='4':
            print("Camera tests are not here yet...")

        if args[2].split('=')[1]=='5':
            import test_propulsion
            test_propulsion.test(odisseus_configuration=odisseus_config_obj)
            import test_ultrasound
            test_ultrasound.test(odisseus_configuration=odisseus_config_obj)

    except getopt.GetoptError as e:
        print(str(e))
        sys.exit(2)
    except ValueError as e:
        print(str(e))
        sys.exit(2)
    except:
        print("Unknown error occured whilst running the tests...")
        sys.exit(2)


if __name__ == '__main__':
    run()
