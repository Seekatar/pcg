import Base
import sys
from glob import glob

def _loadGames():
    """
    """

    games = []
    
    gamePath = os.path.join(os.path.dirname(__file__),'Games'
    sys.path.append(gamePath)
    for f in glob(os.path.join(gamePath,'*.py')):
        m = __import__(os.path.basename(f))
        for i in dir(m):
            if not i.startswith('__') and issubclass(i,Base.GameBase):
                games.append(i)

    return games


                            
                
