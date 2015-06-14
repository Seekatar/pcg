import RPi.GPIO as io
import time
import random
import sys
import os
import Base

sys.path.append(os.path.join(os.path.dirname(__file__),'..','GpioUtil'))

from SevenSegment import SevenSegment
from Flasher import Flasher
from CharliePlexer import CharliePlexer                

class PiHardware(Base.Hardware):
    """
    RaspberryPi RPi.GPIO implementation of the hardware
    """

    def initialize(self):
        
        # initialize
        io.setmode(io.BOARD)

        DEBUG = True             

        # CharliePlexing Numbers
        self.led1 = 0
        self.led2 = 1
        self.led3 = 11
        self.led4 = 2
        self.led5 = 3
        self.led6 = 10
        self.led7 = 9
        self.led8 = 8
        self.led9 = 6
        self.ledCorrect = 4
        self.ledIncorrect = 5

        # Channel Numbers
        beeperNumber = 3

        self.plate1 = 5
        self.plate2 = 23
        self.plate3 = 10
        self.plate4 = 7
        self.plate5 = 21
        self.plate6 = 19
        self.plate7 = 26
        self.plate8 = 24
        self.plate9 = 8

        self.DELAY_SEC = 1
        self.DELAY_PAUSE_SEC = .5
        self.LOOP_CNT = 20

        self.leds = [ self.led1, self.led2, self.led3, self.led4, self.led5, self.led6, self.led7, self.led8, self.led9 ]

        self.plates = [ self.plate1, self.plate2, self.plate3, self.plate4, self.plate5, self.plate6, self.plate7, self.plate8, self.plate9 ]
        for b in self.plates:
            io.setup(b,io.IN, pull_up_down=io.PUD_UP)

        self.sevenSegment = SevenSegment(2)
        self.beeper = Flasher(beeperNumber)
        self.ledArray = CharliePlexer()

    def self_test(self):
            self.sevenSegment.test()
            self.beeper.test()
            self.ledArray.test()

        
    def reset(self):
        """
        reset between games
        """
 
    def cleanup(self):
        """
            cleanup on exit
        """
            pass
    
    def reset(self):
        """
        reset between games
        """
        self.sevenSegment.set(' ',' ')
   
    def light_bad(self,duration_sec=0):
        """
            Turn on the 'bad' light for duration seconds, blocking
        """
        self.ledArray.light(self.ledIncorrect)
        if duration_sec > 0:
            time.sleep(duration_sec)
            self.light_off()

    def light_good(self,duration_sec=0):
        """
        Turn on the 'good' light for duration seconds, blocking
        """
        self.ledArray.light(self.ledCorrect)
        if duration_sec > 0:
            time.sleep(duration_sec)
            self.light_off()
            
    def light_on(self,number,duration_sec=0):
        """
            Turn on a light for duration seconds, blocking
        """
        if number >= 1 and number <= len(self.leds):
            self.ledArray.light(self.leds[number-1])
            if duration_sec > 0:
                time.sleep(duration_sec)
                self.light_off()
            
    def light_off(self,number = -1):
        """
            Turn off a light.  Use -1 to turn off all
        """
        self.ledArray.light(-1)

            
    def display_number(self,number):
        """
        Put this number on the two-digit display
        """
         self.sevenSegment.set_num(number)
 
    def display_characters(self,char1=' ',char2=' '):
        """
        Put these characters on the two-digit display
        """
        self.sevenSegment.set(char1,char2)
            
    def beep(self,count=1,duration_sec=.5,interval_sec=.3):
        """
        Sound the beeper
        """
        self.beeper.flash(count,duration_sec,interval_sec)
            
    def wait_for_button(self,expected_button,timeout_sec=0):
        """
            Wait for a button to be pressed.  Will return
            the button number that was pressed
        """
        while not hit:
            for plate,b in enumerate(self.plates):
                state = io.input(b)
                
                if False: #DEBUG:
                    print "state is",state,"for",b,"looking for",self.plates[self.ledToLight]
                    
                if state == io.LOW:
                    # hit!
                    return plate+1 # plate number is 1 based


    def blink_light_until_button(self, number, button, blink_on_sec =.1, blink_off_sec =.1):
        """
        blink a light until a button is pressed use -1 for button to return on any button
        """
        if number < 1 or number > len(self.leds) or button < 1 or button > len(self.leds):
            raise "Invalid parameter"
        
        while True:
            self.light_on(number)
            pressButton = self.wait_for_button(button)
            if button == -1 or pressButton == button:
                return button
            self.wait(blink_on_sec)
            self.light_off()
            self.wait(blink_off_sec)
    
    def write_message(self,line1,line2=""):
        """
        write a message to the two line display
        """
        pass
                

