import base
import datetime
import random
from FixedRandomGame import FixedRandomGame as __base

# use __base, otherwise when searching for games, FixedRandomGame shows up multiple times
class FineControl(__base):
    """
    Touch four plates in patterns as fast as you can.
    
    Level 1: tight, clockwise 5 times
    Level 2: tight, anti clockwise 5 times
    Level 3: tight, repeat 4 each: clockwise, anticlockwise, diagonal1, diagonal2
    Level 4: wide, clockwise 5 times
    Level 5: wide, anti clockwise 5 times
    Level 6: wide, repeat 4 each: clockwise, anticlockwise, diagonal1, diagonal2
    """
    
    def GameInfo():
        """
        return tuple of (name,desc,levels,author,date,version)
        """
        return ("FineControl",               
                "Tight patterns of plates", 
                6, #levels
                "Jim Wallace",
                 datetime.date(2015,6,19),
                 '0.1')
    GameInfo = staticmethod(GameInfo) 

   # patterns
    _clockwise = (1,2,5,4)
    _anticlockwise = _clockwise[::-1] #reverse
    _diagonal1 = (1,5)
    _diagonal2 = (2,4)
    
    _wclockwise = (1,3,9,7)
    _wanticlockwise = _wclockwise[::-1] #reverse
    _wdiagonal1 = (1,9)
    _wdiagonal2 = (3,7)
                
    def __init__(self):
        super(FineControl,self).__init__()
                    
        self._timeout_sec = 10
        self._interval_sec = 0
 
        self._pattern = None
        self._pattern_index = -1
        self.LOOP_CNT = 0

    def initialize(self,hardware,user,level):
        """
        Initialize 
        """
        super(FineControl,self).initialize(hardware,user,level)
        
        if self.level == 1:    
            self._pattern = FineControl._clockwise*5
        elif self.level == 2:
            self._pattern = FineControl._anticlockwise*5
        elif self.level == 3:    
            repeat = 4
            self._pattern = FineControl._clockwise*repeat+FineControl._anticlockwise*repeat+FineControl._diagonal1*repeat+FineControl._diagonal2*repeat
        elif self.level == 4:    
            self._pattern = FineControl._wclockwise*5
        elif self.level == 5:
            self._pattern = FineControl._wanticlockwise*5
        else:    
            repeat = 4
            self._pattern = FineControl._wclockwise*repeat+FineControl._wanticlockwise*repeat+FineControl._wdiagonal1*repeat+FineControl._wdiagonal2*repeat
        
        # index for next plate
        self._pattern_index = -1
            
        self.LOOP_CNT = len(self._pattern)
       
    def get_next_plate(self):
        """
        override to change number of plates, etc.
        """
        self._pattern_index += 1
        return self._pattern[self._pattern_index]
