import RPi.GPIO as io

io.setmode(io.BCM)

# the Pins Odisseus is using

IN_PIN_1 = 27
IN_PIN_2 = 22
IN_PIN_3 = 20
IN_PIN_4 = 21

io.setup(IN_PIN_1, io.OUT)
io.setup(IN_PIN_2, io.OUT)
io.setup(IN_PIN_3, io.OUT)
io.setup(IN_PIN_4, io.OUT)