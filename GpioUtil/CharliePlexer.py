import RPi.GPIO as io
import time

DEBUG = False

class CharliePlexer:
    """
    class to light LEDs in a CharliePlex arrangements of 3 or 4 pins
    """
    
    states3 = [
        [ 1, 0,-1],
        [ 0, 1,-1],
        [-1, 1, 0],
        [-1, 0, 1],
        [ 1,-1, 0],
        [ 0,-1, 1]]

    states4 = [
        [ 1, 0,-1,-1],
        [ 0, 1,-1,-1],
        [-1, 1, 0,-1],
        [-1, 0, 1,-1],
        [ 1,-1, 0,-1],
        [ 0,-1, 1,-1],
        [ 1,-1,-1, 0],
        [ 0,-1,-1, 1],
        [-1,-1, 0, 1],
        [-1,-1, 1, 0],
        [-1, 1,-1, 0],
        [-1, 0,-1, 1]
        ]

    def __init__( self, pin1 = 15, pin2 = 16, pin3 = 18, pin4 = 22):
        """
        Construct the class using number of leds and pins
        """
        self._pins = [pin1,pin2,pin3]
        if pin4 > 1:
            self._pins.append(pin4)
            self._states = CharliePlexer.states4
        else:
            self._states = CharliePlexer.states3

        for p in self._pins:        
            io.setup(p,io.IN, pull_up_down=io.PUD_OFF)

                              
    def light(self,state):
        """
        light up one of the lights
        """
        if state < -1 or state > len(self._states):
            return
        
        if state == -1:
            for p in self._pins:
                io.setup(p,io.IN, pull_up_down=io.PUD_OFF)
        else:
            for p,s in enumerate(self._states[state]):
                if DEBUG:
                    print "   sending ",s,' to ',self._pins[p]

                if s == -1:
                    io.setup(self._pins[p],io.IN, pull_up_down=io.PUD_OFF)
                else:
                    io.setup(self._pins[p],io.OUT)
                    io.output(self._pins[p],s)
                

    def test(self):
        """
        Light all the LEDs
        """
        for i in range(len(self._states)):
            self.light(i)
            time.sleep(.3)
        self.light(-1)
            
if __name__ == '__main__':        
    import RPi.GPIO as io
    io.setmode(io.BOARD)

    print "Testing 3...."
    s3 = CharliePlexer(pin4=-1)
    s3.test()
    
    print "Testing 4...."
    s = CharliePlexer()
    s.test()

    while True:
        x = int(raw_input("enter 0-11, -1 or 99 to exit " ))
        if x == 99:
            break
        s.light(x)
    
    io.cleanup()

    
        

