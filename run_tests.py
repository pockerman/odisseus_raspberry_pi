
import sys, getopt
from odisseus_config import odisseus_config_obj


def run():

    try:
        # read in the user properties
        opts, args = getopt.getopt(sys.argv, ["PLATFORM", "ID"])

        if len(args) < 3 :
            raise ValueError("Invalid number of input arguments")

        if args[1].split('=')[1]=='Ubuntu':
            odisseus_config_obj.ON_RASP_PI = False

        if args[2].split('=')[1]=='1':
            import test_propulsion # do the import here as the ON_RASP_PI flag may not have been set
            test_propulsion.test(odisseus_configuration=odisseus_config_obj)

    except getopt.GetoptError as e:
        print(str(e))
        sys.exit(2)
    except:
        print("Unknown error occured whilst running the tests...")
        sys.exit(2)


if __name__ == '__main__':
    run()
