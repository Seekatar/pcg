import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))

import Base
import msvcrt
import colorama
colorama.init()

pos = lambda y, x: '\033[%d;%dH' % (y, x)

class TestHardware(Base.Hardware):


    def __init__(self):
        self._prev_light = -1
        self._debug_line = 30
        self._good_on = False
        self._bad_on = False

        self.show_board()

        
    def show_board(self):
        self.cleanup()
        for i in range(1,10):
            self.light_on(i)
        self.light_off(-1)
        self.light_good(0)
        self.light_bad(0)
        self.display_number(0)
        for i in range(15):
            print


    def _bad_off(self):
        if self._bad_on:
            print pos(2,9)+colorama.Fore.GREEN+colorama.Style.DIM+colorama.Fore.RED+"\002"+colorama.Style.RESET_ALL
            self._bad_on = False
            
    def _good_off(self):
        if self._good_on:
            print pos(2,17)+colorama.Fore.GREEN+colorama.Style.DIM+"\002"+colorama.Style.RESET_ALL   
            self._good_on = False
            
    def self_test(self):
        pass

    def plate_count(self):
            """
            return the number of plates/leds in the hardware
            """
            return 9

    def cleanup(self):
            print "\033[0m" # reset
            print '\033[2J' # cls

    def reset(self):
            if self.DEBUG:
                raw_input("Debug mode:  Press enter to continue")
            self.show_board()
            print "\033[0m" # reset

    
    def light_bad(self,duration_sec=.5):
        """
        Turn on the 'bad' light for duration seconds, blocking
        """
        self.light_off(-1)
        self._bad_on = True
        print pos(2,9)+colorama.Back.BLACK+colorama.Fore.RED+colorama.Style.BRIGHT+"\002"+colorama.Style.RESET_ALL
        if duration_sec > 0:
            time.sleep(duration_sec)
            self._bad_off()

        return self

    def light_good(self,duration_sec=.5):
        """
        Turn on the 'good' light for duration seconds, blocking
        """
        self.light_off(-1)
        self._good_on = True
        print pos(2,17)+colorama.Back.BLACK+colorama.Fore.GREEN+colorama.Style.BRIGHT+"\002"+colorama.Style.RESET_ALL    
        if duration_sec > 0:
            time.sleep(duration_sec)
            self._good_off

        return self

    def light_on(self,number,duration_sec=0):
        """
        Turn on a light for duration seconds, blocking
        """
        if self._prev_light != number:
            print colorama.Back.GREEN+colorama.Fore.GREEN+colorama.Style.BRIGHT+pos(9-2*(int((number-1)/3)),6+6*((number-1)%3))+" "+str((number-1)+1)+" "+colorama.Style.RESET_ALL
            if self._prev_light > 0:
                    self.light_off(self._prev_light)
            self._prev_light = number

        if duration_sec > 0:
            time.sleep(duration_sec)
            self.light_off(-1)

        return self
    
    def light_off(self,number=-1):
        """
        Turn off a light.  Use -1 to turn off all
        """
    
        if number == -1:
            self._good_off()
            self._bad_off()
            number = self._prev_light
            
        if number > 0 and number < 10:
                print colorama.Back.GREEN+colorama.Fore.BLACK+colorama.Style.DIM+pos(9-2*(int((number-1)/3)),6+6*((number-1)%3))+" "+str((number-1)+1)+" "+colorama.Style.RESET_ALL
        self._prev_light = -1

        return self
        
    def display_number(self,number):
        """
        Put this number on the two-digit display
        """
        s = "%02d" % number
        print pos(11,12)+colorama.Fore.GREEN+colorama.Style.BRIGHT+colorama.Fore.RED+s

        return self
        
    def display_characters(self,char1=' ',char2=' '):
        """
        Put these characters on the two-digit display
        """
        print pos(11,12)+colorama.Fore.GREEN+colorama.Style.BRIGHT+colorama.Back.BLACK+colorama.Fore.RED+char1+char2+colorama.Style.RESET_ALL

        return self
        
    def beep(self,count=1,duration_sec=.5,interval_sec=.3):
        """
        Sound the beeper
        """
        for i in range(count):
            print "\007"
            time.sleep(interval_sec)

        return self
            
    def wait_for_button(self,timeout_sec=0):
        """
        Wait for a button to be pressed.  Will return
        the button number that was pressed
        """
        start = time.clock()
        while not msvcrt.kbhit():
            time.sleep(.01)
            if not msvcrt.kbhit() and timeout_sec > 0 and time.clock() - start > timeout_sec:
                return 0 # timed out
                
        c = msvcrt.getch()
        if c >= '1' and c <= '9':
            return int(c)
        else:
            self.beep()

    def blink_light_until_button(self, number, button = -1, blink_on_sec = .3, blink_off_sec = .3):
        """
        blink a light until a button is pressed use -1 for button to return on any button
        """
        b = 0
        while b == 0: 
            b = self.light_on(number).wait_for_button(blink_on_sec)
            if b != 0 and (button == -1 or b == button):
                return b
            self.light_off().wait(blink_off_sec)

    def write_message(self,line1,line2=""):
        """
        write a message to the two line display
        """
        print colorama.Style.RESET_ALL,pos(13,1)+colorama.Fore.BLUE+colorama.Style.BRIGHT+line1+' '*(78-len(line1))
        print pos(14,1)+colorama.Fore.BLUE+colorama.Style.BRIGHT+line2+' '*(78-len(line2))

        return self

    def write_debug(self,*msg):
        m = ""
        for i in msg:
            m += str(i)+' '
            
        print pos(self._debug_line,1)+colorama.Fore.WHITE+m+'\n                             '
        self._debug_line += 1
        if self._debug_line > 30:
            self._debug_line = 16
        
        return self

        
if __name__ == '__main__':        
    test = TestHardware()
    score = 0
    for i in range(1,10):
        test.light_on(i)
        j = test.wait_for_button(10)
        if j == i:
            test.light_good()
            test.beep()
        elif j == 0:
            print 'timed out'
        else:
            score += 1
            test.display_number(score)
            test.light_bad()
            test.beep()
            test.beep()
    test.write_message("this is line 1","this is line2")
            
