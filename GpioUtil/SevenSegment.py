import RPi.GPIO as io
import time

class SevenSegment:
    """
    Class for sending letters or numbers to one or two 7-segment leds
    using a bit shifting IC.  The wiring is like the Sunfounder sample
    """
    
    def __init__( self, leds = 1, dataPin = 11, latchPin = 12, clockPin = 13):
        """
        Construct the class using number of leds and pins
        """
        self._leds = leds;
        self._data = dataPin
        self._latch = latchPin
        self._clock = clockPin
        
        io.setup(self._data,io.OUT)
        io.setup(self._latch,io.OUT)
        io.setup(self._clock,io.OUT)

        io.output(self._data, io.LOW)
        io.output(self._latch, io.LOW)
        io.output(self._clock, io.LOW)


    # bit codes with character in comment
    SegCodes = {   '0':0x3f, # 0
                       '1':0x06, # 1
                       '2':0x5b, # 2
                       '3':0x4f, # 3
                       '4':0x66, # 4
                       '5':0x6d, # 5
                       '6':0x7d, # 6
                       '7':0x07, # 7
                       '8':0x7f, # 8
                       '9':0x6f, # 9
                       'A':0x77, # A
                       'B':0x7c, # b
                       'C':0x39, # C
                       'D':0x5e, # d
                       'E':0x79, # E
                       'F':0x71, # F
                       '-':0x40, # -
                         1:0x01, # top
                         2:0x02, # upper rt  
                         4:0x04, # lower rt
                         8:0x08, # bottom
                       0x10:0x10,# lower left
                       0x20:0x20,# upper left
                       0x40:0x40,# middle
                       '.':0x80, # .
                       ' ':0x00} # <blank>


    def _hc595_shift(self,dat):
        # put the 8 bits into the register
        # one bit at a time
        for x in range(0,8):
            value =  0x80 & (dat << x)
            # set the bit
            if value == 0:
                io.output(self._data,io.LOW)
            else:
                io.output(self._data,io.HIGH)
            # tell it to take the bit    
            io.output(self._clock, io.HIGH)
            time.sleep(.001)
            io.output(self._clock, io.LOW)

    def _hc595_latch(self):
        # flip the self._latch to move to the output lines
        io.output(self._latch, io.HIGH)
        time.sleep(.001)
        io.output(self._latch, io.LOW)

    def set(self,char1ToSet,char2ToSet=None):
        """
        Set a character on the display
        Valid values are 0-9, A-F, ., -, and numbers 1-0x40 in multiples of 2
        """
        if char1ToSet >= 'a' and char1ToSet <= 'z':
            char1ToSet = char1ToSet.upper()
        if char2ToSet >= 'a' and char2ToSet <= 'z':
            char2ToSet = char2ToSet.upper()
        
        self._hc595_shift(SevenSegment.SegCodes[char1ToSet])
        if char2ToSet != None and self._leds > 1:
            self._hc595_shift(SevenSegment.SegCodes[char2ToSet])
        self._hc595_latch()

    def set_num(self,num):
        if num > 100:
            num = 99
        elif num < 0:
            num = 0

        char1 = ' '
        char2 = ' '
        if num < 10:
            char1 = chr(ord('0') + num)
        else:
            char1 = chr(ord('0') + num % 10)
            char2 = chr(ord('0') + num / 10)

        if self._leds == 1:
            char1 = None
        self.set(char2,char1)
            
    def march(self,count,delay=.1):
        for i in range(count):
            s.set(1,1)
            time.sleep(delay)
            s.set(0x40,0x40)
            time.sleep(delay)
            s.set(8,8)
            time.sleep(delay)

    def spin(self,count,delay=.05):
        for i in range(count):
            num = 1
            for j in range(0,6):
                s.set(num,num)
                num = num*2
                time.sleep(delay)

    def spin_cc(self,count,delay=.05):
        for i in range(count): 
            num = 0x20
            for j in range(0,6):
                s.set(num,num)
                num = num/2
                time.sleep(.05)

    def snake(self,count,delay=.05):
        for i in range(count):
            nums = [1,2,0x40,0x10,8,4,0x40,0x20]
            for j in nums:
                self.set(j,j)
                time.sleep(.05)

    def test(self):
        self.snake(2)
        self.set(' ',' ')
        
if __name__ == '__main__':        
    import RPi.GPIO as io
    print "Testing...."
    io.setmode(io.BOARD)
    s = SevenSegment(2)
    for i in range(0,100):
        s.set_num(i)
        time.sleep(.05)
        print i
    s.set('.','.');

    # march down
    s.march(5)

    # spin clockwise
    s.spin(5)

    # spin counter clockwise
    s.spin_cc(5)
    
    #snake
    s.snake(5)

    s.test()
    
    io.cleanup()

    
        

