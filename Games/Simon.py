import Base
import datetime

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
			self.pattern.append(random.randint(0,9))
		
	def play(self):
		"""
		Implement to play game and return the score. 
		"""
				
		self.hardware.write_message('Follow the pattern')
				
		for i in range(1,PATTERN_LENGTH +1):
			
			for j in range (i):
				ledToLight = self._pattern[j]
				self.hardware.light_on(ledToLight)
			
			
				b = self.hardware.wait_for_button()
				if b != ledToLight: # wrong
					self.hardware.beep(duration_sec=1)
	
			
					return i - 1

		return i - 1 
					
                
              
