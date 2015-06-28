import argparse
import time
import random
import sys
import os
import signal
from inspect import isclass
from glob import glob
import gc

sys.path.append(os.path.join(os.path.dirname(__file__),'hardware'))
sys.path.append(os.path.join(os.path.dirname(__file__),'games'))
sys.path.append(os.path.join(os.path.dirname(__file__),'persistence'))

from base import User
from base import Game
from base import Score

def signal_handler(signal, frame):
    """
    control C handler when interactive
    """
    if hardware is not None:
        hardware.cleanup()
    if persistence is not None:
        persistence.close()
        
    print "Cleaned up"
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

hardware = None
persistence = None
games = []

def _load_games(printOut):
    """
    load all the game classes in the Games folder
    """
    games = []
    gameFolder = os.path.join(os.path.dirname(__file__),'games')
    sys.path.append(gameFolder)
    print os.path.join(gameFolder,'*.py')
    gameNum = 1
    for f in  sorted(glob(os.path.join(gameFolder,'*.py')),key=str.lower):
        m = __import__(os.path.splitext(os.path.basename(f))[0])
        for i in dir(m):
            if not i.startswith('__') and isclass(m.__dict__[i]) and issubclass(m.__dict__[i],Game):
                (name,description,levels,author,date,version) = m.__dict__[i].GameInfo()
                hardware.write_debug( "Added", gameNum, name,"by",author,"with",levels,"levels from file",f)
                games.append(m.__dict__[i])
                
                if printOut:
                    print "Game %d %s with %d levels:" % (gameNum,name,levels)
                    print games[gameNum-1].__doc__
                    
                gameNum += 1

    return games
    
def _initialize():
    """
    initialize the main game
    """
    global hardware
    global games
    global persistence
    
    parser = argparse.ArgumentParser(description='Point Control Game by Jimmy Wallace')
    parser.add_argument('-t','--test',action='store_true',help='run the simulator instead of on Pi hardware')
    parser.add_argument('-d','--debug',action='store_true',help='show debug message on console')
    parser.add_argument('-l','--list',action='store_true',help='list all the games')

    args = parser.parse_args()

    # load the hardware
    if args.test:
        from TestHardware import TestHardware
        hardware = TestHardware()
    else:
        from PiHardware import PiHardware
        hardware = PiHardware()

    hardware.initialize(args.debug)
    
    from Sqlite import SqlitePersistence
    persistence = SqlitePersistence()
    persistence.load()

    # load games
    games = _load_games(args.list)

    if args.list:
        exit ()
            
    if args.debug:
        raw_input("Press enter")    
        
def _main():
    """
    main loop
    """
    user = None
    GAME_SELECT_DELAY = .4
    
    while True:
        gc.disable()
        hardware.reset()

        if user is None:
            user = persistence.get_anonymous()
            
        # do game selection by good/bad light
        hardware.write_message("Waiting for a game selection","  Choose 1 - %d" % len(games)).\
                display_characters('H','I')
            
        select = hardware.select_by_lights(len(games),9)
        if select == 9:
            for i in xrange(5):
                hardware.display_characters('B','Y')\
                        .wait(.3)\
                        .display_characters(' ',' ')\
                        .wait(.2)
            hardware.wait(1)\
                    .cleanup()
            exit()
            
        # game picked, construct it
        (name,description,levels,author,date,ver) = games[select-1].GameInfo()
        game = games[select-1]() 
        level = 1
        if levels > 1:
            hardware.display_characters('L','E')
            level = hardware.select_by_lights(levels,9)
        if level == 9:
            continue
        
        hardware.display_number(0)
        
        game.initialize(hardware,user,level)

        hardware.write_message("Playing game>",name)
        hardware.write_debug(description,'by',author)
        
        score = Score().load_at_start(name,ver,level,user)
        persistence.save_score_start(score,user)
        
        start = time.clock()
        score.score = game.play()

        score.duration_sec = time.clock() - start
        persistence.save_score_end(score,user)

        hardware.beep(2,.5)
        hardware.blink_light_until_button(5)
        
        gc.enable()
        gc.collect()
        
        
if __name__ == '__main__':
    
    _initialize()

    _main()
