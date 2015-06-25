import Base
import datetime
import random
from FixedRandomGame import FixedRandomGame as __base

class SpeedyRandomGame(__base):
    """
    Game with a declining speed to hit the plates
    """
    
    def GameInfo():
        """
        return tuple of (name,desc,levels,author,date,version)
        """
        return ('SpeedyTouch',
                  'Faster!',
                  1,
                  'Jim Wallace',
                  datetime.date(2015,6,14),
                  '0.1')
                 
    GameInfo = staticmethod(GameInfo)    
        
    def __init__(self):
        super(SpeedyRandomGame,self).__init__()
        self.LOOP_CNT = 100
        self._timeout_sec = 2
        self._interval_sec = 2


    def get_timeout_sec(self):
        """
        override to adjust timeout each time they touch
        """
        self._interval_sec *= .95
        self.hardware.write_debug("now",self._interval_sec,self.LOOP_CNT)
        return self._interval_sec
    
    def _timeout(self,button):
        """
        return True to end the game
        """
        return True
    
    def _hit(self,button):
        """
        return True to end the game
        """
        self._score += 1
        self.hardware.light_good(.2)\
                     .display_number(self._score)
        
        return False

    def _miss(self,button,missed_button):
        """
        return True to end the game
        """
        self.hardware.light_bad()\
                .beep(duration_sec=.2)\
                .light_on(button)
        
        return False
