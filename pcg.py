import argparse
import time
import random
import sys
import os
import signal

sys.path.append(os.path.join(os.path.dirname(__file__),'Hardware'))
sys.path.append(os.path.join(os.path.dirname(__file__),'Games'))

from Base import User

def signal_handler(signal, frame):
    """
    control C handler when interactive
    """
    # TODO 
    print "Cleaned up"
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

hardware = None
games = {}

def _initialize():
    global hardware
    global games
    
    parser = argparse.ArgumentParser(description='Point Control Game by Jimmy Wallace')
    parser.add_argument('-t','--test',action='store_true',help='run the simulator instead of on Pi hardware')
    parser.add_argument('-d','--debug',action='store_true',help='show debug message on console')

    args = parser.parse_args()

    # load the hardware
    if args.test:
        from TestHardware import TestHardware
        hardware = TestHardware()
    else:
        from PiHardware import PiHardware
        hardware = PiHardware()

    hardware.initialize()

    # load games
    from TestGame import TestGame

    games[9] = TestGame()

def _get_user():
    """
    get a user 
    """
    u = User()
    u.first_name = 'Jimmy'
    u.last_name = 'Wallace'
    u.email = 'xeekatar@gmal.com'
    u.pin = '1234'
    return u

def _main():
    """
    main loop
    """
    user = None
    
    while True:
        hardware.reset()

        if user is None:
            user = _get_user()
            
        # do game selection by good/bad light
        hardware.write_message("Waiting for a game selection")
        while True:
            hardware.light_good()
            b = hardware.wait_for_button()
            if b in games:
                break
            else:
                hardware.beep()
            hardware.wait(.1)
            hardware.light_bad()
            hardware.wait(.1)

        # game picked
        game = games[b]

        game.initialize(hardware,user)

        game.play()
        
        
if __name__ == '__main__':
    
    _initialize()

    _main()
