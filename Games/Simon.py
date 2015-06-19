import Base
import datetime
import random

class SimonSays(Base.Game):
	"""
        Game with a fixed set of random plates to touch
	"""
	
	def __init__(self):
                super(SimonSays,self).__init__('Simon Says',
                                  'Remember the pattern',
                                  'Jimmy Wallace',
                                  datetime.date(2015,6,14),
                                  '0.1')
                self.PATTERN_LENGTH = 50
                self._pattern = []
	
	def initialize(self,hardware,user):
		"""
		Initialize 
		"""
		super(SimonSays,self).initialize(hardware,user)
                
                self.hardware.display_number(0)
		
		self._pattern = []
		
		for i in range (self.PATTERN_LENGTH):
			self._pattern.append(random.randint(1,9))

		self.hardware.wait(.5)
		
	def play(self):
		"""
		Implement to play game and return the score. 
		"""

		hw = self.hardware
		
		hw.write_message('Follow the pattern')
				
		for i in range(1,self.PATTERN_LENGTH +1):
			
			for j in range (i):
				ledToLight = self._pattern[j]
				hw.write_debug( "lighting",ledToLight)
				hw.light_on(ledToLight,.5)
				hw.light_off()
				hw.wait(.1)
			
                        for j in range (i):
				ledToLight = self._pattern[j]
				
				b = hw.wait_for_button()
				if b != ledToLight: # wrong
                                        hw.write_debug( "Got wrong",b )
					hw.beep(duration_sec=1)
					return i - 1
				else:
                                        hw.write_debug( "Got right",b )
                                        hw.light_on(ledToLight)
                                        hw.beep(duration_sec=.1)
                                        					
                        hw.beep(2,.1)
                        hw.wait(.3)
                        
		return i - 1 
					
                
              
