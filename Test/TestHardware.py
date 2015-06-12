import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
print sys.path
import Base
import colorama
colorama.init()

pos = lambda y, x: '\x1b[%d;%dH' % (y, x)

class HardwareTest(Base.HardwareBase):


	def __init__(self):
		self._prev_light = -1
		self.show_board()
		
	def show_board(self):
		print "\033[2J"
		for i in range(1,10):
			self.light_on(i)
		self.light_on(5)
		self.light_good(.1)
		self.light_bad(.1)
		self.display_number(0)
		self.beep()
		
	def self_test(self):
		pass

	def light_bad(self,duration_sec=.5):
		"""
		Turn on the 'bad' light for duration seconds, blocking
		"""
		print pos(2,9)+colorama.Back.BLACK+colorama.Fore.RED+colorama.Style.BRIGHT+"\002"
		time.sleep(duration_sec)
		print pos(2,9)+colorama.Fore.GREEN+colorama.Style.DIM+colorama.Fore.RED+"\002"

	def light_good(self,duration_sec=.5):
		"""
		Turn on the 'good' light for duration seconds, blocking
		"""
		print pos(2,17)+colorama.Back.BLACK+colorama.Fore.GREEN+colorama.Style.BRIGHT+"\002"	
		time.sleep(duration_sec)
		print pos(2,17)+colorama.Fore.GREEN+colorama.Style.DIM+"\002"	

	def light_on(self,number,duration_sec=0):
		"""
		Turn on a light for duration seconds, blocking
		"""
		
		print colorama.Back.GREEN+colorama.Fore.GREEN+colorama.Style.BRIGHT+pos(5+2*(int((number-1)/3)),6+6*((number-1)%3))+" "+str((number-1)+1)+" "
		if self._prev_light > 0:
			self.light_off(self._prev_light)
		self._prev_light = number
		if duration_sec > 0:
			time.sleep(duration_sec)
			self.light_off(i)
	
	def light_off(self,number):
		"""
		Turn off a light.  Use -1 to turn off all
		"""
		print colorama.Back.GREEN+colorama.Fore.BLACK+colorama.Style.DIM+pos(5+2*(int((number-1)/3)),6+6*((number-1)%3))+" "+str((number-1)+1)+" "
		pass
		
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
		print pos(13,1)+colorama.Back.BLACK+colorama.Fore.WHITE+"Press	a button"
		return int(raw_input())
		
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
			
