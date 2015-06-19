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
        self.LOOP_CNT = 20
        self._timeout_sec = 10
        self._interval_sec = 0

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
                    hw.write_debug( "Game got button",b )
                    if b == 0:
                        break
                    elif b != ledToLight: # wrong
                        wrong += 1
                        hw.display_number(wrong)
                        hw.light_bad()
                        hw.beep(duration_sec=.2)
                        hw.light_on(ledToLight)
                    else:
                        hw.light_good(.2)
                    hw.wait(self._interval_sec)

            if b == 0:
                break
            hw.light_off()
            hw.wait(.1)
            
                                
        return wrong
                    
                                    
                                    
            
          
