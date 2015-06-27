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
sys.path.append(os.path.join(os.path.dirname(__file__),'Games'))
sys.path.append(os.path.join(os.path.dirname(__file__),'Persistence'))

from Base import User,Game,Score

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

def _load_games():
    """
    load all the game classes in the Games folder
    """
    games = []
    gameFolder = os.path.join(os.path.dirname(__file__),'Games')
    sys.path.append(gameFolder)
    print os.path.join(gameFolder,'*.py')
    gameNum = 1
    for f in  sorted(glob(os.path.join(gameFolder,'*.py')),key=str.lower):
        m = __import__(os.path.splitext(os.path.basename(f))[0])
        for i in dir(m):
            if not i.startswith('__') and isclass(m.__dict__[i]) and issubclass(m.__dict__[i],Game):
                (name,description,levels,author,date,version) = m.__dict__[i].GameInfo()
                hardware.write_debug( "Added", gameNum, name,"by",author,"with",levels,"levels from file",f)
                gameNum += 1
                games.append(m.__dict__[i])
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
    games = _load_games()
    if args.debug:
        raw_input("Press enter")
    
def _get_user():
    """
    get a user 
    """
    u = User()
    u.first_name = 'Jimmy'
    u.last_name = 'Wallace'
    u.email = 'xeekatar@gmail.com'
    u.pin = '1234'
    return u

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
            hardware.display_characters('B','Y')
            hardware.cleanup()
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
        
        score = Score().load_at_start(name,level,user)
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
