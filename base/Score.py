import time

class Score(object):
    """
    Simple score object for easy storing in database
    """
    def __init__(self):
        self.score_id = None # database id
        self.score = 0
        self.duration_sec = 0.0
        self.level = 1
        self.user_id = None
        self.game_name = None
        self.game_version = None
        self.timestamp = None
        self.crashed = True
        
    def load_at_start(self,game_name,game_version,level,user):
        self.score_id = None # database id
        self.score = 0
        self.duration_sec = 0.0
        self.game_name = game_name
        self.game_version = game_version
        self.level = level
        self.user_id = user.user_id
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S.000')
        self.crashed = True
        return self
        
    def load_from_tuple(self,scoreTuple):
        self.score_id = scoreTuple[0]
        self.score = scoreTuple[1]
        self.duration_sec = scoreTuple[2]
        self.game_name = scoreTuple[3]
        self.game_version = scoreTuple[4]
        self.level = scoreTuple[5]
        self.user_id = scoreTuple[6]
        self.timestamp = scoreTuple[7]
        self.crashed = scoreTuple[8]
        return self
                        
