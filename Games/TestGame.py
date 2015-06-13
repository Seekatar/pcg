import Base

class TestGame(Base.GameBase):
	"""
	Simple test game that lights all panels waiting
	for a hit
	"""
	
	def initialize(self,hardware,user):
		"""
		Initialize 
		"""
		super(TestGame,self).initialize(hardware,user)
                
		self.name = 'Test game'
		self.description = 'Game to test leds and buttons'
		self.author = 'Jim Wallace'
		self.date = '2015-6-12'
		self.version = '0.1'

		self.hardware.display_number(0)
		
	def play(self):
		"""
		Implement to play your game.  Return the score
		"""
                wrong = 0
                
		for i in range(1,10):
                    self.hardware.light_on(i)
                    b = 0
                    while b != i:
                        b = self.hardware.wait_for_button()
                        if b != i: # wrong
                            wrong += 1
                            self.hardware.display_number(wrong)
                            self.hardware.light_bad(.3)
                            self.hardware.beep(duration_sec=.2)
                            self.hardware.light_on(i)
                        
                # game over
                self.hardware.light_off(-1)
                self.hardware.beep(duration_sec=1)
                return wrong
                

        
    
