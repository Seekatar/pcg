import base
import datetime

class TestGame(base.Game):
    """
    Simple test game that lights all panels waiting for a hit
    """

    def GameInfo():
        """
        return tuple of (name,desc,levels,author,date,version)
        """
        return ('Test game',
                  'Game to test leds and buttons',
                  1,
                  'Jim Wallace',
                  datetime.date(2015,6,12),
                  '0.1')
    GameInfo = staticmethod(GameInfo)   
    
    def __init__(self):
        super(TestGame,self).__init__()
    
    def initialize(self,hardware,user,level):
        """
        Initialize 
        """
        super(TestGame,self).initialize(hardware,user,level)
                
        self.hardware.display_number(0)
        
    def play(self):
        """
        Implement to play your game.  Return the score
        """
        self._score = 0
    
        self.hardware.write_message('Press 1-9')
                
        for i in range(1,10):
            self.hardware.light_on(i)
            b = 0
            while b != i:
                b = self.hardware.wait_for_button(5)
                if b == 0:
                    break # timeout, go on to next number
                if b != i: # wrong
                    if self._score > 0:
                        self._score -= 1
                    self.hardware.display_number(self._score)\
                                 .light_bad()\
                                 .beep(duration_sec=.2)\
                                 .light_on(i)
            self._score += 1
            self.hardware.display_number(self._score)
                        
        # game over
        self.hardware.light_off()
                     
        return self._score
                

        
    
