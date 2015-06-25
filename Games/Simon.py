import Base
import datetime
import random

class Simon(Base.Game):
    """
        Game with a fixed set of random plates to touch
    """
    
    def GameInfo():
        """
        return tuple of (name,desc,levels,author,date,version)
        """
        return ("Simon",               
                "Simon says follow the leader", 
                1, #levels
                'Jimmy Wallace',
                datetime.date(2015,6,14),
                '0.1')
                 
    GameInfo = staticmethod(GameInfo)     
    
    def __init__(self):
        super(Simon,self).__init__()
        
        self.PATTERN_LENGTH = 50
        self._pattern = []
    
    def initialize(self,hardware,user,level):
        """
        Initialize 
        """
        super(Simon,self).initialize(hardware,user,level)
                
        self.hardware.display_number(0)
        
        self._pattern = []
        
        for i in range (self.PATTERN_LENGTH):
            self._pattern.append(random.randint(1,9))

        self.hardware.wait(.5)
        
    def play(self):
        """
        Implement to play game and return the score. 
        """

        hw = self.hardware
        
        hw.write_message('Follow the pattern')
                
        for i in range(1,self.PATTERN_LENGTH +1):
            
            # show the pattern
            for j in range (i):
                ledToLight = self._pattern[j]
                hw.write_debug( "lighting",ledToLight).\
                    light_on(ledToLight,.5).\
                    light_off().\
                    wait(.1)
            
            # have then match it
            for j in range (i):
                ledToLight = self._pattern[j]
                
                b = hw.wait_for_button()
                if b != ledToLight: # wrong
                    hw.write_debug( "Got wrong",b )
                    hw.beep(duration_sec=1)
                    return i - 1
                else:
                    hw.write_debug( "Got right",b )
                    hw.light_on(ledToLight)
                                                            
            hw.wait(.4)
                        
        return i - 1 
                    
                
              
