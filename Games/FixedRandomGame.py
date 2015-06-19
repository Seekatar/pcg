import Base
import datetime
import random

class FixedRandomGame(Base.Game):
    """
    Game with a fixed set of random plates to touch
    """
    
    def __init__(self):
        super(FixedRandomGame,self).__init__('Random touch game',
                          'Game to test leds and buttons',
                          'Jimmy Wallace',
                          datetime.date(2015,6,14),
                          '0.1')
        self.LOOP_CNT = 2
        self._timeout_sec = 10
        self._interval_sec = 0
        self._score = 0

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
        return False
            
    def _hit(self,button):
        """
        return True to end the game
        """
        self.hardware.light_good(.2)
        return False

    def _miss(self,button,missed_button):
        """
        return True to end the game
        """
        self._score += 1
        self.hardware.display_number(self._score)
        self.hardware.light_bad()
        self.hardware.beep(duration_sec=.2)
        self.hardware.light_on(button)
        return False

    def initialize(self,hardware,user):
        """
        Initialize 
        """
        super(FixedRandomGame,self).initialize(hardware,user)
        
        self.hardware.display_number(0)
            
    def play(self):
        """
        Implement to play game and return the score. 
        """
        wrong = 0

        hw = self.hardware
        
        hw.write_message('Press 1-9')
                        
        for i in range(0,self.LOOP_CNT):
            ledToLight = self.get_next_plate()
            hw.write_debug( "Game lighting",ledToLight )
            hw.light_on(ledToLight)
            
            b = 0
            while b != ledToLight:
                b = hw.wait_for_button(self.get_timeout_sec())
                hw.write_debug( "Game got button (0 is timeout)",b )
                if b == 0: # timeout
                    if self._timeout(ledToLight):
                        break 
                elif b != ledToLight: # wrong
                    if self._miss(ledToLight,b):
                        b = 0
                        break
                elif self._hit(b):
                    b = 0
                    break
                hw.wait(self._interval_sec)

            if b == 0:
                break
            hw.light_off()
            hw.wait(.1)
            
                                
        return wrong
                    
                                    
                                    
            
          
