import RPi.GPIO as io
import time
import random
import sys
import os

sys.path.append(os.path.join(os.getcwd(),'GpioUtil'))


from SevenSegment import SevenSegment
from Flasher import Flasher
from CharliePlexer import CharliePlexer                

# initialize
io.setmode(io.BOARD)
sevenSegment = SevenSegment()
beeper = Flasher(3)
ledArray = CharliePlexer()

sevenSegment.test()
beeper.test()
ledArray.test()
                
DEBUG = False
led1 = 15
led2 = 13

beeper = 7

button1 = 11
button2 = 12
stopbutton = 16

DELAY_SEC = 1
DELAY_PAUSE_SEC = .5
LOOP_CNT = 10

io.setmode(io.BOARD)

io.setup(beeper,io.OUT)

leds = [ led1, led2 ]
for l in leds:
    io.setup(l,io.OUT)

buttons = [ button1, button2, stopbutton]
for b in buttons:
    io.setup(b,io.IN, pull_up_down=io.PUD_UP)

def beep(durationSec = .1, pin = 7):
    io.output(pin,io.HIGH)
    time.sleep(durationSec)
    io.output(pin,io.LOW)

def beepbeep(durationSec = .01, waitSec = .01, pin = 7):
    beep(durationSec,pin)
    time.sleep(waitSec)
    beep(durationSec,pin)

def beepbeepbeep(durationSec = .01, waitSec = .01, pin = 7):
    beep(durationSec,pin)
    time.sleep(waitSec)
    beep(durationSec,pin)
    time.sleep(waitSec)
    beep(durationSec,pin)



prevState0 = io.HIGH
prevState1 = io.HIGH

for l in leds:
    io.output(l, io.LOW) 

while True:
    for x in range(0,LOOP_CNT):
        ledToLight = random.randint(0,len(leds)-1)
        io.output(leds[ledToLight],io.HIGH)
        print 'hit it now!', ledToLight

        hit = False 

        while not hit:
            for b in buttons:
                state = io.input(b)
                if DEBUG:
                    print "state is",state,"for",b,"looking for",buttons[ledToLight]
                if state == io.LOW:
                    if  b == buttons[ledToLight]:
                        hit = True
                        print "HIT!"
                        beep(.05)
                        break
                    elif b == stopbutton:
                        beepbeepbeep(.3,.2)
                        exit (9)
                    else:
                        print "Miss."
                        beepbeep()
            
        io.output(leds[ledToLight],io.LOW)
        time.sleep(DELAY_PAUSE_SEC)

    beep(1)
