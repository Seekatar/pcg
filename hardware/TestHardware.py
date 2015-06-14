import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))

import Base
import msvcrt
import colorama
colorama.init()

pos = lambda y, x: '\x1b[%d;%dH' % (y, x)

class TestHardware(Base.Hardware):


	def __init__(self):
		self._prev_light = -1

	def show_board(self):
		self.cleanup()
		for i in range(1,10):
			self.light_on(i)
		self.light_off(-1)
		self.light_good(0)
		self.light_bad(0)
		self.display_number(0)
		
	def self_test(self):
		pass

        def cleanup(self):
                print "\033[0m" # reset
                print "\033[2J" # cls

        def reset(self):
                self.show_board()
                print "\033[0m" # reset
                
	def light_bad(self,duration_sec=.5):
		"""
		Turn on the 'bad' light for duration seconds, blocking
		"""
		self.light_off(-1)
		print pos(2,9)+colorama.Back.BLACK+colorama.Fore.RED+colorama.Style.BRIGHT+"\002"
		time.sleep(duration_sec)
		print pos(2,9)+colorama.Fore.GREEN+colorama.Style.DIM+colorama.Fore.RED+"\002"

	def light_good(self,duration_sec=.5):
		"""
		Turn on the 'good' light for duration seconds, blocking
		"""
		self.light_off(-1)
		print pos(2,17)+colorama.Back.BLACK+colorama.Fore.GREEN+colorama.Style.BRIGHT+"\002"	
		time.sleep(duration_sec)
		print pos(2,17)+colorama.Fore.GREEN+colorama.Style.DIM+"\002"	

	def light_on(self,number,duration_sec=0):
		"""
		Turn on a light for duration seconds, blocking
		"""
		if self._prev_light != number:
                        print colorama.Back.GREEN+colorama.Fore.GREEN+colorama.Style.BRIGHT+pos(5+2*(int((number-1)/3)),6+6*((number-1)%3))+" "+str((number-1)+1)+" "
                        if self._prev_light > 0:
                                self.light_off(self._prev_light)
                        self._prev_light = number

		if duration_sec > 0:
			time.sleep(duration_sec)
			self.light_off(i)
	
	def light_off(self,number=-1):
		"""
		Turn off a light.  Use -1 to turn off all
		"""
		if number == -1:
                        number = self._prev_light
                if number > 0 and number < 10:
                        print colorama.Back.GREEN+colorama.Fore.BLACK+colorama.Style.DIM+pos(5+2*(int((number-1)/3)),6+6*((number-1)%3))+" "+str((number-1)+1)+" "
                self._prev_light = -1
		
	def display_number(self,number):
		"""
		Put this number on the two-digit display
		"""
		s = "%02d" % number
		print pos(11,12)+colorama.Fore.GREEN+colorama.Style.BRIGHT+colorama.Fore.RED+s
		
	def display_characters(self,char1=' ',char2=' '):
		"""
		Put these characters on the two-digit display
		"""
		print pos(11,12)+colorama.Fore.GREEN+colorama.Style.BRIGHT+colorama.Back.BLACK+colorama.Fore.RED+char1+char2
		
	def beep(self,count=1,duration_sec=.5,interval_sec=.3):
		"""
		Sound the beeper
		"""
		for i in range(count):
			print "\007"
			time.sleep(interval_sec)
			
	def wait_for_button(self,timeout_sec=0):
		"""
		Wait for a button to be pressed.  Will return
		the button number that was pressed
		"""
		while True:
                        c = msvcrt.getch()
                        if c >= '1' and c <= '9':
                                return int(c)
                        else:
                                self.beep()

        def blink_light_until_button(self, number, button, blink_on_sec, blink_off_sec ):
            """
            blink a light until a button is pressed use -1 for button to return on any button
            """
            self.light_on(number)
            wait_for_button(button)

        def write_message(self,line1,line2=""):
                """
                write a message to the two line display
                """
                print pos(13,0)+colorama.Fore.BLUE+colorama.Style.BRIGHT+line1+' '*(78-len(line1))
                print pos(14,0)+colorama.Fore.BLUE+colorama.Style.BRIGHT+line2+' '*(78-len(line2))
                		
if __name__ == '__main__':        
	test = HardwareTest()
	score = 0
	for i in range(1,10):
		test.light_on(i)
		j = test.wait_for_button()
		if j == i:
			test.light_good()
			test.beep()
		else:
			score += 1
			test.display_number(score)
			test.light_bad()
			test.beep()
			test.beep()
	test.write_message("this is line 1","this is line2")
			
