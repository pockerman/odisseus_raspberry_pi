"""
Test if anything is connected to I2C bus. This code is taken
from: https://learn.adafruit.com/circuitpython-essentials/circuitpython-i2c
"""

import time
import board
import busio

def main():

    i2c = busio.I2C(board.SCL, board.SDA)

    while not i2c.try_lock():
        pass

    while True:
        print("I2C addresses found:", [hex(device_address)
                                   for device_address in i2c.scan()])
        time.sleep(2)


if __name__ == '__main__':

    print("Testing I2C bus...")
    main()