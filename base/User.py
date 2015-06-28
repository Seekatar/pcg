class User(object):
    """
    Simple user, date only for easy storing in database
    """
    def __init__(self):
        self.user_id = None # database id
        self.first_name = None
        self.last_name = None
        self.email = None
        self.pin = None
        
    def load_from_tuple(self,user):
        self.user_id = user[0]
        self.first_name = user[1]
        self.last_name = user[2]
        self.email = user[3]
        self.pin = user[4]
        return self
        
