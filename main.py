"""
Main driver for Odisseus
"""

from odisseus_config import odisseus_config_obj
from master_process import MasterProcess

def main():

    """
    Main driver for Odisseus
    """
    master = MasterProcess(odisseus_configuration=odisseus_config_obj)
    master.create_processes()
    master.run()


if __name__ == '__main__':
    main()