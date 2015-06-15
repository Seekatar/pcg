import Base
import datetime
import random

class FixedRandomGame(Base.Game):
	"""
        Game with a fixed set of random plates to touch
	"""
	
	def __init__(self):
                super(FixedRandomGame,self).__init__('Random touch game',
                                  'Game to test leds and buttons',
                                  'Jimmy Wallace',
                                  datetime.date(2015,6,14),
                                  '0.1')
                self.LOOP_CNT = 20
	
	def initialize(self,hardware,user):
		"""
		Initialize 
		"""
		super(FixedRandomGame,self).initialize(hardware,user)
                
		self.hardware.display_number(0)
		
	def play(self):
		"""
		Implement to play game and return the score. 
		"""
		wrong = 0
				
		self.hardware.write_message('Press 1-9')
				
		for i in range(0,self.LOOP_CNT):
			ledToLight = random.randint(0,9)
			self.hardware.light_on(ledToLight)
			
			b = 0
			while b != ledToLight:
				b = self.hardware.wait_for_button()
				if b != ledToLight: # wrong
					wrong += 1
					self.hardware.display_number(wrong)
					self.hardware.light_bad()
					self.hardware.beep(duration_sec=.2)
					self.hardware.light_on(ledToLight)
					
		return wrong
			
					
					
                
              
