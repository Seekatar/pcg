class Persistence(object):
    """
    Base peristence class
    """
    
    def load(self):
        """
        load the persistence
        """
        pass
        
    def close(self):
        """
        close the object
        """
        pass
        
    def get_anonymous(self):
        """
        get the anonymous user 
        """
        pass
        
    def save_score_start(self,score,user):
        """
        save the score for a user
        """
        pass            

    def save_score_end(self,score,user):
        """
        save the score for a user
        """
        pass            
