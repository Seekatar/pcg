import RPi.GPIO as io
import time
import random
import sys
import os
import Queue
import threading
import argparse

class EventButtonTest(object):
    """ mostly copied from PiHardware"""
    
    def button_pressed(channel):
        EventButtonTest.me().pressed(channel)
        
    button_pressed = staticmethod(button_pressed)
        
    def me():
        return __me
    me = staticmethod(me)
    
    def __init__(self,bounce):
        global __me
        __me = self
        self.plate1 = 5
        self.plate2 = 23
        self.plate3 = 10
        self.plate4 = 7
        self.plate5 = 21
        self.plate6 = 19
        self.plate7 = 26
        self.plate8 = 24
        self.plate9 = 8

        self.plates = [ self.plate1, self.plate2, self.plate3, self.plate4, self.plate5, self.plate6, self.plate7, self.plate8, self.plate9 ]

        for (i,b) in enumerate(self.plates):
            io.setup(b,io.IN, pull_up_down=io.PUD_UP)
            io.add_event_detect(b,io.FALLING,\
                                callback=EventButtonTest.button_pressed,bouncetime=bounce) # 100 caused problems, 200 ok

        self._buttonQ = Queue.Queue()
        self._event = threading.Event()
        self._last = time.time()
        self._count = 0
        self._falseCount = 0

    def pressed(self,channel):
        button = self.plates.index(channel)+1
        if not io.input(channel):
            self._buttonQ.put(button)
            self._event.set()
            now = time.time()
            self._count += 1
            print "%.3f button %d on channel %d elapsed = %.2f count is %d" % (time.time(),button,channel,now - self._last, self._count)
            self._last = now
            
        else:
            self._falseCount += 1
            print "%.3f FALSE button %d on channel %d count is %d" % (time.time(),button,channel,self._falseCount)
            
if __name__ == '__main__':        
    import RPi.GPIO as io
    print "Testing...."

    """
    Bounce: When hammering it n times:  n/<hit>/<falsehit>
    Get extras
    0: 10/24/34
    50 10/14/9
    75 10/14/7
    
    Ok
    *100 50/50/28
    *150 50/50/18
    
    Lose some
    200 10/7/4
    250 10/5/3
   
    """
    
    parser = argparse.ArgumentParser(description='Button testing with bounce')
    parser.add_argument('-b','--bounce',type=int,default=200)

    args = parser.parse_args()
    
    print 'Bounce is set to ',args.bounce
    
    io.setmode(io.BOARD)

    b = EventButtonTest(args.bounce)
    
    raw_input("running in background")
    
        
        
       