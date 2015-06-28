import Base
import datetime
import random
from FixedRandomGame import FixedRandomGame as __base

class SpeedyRandomGame(__base):
    """
    Game with a declining time to hit the plates
    
    Level 1: 5% decrease after each touch
    Level 2: 15% decrease after each touch
    Level 3: 25% decrease after each touch
    """
    
    def GameInfo():
        """
        return tuple of (name,desc,levels,author,date,version)
        """
        return ('SpeedyTouch',
                  'Faster!',
                  3,
                  'Jim Wallace',
                  datetime.date(2015,6,14),
                  '0.1')
                 
    GameInfo = staticmethod(GameInfo)    
        
    def __init__(self):
        super(SpeedyRandomGame,self).__init__()
        self.LOOP_CNT = 100
        self._timeout_sec = 2
        self._interval_sec = 2
        self._interval_decrease = .95

    def initialize(self,hardware,user,level):
        """
        Initialize 
        """
        super(SpeedyRandomGame,self).initialize(hardware,user,level)
        
        self._interval_decrease = 1 - (.05*level)
        
        self.hardware.write_debug("decrease amount is",self._interval_decrease)
        
        
    def get_timeout_sec(self):
        """
        override to adjust timeout each time they touch
        """
        self._interval_sec *= self._interval_decrease
        self.hardware.write_debug("now",self._interval_sec,self.LOOP_CNT)
        return self._interval_sec


