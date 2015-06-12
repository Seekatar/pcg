

class User:
	
	def __init__(self):
		self.first_name = None
		self.last_name = None
		self.email = None
		self.pin = None
		
class GameBaseData:
	"""
	Just the data members for a game
	"""
	def __init__(self):
		self.name = None
		self.id = None
		self.description = None
		self.author = None
		self.date = None
		self.version = None
	
class GameBase(GameBaseData):
	"""
	Base class for games
	"""
	
	def initialize(self,hardware,user):
		"""
		Initialize 
		"""
		self.hardware = hardware
		self.user = user
		
	def play(self):
		"""
		Implement to play your game.  Return the score
		"""
		pass
		

class HardwareBase:
	"""
	Abstraction of the hardware

	Note that for the lights, only one is on at a time, turning one on
	will turn any other one off
	"""
	def self_test(self):
		pass

	def light_bad(self,duration_sec=0):
		"""
		Turn on the 'bad' light for duration seconds, blocking
		"""
		pass

	def light_good(self,duration_sec=0):
		"""
		Turn on the 'good' light for duration seconds, blocking
		"""
		pass

	def light_on(self,number,duration_sec=0):
		"""
		Turn on a light for duration seconds, blocking
		"""
		pass
	
	def light_off(self,number):
		"""
		Turn off a light.  Use -1 to turn off all
		"""
		pass
		
	def display_number(self,number):
		"""
		Put this number on the two-digit display
		"""
		pass
		
	def display_characters(self,char1=' ',char2=' '):
		"""
		Put these characters on the two-digit display
		"""
		pass
		
	def beep(self,count=1,duration_sec=.5,interval_sec=.3):
		"""
		Sound the beeper
		"""
		pass
		
	def wait_for_button(self,expected_button,timeout_sec=0):
		"""
		Wait for a button to be pressed.  Will return
		the button number that was pressed
		"""
		pass