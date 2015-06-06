import RPi.GPIO as io
import time

class Flasher:
    """
    Class for flashing or beeping
    """
    
    def __init__( self, dataPin = 11):
        """
        Construct the class 
        """
        self._pin = dataPin
        
        io.setup(self._pin,io.OUT)

        io.output(self._pin, io.LOW)

    def flash(self, count = 1, durationSec = .1, delaySec = .1):
        for i in range(count):
            io.output(self._pin,io.HIGH)
            time.sleep(durationSec)
            io.output(self._pin,io.LOW)
            if count > 1:
                time.sleep(delaySec)

if __name__ == '__main__':        
    import RPi.GPIO as io
    print "Testing...."

    io.setmode(io.BOARD)
    
    f = Flasher(3)
    f.flash(5)
