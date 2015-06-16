import argparse
import time
import random
import sys
import os
import signal
from inspect import isclass
from glob import glob

sys.path.append(os.path.join(os.path.dirname(__file__),'hardware'))
sys.path.append(os.path.join(os.path.dirname(__file__),'Games'))

from Base import User,Game

def signal_handler(signal, frame):
    """
    control C handler when interactive
    """
    if hardware is not None:
        hardware.cleanup()
    print "Cleaned up"
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

hardware = None
games = []

def _load_games():
    """
    load all the game classes in the Games folder
    """
    games = []
    gameFolder = os.path.join(os.path.dirname(__file__),'Games')
    sys.path.append(gameFolder)
    print os.path.join(gameFolder,'*.py')
    for f in  sorted(glob(os.path.join(gameFolder,'*.py')),key=str.lower):
        m = __import__(os.path.splitext(os.path.basename(f))[0])
        for i in dir(m):
            if not i.startswith('__') and isclass(m.__dict__[i]) and issubclass(m.__dict__[i],Game):
                print "Added %s" % (i)
                games.append(m.__dict__[i])
    return games
    
def _initialize():
    """
    initialize the main game
    """
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

    hardware.initialize(args.debug)

    # load games
    games = _load_games()
    
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
    GAME_SELECT_DELAY = .4
    
    while True:
        hardware.reset()

        if user is None:
            user = _get_user()
            
        # do game selection by good/bad light
        hardware.write_message("Waiting for a game selection","  Choose 1 - %d" % len(games))
        selectCount = 0
        while True:
            # blink lights for available games
            hardware.light_on(1+(selectCount % len(games)))
            selectCount += 1
            b = hardware.wait_for_button(.4) # array 0-based, buttons 1-based
            if b == 9:
                hardware.cleanup()
                exit()
                
            if b > 0:
                index = b - 1
                if index >= 0 and index < len(games):
                    # blink their choice
                    for w in xrange(5):
                        hardware.light_on(b,.1)
                        hardware.light_off()
                        hardware.wait(.1)
                    break
                else:
                    hardware.beep()
                    hardware.write_message("Chose %d.  Try again" % b,"  Choose 1 - %d" % len(games))
                    hardware.wait(.1)
                    hardware.light_bad()
                    hardware.wait(.1)

        # game picked, construct it
        game = games[index]() 

        game.initialize(hardware,user)

        hardware.write_message("Playing game",game.name)
        game.play()
        
        
if __name__ == '__main__':
    
    _initialize()

    _main()
