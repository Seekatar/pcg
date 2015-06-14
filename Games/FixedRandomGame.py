import Base
import datetime

class FixedRandomTestGame(Base.Game):
	"""
        Game with a fixed set of random plates to touch
	"""
	
	def __init__(self):
	                super(FixedRandomTestGame,self).__init__('Random touch game',
                                          'Game to test leds and buttons',
                                          'Jimmy Wallace',
                                          datetime.date(2015,6,14),
                                          '0.1')
	
	def initialize(self,hardware,user):
		"""
		Initialize 
		"""
		super(FixedRandomTestGame,self).initialize(hardware,user)
                
                self.hardware.display_number(0)
		
        def play(self):
                """
                TODO
                """
                pass
              
