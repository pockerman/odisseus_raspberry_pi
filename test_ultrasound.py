def test(odisseus_configuration):

    try:

        print("============================")
        print("Executing Ultrasound Tests")
        print("Done Executing Ultrasound Tests")
        print("============================")

    except Exception as e:
        print("An exception occured whilst running the test..." + str(e))
    finally:
        print("Cleaning up GPIO")


if __name__ == '__main__':
    from odisseus_config import odisseus_config_obj
    test(odisseus_config_obj)
