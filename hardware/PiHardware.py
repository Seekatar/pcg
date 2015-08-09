import RPi.GPIO as io
import time
import random
import sys
import os
import base
import Queue
import threading

sys.path.append(os.path.join(os.path.dirname(__file__),'..','GpioUtil'))

from SevenSegment import SevenSegment
from Flasher import Flasher
from CharliePlexer import CharliePlexer                

DEBUG = True

def button_pressed(channel):
    PiHardware.me().pressed(channel)

class PiHardware(base.Hardware):
    """
    RaspberryPi RPi.GPIO implementation of the hardware
    """

    def __init__(self):
        global __piHardware
        __piHardware = self
        print "Init to",self,__piHardware

    def me():
        return __piHardware
    me = staticmethod(me)
    
    def initialize(self,debugFlag):
        super(PiHardware,self).initialize(debugFlag)
        
        print "Initialize says",__piHardware
        
        # initialize
        io.setwarnings(False)
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

        for (i,b) in enumerate(self.plates):
            io.setup(b,io.IN, pull_up_down=io.PUD_UP)
            io.add_event_detect(b,io.FALLING,\
                                callback=button_pressed,bouncetime=200) 

        self.sevenSegment = SevenSegment(2)
        self.beeper = Flasher(beeperNumber)
        self.ledArray = CharliePlexer()
        self._buttonQ = Queue.Queue()
        self._event = threading.Event()

    def pressed(self,channel):
        button = self.plates.index(channel)+1
        if not io.input(channel):
            self.write_debug( "+ button",button," on channel ",channel )
            self._buttonQ.put(button)
            self._event.set()
        else:
            self.write_debug( "FALSE button",button," on channel ",channel )
        
       
         

    def self_test(self):
            self.sevenSegment.test()
            self.beeper.test()
            self.ledArray.test()

    def plate_count(self):
        return len(self.leds())
        
    def reset(self):
        """
        reset between games
        """

        return self
 
    def cleanup(self):
        """
            cleanup on exit
        """
        io.cleanup()

        return self
    
    def reset(self):
        """
        reset between games
        """
        self.sevenSegment.set(' ',' ')

        return self
   
    def light_bad(self,duration_sec=0):
        """
            Turn on the 'bad' light for duration seconds, blocking
        """
        self.ledArray.light(self.ledIncorrect)
        if duration_sec > 0:
            time.sleep(duration_sec)
            self.light_off()

        return self

    def light_good(self,duration_sec=0):
        """
        Turn on the 'good' light for duration seconds, blocking
        """
        self.ledArray.light(self.ledCorrect)
        if duration_sec > 0:
            time.sleep(duration_sec)
            self.light_off()
            
        return self

    def light_on(self,number,duration_sec=0):
        """
            Turn on a light for duration seconds, blocking
        """
        if number >= 1 and number <= len(self.leds):
            self.ledArray.light(self.leds[number-1])
            if duration_sec > 0:
                time.sleep(duration_sec)
                self.light_off()

        return self
            
    def light_off(self,number = -1):
        """
            Turn off a light.  Use -1 to turn off all
        """
        self.ledArray.light(-1)

        return self
            
    def display_number(self,number):
        """
        Put this number on the two-digit display
        """
        self.sevenSegment.set_num(number)
 
        return self

    def display_characters(self,char1=' ',char2=' '):
        """
        Put these characters on the two-digit display
        """
        self.sevenSegment.set(char1,char2)

        return self
            
    def beep(self,count=1,duration_sec=.5,interval_sec=.3):
        """
        Sound the beeper
        """
        self.beeper.flash(duration_sec,count,interval_sec)
        
        return self
            
    def wait_for_button(self,timeout_sec=None):
        """
        Wait for a button to be pressed.  Will return
        the button number that was pressed
        """
        start = time.time()
        while True:
            try:
                if self._event.wait(timeout_sec):
                    self._event.clear()
                    now = time.time()
                    if timeout_sec != None:
                        msg = "OK GOT WITHIN %.2f <= %.2f" % (now-start,timeout_sec)
                    else:
                        msg = "OK GOT WITHIN %.2f <= -1" % (now-start)
                    self.write_debug(msg)                   
                    return self._buttonQ.get_nowait()
                else:
                    break
            except Queue.Empty:
               pass
           
        now = time.time()
        msg = "TIMED OUT %.2f >= %.2f" % (now-start,timeout_sec)
        self.write_debug(msg)
        return 0 # timeout

    def blink_light_until_button(self, number, button = -1, blink_on_sec =.3, blink_off_sec =.3):
        """
        blink a light until a button is pressed use -1 for button to return on any button
        """
        if number < 1 or number > len(self.leds) or button < -1 or button == 0 or button > len(self.leds):
            raise "Invalid parameter"
        
        pressButton = 0
        while pressButton == 0:
            pressButton = self.light_on(number).wait_for_button(blink_on_sec)
            if pressButton != 0 and (button == -1 or pressButton == button):
                return pressButton
            self.light_off().wait(blink_off_sec)
    
    def write_message(self,line1,line2=""):
        """
        write a message to the two line display
        """
        print line1
        if len(line2) > 0:
            print line2
                
        return self

    def write_debug(self,*msg):
        m = ""
        for i in msg:
            m += str(i)+' '

        print "DEBUG: "+m
        
        return self
