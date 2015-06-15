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
				
		self.hardware.write_message('Follow the pattern')
				
		for i in range(1,self.PATTERN_LENGTH +1):
			
			for j in range (i):
				ledToLight = self._pattern[j]
				print "lighting",ledToLight
				self.hardware.light_on(ledToLight,.5)
			
                        for j in range (i):
				ledToLight = self._pattern[j]
				
				b = self.hardware.wait_for_button()
				if b != ledToLight: # wrong
                                        print "Got wrong",b
					self.hardware.beep(duration_sec=1)
					return i - 1
				else:
                                        print "Got right",b
                                        self.hardware.light_on(ledToLight)
                                        self.hardware.beep(duration_sec=.1)
                                        					
                        self.hardware.beep(2,.1)
                        
		return i - 1 
					
                
              
