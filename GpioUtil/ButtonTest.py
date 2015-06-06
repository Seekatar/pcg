import RPi.GPIO as io
import time

buttons = [7, # GPIO7
           #3, # SDA
           5, # SCL
           8, # TXD
           10, # RXD
           19, # MOS
           21, # MSO
           23, # SCLK
           24, # CE0
           26] # CE1

io.setmode(io.BOARD)

for b in buttons:
    io.setup(b,io.IN, pull_up_down=io.PUD_UP)

while True:
    for b in buttons:
        state = io.input(b)
        if state == io.LOW:
            print "Button",b,"!"
