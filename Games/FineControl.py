import Base
import datetime
import random
from FixedRandomGame import FixedRandomGame as __base

class FineControl(__base):
    """
    Game with a declining speed to hit the plates
    
    Level 1: clockwise 5 times
    Level 2: anti clockwise 5 times
    Level 3: repeat 4 clockwise, anticlockwise, diagonal1, diagonal2
    """
    
    def GameInfo():
        """
        return tuple of (name,desc,levels,author,date,version)
        """
        return ("FineControl",               
                "Tight patterns of plates", 
                3, #levels
                "Jim Wallace",
                 datetime.date(2015,6,19),
                 '0.1')
    GameInfo = staticmethod(GameInfo) 
    
    def __init__(self):
        super(FineControl,self).__init__()
                    
        self._timeout_sec = 10
        self._interval_sec = 0


        # pattern
        self._clockwise = (1,2,5,4)
        self._anticlockwise = self._clockwise[::-1] #reverse
        self._diagonal1 = (1,5)
        self._diagonal2 = (2,4)
        
        self._pattern = None
        self._pattern_index = -1
        self.LOOP_CNT = 0

    def initialize(self,hardware,user,level):
        """
        Initialize 
        """
        super(FineControl,self).initialize(hardware,user,level)
        
        if self.level == 1:    
            self._pattern = self._clockwise*5
        elif self.level == 2:
            self._pattern = self._anticlockwise*5
        else:    
            repeat = 4
            self._pattern = self._clockwise*repeat+self._anticlockwise*repeat+self._diagonal1*repeat+self._diagonal2*repeat
            
        # index for next plate
        self._pattern_index = -1
            
        self.LOOP_CNT = len(self._pattern)
       
    def get_next_plate(self):
        """
        override to change number of plates, etc.
        """
        self._pattern_index += 1
        return self._pattern[self._pattern_index]

    def _hit(self,button):
        """
        return True to end the game
        """
        self._score += 1
        self.hardware.display_number(self._score)\
                    .light_good(.2)
        return False

    def _miss(self,button,missed_button):
        """
        return True to end the game
        """
        self._score -= 1
        self.hardware.display_number(self._score)\
                    .light_bad()\
                    .beep(duration_sec=.2)\
                    .light_on(button)
        return False
        
                                    
                                    
            
          
