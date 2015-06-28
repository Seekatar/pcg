import Base
import datetime
import random

class FixedRandomGame(Base.Game):
    """
    Game with a fixed set of random plates to touch
    
    Level n: n*10 plates
    """
    
    def GameInfo():
        """
        return tuple of (name,desc,levels,author,date,version)
        """
        return ('Random',
                'Fixed number of random touches',
                5, #levels
                'Jimmy Wallace',
                datetime.date(2015,6,14),
                '0.1')    
    GameInfo = staticmethod(GameInfo) 

    def __init__(self):
        self.LOOP_CNT = 20
        self._timeout_sec = 10
        self._interval_sec = 0
        self._score = 0

    def initialize(self,hardware,user,level):
        """
        Initialize 
        """
        super(FixedRandomGame,self).initialize(hardware,user,level)
        
        self.LOOP_CNT = level*10
        
    def get_next_plate(self):
        """
        override to change number of plates, etc.
        """
        return random.randint(1,9)
        
    def get_timeout_sec(self):
        """
        override to adjust timeout each time they touch
        """
        return self._timeout_sec

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
        self.hardware.display_number(self._score)\
            .light_good(.2)
            
        return False

    def _miss(self,button,missed_button):
        """
        return True to end the game
        """
        if self._score > 0:
            self._score -= 1
        self.hardware.display_number(self._score)\
            .light_bad()\
            .beep(duration_sec=.2)\
            .light_on(button)
        return False

    def initialize(self,hardware,user,level):
        """
        Initialize 
        """
        super(FixedRandomGame,self).initialize(hardware,user,level)
        
        self.hardware.display_number(0)
            
    def play(self):
        """
        Implement to play game and return the score. 
        """
        self._score = 0

        hw = self.hardware
        
        hw.write_message('Press 1-9')
                        
        for i in range(0,self.LOOP_CNT):
            ledToLight = self.get_next_plate()
            hw.write_debug( "Game lighting",ledToLight )
            hw.light_on(ledToLight)
            
            b = 0
            while b != ledToLight:
                b = hw.wait_for_button(self.get_timeout_sec())
                hw.write_debug( "Game got button",b,"expecting",ledToLight,"(0 is timeout)")
                if b == 0: # timeout
                    if self._timeout(ledToLight):
                        hw.write_debug("timed out")
                        break 
                elif b != ledToLight: # miss
                    if self._miss(ledToLight,b):
                        b = 0
                        hw.write_debug("exiting with miss")
                        break
                elif self._hit(b):
                    b = 0
                    hw.write_debug("exiting with hit")
                    break
                hw.wait(self._interval_sec)

            if b == 0:
                break
            hw.light_off()
            hw.wait(.1)
            
                                
        return self._score
                    
                                    
                                    
            
          
