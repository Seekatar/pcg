import Base
import datetime
import random
from FixedRandomGame import FixedRandomGame as __base

class FineControl(__base):
    """
    Game with a declining speed to hit the plates
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

        repeat = 4
        self._pattern = self._clockwise*repeat+self._anticlockwise*repeat+self._diagonal1*repeat+self._diagonal2*repeat
        
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
        
                                    
                                    
            
          
