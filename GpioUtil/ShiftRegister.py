import RPi.GPIO as io
import time

class ShiftRegister:
	"""
	Class for sending data to a shift register.
	"""
	
	def __init__( self, bytes, dataPin, latchPin, clockPin):
		"""
		Construct the class using pins
		"""
		self._bytes = bytes
		self._data = dataPin
		self._latch = latchPin
		self._clock = clockPin
		
		io.setup(self._data,io.OUT)
		io.setup(self._latch,io.OUT)
		io.setup(self._clock,io.OUT)

		io.output(self._data, io.LOW)
		io.output(self._latch, io.LOW)
		io.output(self._clock, io.LOW)


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
			time.sleep(.000001) # longer delay get flicker if setting multple dots fast
			io.output(self._clock, io.LOW)

	def _hc595_latch(self):
		# flip the self._latch to move to the output lines
		io.output(self._latch, io.HIGH)
		time.sleep(.000001) # longer delay get flicker if setting multple dots fast
		io.output(self._latch, io.LOW)

	def set(self,firstNum,*moreNums):
		"""
		set one or more numbers into the shift registers
		"""
		self._hc595_shift(int(firstNum))
		#print( "Set first",firstNum)
		for num in moreNums:
			self._hc595_shift(int(num))
			#print("Set more",num)
			
		self._hc595_latch()

class LedMatrix(ShiftRegister):

	def __init__(self,bytes,dataPin, latchPin, clockPin):
		super(LedMatrix,self).__init__(bytes, dataPin, latchPin, clockPin)

	def rowOn(self,row):
		"""
		Turn on a row, zero-base
		"""
		# 0 for first turns all leds across on
		# second byte is row bit, set only one row bit to turn on row
		if ( row > 7 ):
			return
		self.set(0x0,1 << (row))

	def columnOn(self,column):
		# ff for second turns on all columns
		# first byte needs column bit set to zero, turn off only one bit to turn on col
		if ( column > 7 ):
			return
		self.set( 0xff & (~(1 << (column))), 0xff )

	def off(self):
		self.set(0xff,0)

	def set_dot(self,x,y):
		if ( x > 7 or y > 7 ):
			return
		# x bit is off to turn on
		# y bit is on to turn on 
		self.set(0xff & (~(1 << y)),1 << x )

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("--dataPin", type=int, help="pin number for data")
	parser.add_argument("--latchPin", type=int, help="latch pin number")
	parser.add_argument("--clockPin", type=int, help="clock pin number")
	parser.add_argument("--delay", type=float, help="delay")
	args = parser.parse_args()


	print ("Testing....")
	io.setmode(io.BOARD)
	s = ShiftRegister(2,args.dataPin, args.latchPin, args.clockPin )

	x = input('enter a number to set (use 0x for hex), nothing to exit ')
	while len(x) > 0:
		n = int(x,0)
		if ( n > 0xfffff ):
			s.set( n >> 32 )
		if ( n > 0xffff ):
			s.set( (n & 0xff0000) >> 16 )
		if ( n > 0xff ):
			s.set( (n & 0xff00) >> 8)
		s.set( n & 0xff )
		x = input('enter a number to set (use 0x for hex), nothing to exit ')
	
	print ("testing matrix")
	m = LedMatrix(2,args.dataPin, args.latchPin, args.clockPin )
	#x = input('enter a row ')
	#while (len(x) > 0 ):
	#	m.rowOn(int(x))
	#	x = input('enter a row ')

	#x = input('enter a column ')
	#while (len(x) > 0 ):
	#	m.columnOn(int(x))
	#	x = input('enter a column ')

	#x = input('enter numbers x,y ')
	#while (len(x) > 0 and x.find(',') >= 0):
	#	(x,y) = x.split(',')
	#	m.set_dot(int(x),int(y))
	#	x = input('enter numbers x,y ')

	try:
		#totalOns = 0
		#totalOffs = 0
		#start = time.time()
		#for i in range(1000):
		#	m.set_dot(7,7)
		#	m.set_dot(1,1)
		#end = time.time()
		#print('100 ons averaged', (end-start)/2000.0)

		refreshRate = 1/30.0
		bits = 3.0
		lights = 3.0
		overheadPerSet = .0015

		timeLeft = refreshRate # - (bits*lights*overheadPerSet)
		sleepTime = timeLeft/(bits)

		print('refresh rate',refreshRate,'sleeptime',sleepTime)

		while (True):
			# bit one all of them
			m.set_dot(0,0)
			time.sleep(sleepTime/8)
			m.set_dot(0,1)
			time.sleep(sleepTime/8)
			m.set_dot(0,2)
			time.sleep(.000001) #sleepTime/500)

			## bit two, only first two
			#m.set_dot(0,0)
			#time.sleep(sleepTime/7)  # (longer?)
			#m.set_dot(0,1)
			#time.sleep(sleepTime/7)

			# bit three, only last
			m.set_dot(0,0)
			time.sleep(sleepTime)

			#for j in range(1,5):
			#	for i in range(8):
			#		if ( i & j ):
			#			m.set_dot(i,i)

	except KeyboardInterrupt:
		pass

	m.off()

	io.cleanup()
