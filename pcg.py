import RPi.GPIO as io
import time
import random
import sys
import os
import signal

print ">>>>",os.path.dirname(__file__)
sys.path.append(os.path.join(os.path.dirname(__file__),'GpioUtil'))

def signal_handler(signal, frame):
    io.cleanup()
    print "Cleaned up"
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
  


from SevenSegment import SevenSegment
from Flasher import Flasher
from CharliePlexer import CharliePlexer                

# initialize
io.setmode(io.BOARD)

DEBUG = True

# CharliePlexing Numbers
led1 = 0
led2 = 1
led3 = 11
led4 = 2
led5 = 3
led6 = 10
led7 = 9
led8 = 8
led9 = 6
ledCorrect = 4
ledIncorrect = 5

# Channel Numbers
beeperNumber = 3

plate1 = 5
plate2 = 23
plate3 = 10
plate4 = 7
plate5 = 21
plate6 = 19
plate7 = 26
plate8 = 24
plate9 = 8

DELAY_SEC = 1
DELAY_PAUSE_SEC = .5
LOOP_CNT = 20

leds = [ led1, led2, led3, led4, led5, led6, led7, led8, led9 ]

plates = [ plate1, plate2, plate3, plate4, plate5, plate6, plate7, plate8, plate9 ]
for b in plates:
    io.setup(b,io.IN, pull_up_down=io.PUD_UP)

sevenSegment = SevenSegment(2)
beeper = Flasher(beeperNumber)
ledArray = CharliePlexer()

if False:
    sevenSegment.test()
    beeper.test()
    ledArray.test()


sevenSegment.set(' ',' ')

# At start turn on middle panel
while True:
    
    print "Waiting for plate 5"
    while True:
        ledArray.light(led5)
        state = io.input(plate5)
        if state == io.LOW:
            if DEBUG:
                print "Ready to play"
            for l in leds:
                ledArray.light(l)
                time.sleep(.2)
            ledArray.light(-1)
            break
        time.sleep(.1)
        ledArray.light(-1)
        time.sleep(.1)

    misses = 0
    sevenSegment.set_num(misses)

    # Game ready to start
    for x in range(0,LOOP_CNT):
        ledToLight = random.randint(0,len(leds)-1)
        ledArray.light(leds[ledToLight])

        if DEBUG:
            print 'hit it now! plate', ledToLight+1,'led', leds[ledToLight], 'plate pin', plates[ledToLight]

        hit = False 

        while not hit:
            for b in plates:
                state = io.input(b)
                if False: #DEBUG:
                    print "state is",state,"for",b,"looking for",plates[ledToLight]
                if state == io.LOW:
                    if  b == plates[ledToLight]:
                        hit = True
                        print "HIT!",misses,"/",LOOP_CNT
                        ledArray.light(ledCorrect)
                        beeper.flash(.3)
                        break
                    else:
                        print "Miss. plate",b,'looking for', plates[ledToLight]
                        misses = misses + 1
                        sevenSegment.set_num(misses)
                        ledArray.light(ledIncorrect)
                        beeper.flash(.1, 3)
                        time.sleep(DELAY_PAUSE_SEC)
                        ledArray.light(leds[ledToLight])
            

    beeper.flash(1)
