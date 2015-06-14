import Base
import datetime

class TestGame(Base.Game):
	"""
	Simple test game that lights all panels waiting	for a hit
	"""

	def __init__(self):
                super(TestGame,self).__init__('Test game',
                                          'Game to test leds and buttons',
                                          'Jim Wallace',
                                          datetime.date(2015,6,12),
                                          '0.1')
	
	def initialize(self,hardware,user):
		"""
		Initialize 
		"""
		super(TestGame,self).initialize(hardware,user)
                
		self.hardware.display_number(0)
		
	def play(self):
		"""
		Implement to play your game.  Return the score
		"""
                wrong = 0

                self.hardware.write_message('Press 1-9')
                
		for i in range(1,10):
                    self.hardware.light_on(i)
                    b = 0
                    while b != i:
                        b = self.hardware.wait_for_button()
                        if b != i: # wrong
                            wrong += 1
                            self.hardware.display_number(wrong)
                            self.hardware.light_bad()
                            self.hardware.beep(duration_sec=.2)
                            self.hardware.light_on(i)
                        
                # game over
                self.hardware.light_off()
                self.hardware.beep(duration_sec=1)
                return wrong
                

        
    
