import time

class User(object):
	"""
        Simple user, date only for easy storing in database
        """
	def __init__(self):
                self.user_id = None # database id
		self.first_name = None
		self.last_name = None
		self.email = None
		self.pin = None

class Score(object):
        """
        Simple score object for easy storing in database
        """
	def __init__(self):
		self.id = None # database id
                self.score = 0
                self.user_id = None
                self.game_id = None
                self.timestamp = None
                
class GameBaseData(object):
	"""
	Just the data members for a game
	"""
	def __init__(self):
		self.game_id = None # database id
		self.name = None
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

	def cleanup(self):
                """
                Implement to cleanup your game in case it was interrupted
                """
                pass
        

class HardwareBase(object):
	"""
	Abstraction of the hardware

	Note that for the lights, only one is on at a time, turning one on
	will turn any other one off
	"""
	def self_test(self):
		pass

        def initialize(self):
                """
                do any one-time initialization
                """
                pass

        def cleanup(self):
                """
                cleanup on exit
                """
                pass
        
        def reset(self):
                """
                reset between games
                """
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

	def wait(self,timeout_sec = .5):
                """
                wait for a bit
                """
                time.sleep(timeout_sec)
                
