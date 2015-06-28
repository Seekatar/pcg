from GameData import GameData

class Game(GameData):
    """
    Base class for games
    """
    
    def __init__(self):
        super(Game,self).__init__()
        self.level = 1

    def initialize(self,hardware,user,level):
        """
        Initialize 
        """
        self.level = level
        self.hardware = hardware
        self.user = user
        self.DEBUG = hardware.DEBUG
        
    def play(self):
        """
        Implement to play your game.  Return the score
        """
        pass

    def cleanup(self):
        """
        Implement to cleanup your game in case it was interrupted
        """
        pass
        

