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
        self.duration_sec = 0.0
        self.level = 1
        self.user_id = None
        self.game_id = None
        self.timestamp = None
        self.crashed = True
                
class GameData(object):
    """
    Just the data members for a game
    """
    def __init__(self):
        return self
                
class Game(GameData):
    """
    Base class for games
    """
    
    def __init__(self):
        self.level = 1

    def initialize(self,hardware,user,level):
        """
        Initialize 
        """
        self.level = level
        self.hardware = hardware
        self.user = user
        self.DEBUG = hardware.DEBUG
        
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
        

class Hardware(object):
    """
    Abstraction of the hardware

    Note that for the lights, only one is on at a time, turning one on
    will turn any other one off
    """
    def __init__(self):
        self.DEBUG = False
                
    def self_test(self):
        return self

    def plate_count(self):
        """
        return the number of plates/leds in the hardware
        """
        return self
               
    def initialize(self,debugFlag):
        """
        do any one-time initialization
        """
        self.DEBUG = debugFlag
        return self

    def cleanup(self):
        """
        cleanup on exit
        """
        return self
    
    def reset(self):
        """
        reset between games
        """
        return self
    
    def light_bad(self,duration_sec=0):
        """
        Turn on the 'bad' light for duration seconds, blocking
        """
        return self

    def light_good(self,duration_sec=0):
        """
        Turn on the 'good' light for duration seconds, blocking
        """
        return self

    def light_on(self,number,duration_sec=0):
        """
        Turn on a light for duration seconds, blocking
        """
        return self
    
    def light_off(self,number):
        """
        Turn off a light.  Use -1 to turn off all
        """
        return self
        
    def display_number(self,number):
        """
        Put this number on the two-digit display
        """
        return self
        
    def display_characters(self,char1=' ',char2=' '):
        """
        Put these characters on the two-digit display
        """
        return self
        
    def beep(self,count=1,duration_sec=.5,interval_sec=.3):
        """
        Sound the beeper
        """
        return self
        
    def wait_for_button(self,timeout_sec=0):
        """
        Wait for a button to be pressed.  Will return
        the button number that was pressed
        """
        return self

    def blink_light_until_button(self, number, button, blink_on_sec, blink_off_sec ):
        """
        blink a light until a button is pressed use -1 for button to return on any button
        """
        return 0
    
    def wait(self,timeout_sec = .5):
        """
        wait for a bit
        """
        time.sleep(timeout_sec)
        return self
    
    def write_message(self,line1,line2=""):
        """
        write a message to the two line display
        """
        return self

    def write_debug(self,*msg):
        """
        write a message out if debug set
        """
        return self
        
    def select_by_lights(self, count, exitNumber):
        """
        Use the lights to select up to count items
        """
        selectCount = 0
        while True:
            # blink lights for available games
            selectCount += 1
            self.light_on(1+(selectCount % count))
            b = self.wait_for_button(.4) # array 0-based, buttons 1-based
            if b == exitNumber:
                return exitNumber
                
            if b > 0:
                index = b - 1
                if index >= 0 and index < count:
                    # blink their choice
                    for w in xrange(5):
                        self.light_on(b,.1)\
                                 .light_off()\
                                 .wait(.1)
                    break
                else:
                    self.beep()\
                             .write_message("Chose %d.  Try again" % b,"  Choose 1 - %d" % count)\
                             .wait(.1)\
                             .light_bad()\
                             .wait(.1)
                             
        return b


            
