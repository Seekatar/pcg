import argparse
import sqlite3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))

from base import Persistence, User, Score

class SqlitePersistence(Persistence):
    """
    Sqlite persistence implementation
    """
    def __init__(self):
        self._conn = None
        pass
        
    def load(self):
        self._conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),'pcg.db'))
        self._create()
        
    def close(self):
        """
        close the object
        """
        if self._conn is not None:
            self._conn.close()
               
    CREATE_USER = """
        CREATE TABLE  IF NOT EXISTS USER
            (USER_ID INTEGER primary key,
                FIRST_NAME TEXT not null,
                LAST_NAME TEXT not null,
                EMAIL TEXT not null unique,
                PIN TEXT not null)
         """
     
    CREATE_SCORE = """       
         CREATE TABLE  IF NOT EXISTS SCORE
            (SCORE_ID  INTEGER primary key,
             GAME_NAME TEXT NOT NULL,
             GAME_VERSION TEXT NOT NULL,
             LEVEL INTEGER NOT NULL,
             USER_ID  INTEGER not null,
             TIMESTAMP datetime not null,
             SCORE REAL not null,
             DURATION_SEC REAL not null,
             CRASHED INTEGER NOT NULL,
             FOREIGN KEY(USER_ID) REFERENCES USER(USER_ID))        
        """    
        
    GET_ANONYMOUS = """
        SELECT * FROM USER WHERE EMAIL = 'ANONYMOUS'    
        """
    CREATE_ANONYMOUS = """
        INSERT INTO USER ( FIRST_NAME, LAST_NAME, EMAIL, PIN )
        VALUES ('U.N.','Owen','ANONYMOUS','')
        """
    INSERT_SCORE = """
        INSERT INTO SCORE ( GAME_NAME, GAME_VERSION, LEVEL, USER_ID, TIMESTAMP, SCORE,DURATION_SEC,CRASHED)
        VALUES(?,?,?,?,?,?,?,1)
        """      
          
    UPDATE_SCORE = """
        UPDATE SCORE 
            SET SCORE = ?,
            DURATION_SEC = ?,
            CRASHED = 0
        WHERE SCORE_ID = ?
        """              
    def _create(self):
        
        self._conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),'pcg.db'))
            
        c = self._conn.cursor()
        
        c.execute(SqlitePersistence.CREATE_USER)
        c.execute(SqlitePersistence.CREATE_SCORE)
        
        c.execute(SqlitePersistence.GET_ANONYMOUS)
        if c.fetchone() is None:
            c.execute(SqlitePersistence.CREATE_ANONYMOUS)
        
        self._conn.commit()
        
    def get_anonymous(self):
        """
        get the anonymous user 
        """
        c = self._conn.cursor()
        c.execute(SqlitePersistence.GET_ANONYMOUS)
        return User().load_from_tuple(c.fetchone())
                
    def save_score_start(self,score,user):
        """
        save the score for a user at start of game
        """
        c = self._conn.cursor()
        c.execute(SqlitePersistence.INSERT_SCORE,
            (score.game_name,
            score.game_version,
            score.level,
            user.user_id,
            score.timestamp,
            score.score,
            score.duration_sec))
        score.score_id = c.lastrowid
        self._conn.commit()
        
    def save_score_end(self,score,user):
        """
        save the score for a user at end with score
        """
        c = self._conn.cursor()
        c.execute(SqlitePersistence.UPDATE_SCORE,
            (score.score,
            score.duration_sec,
            score.score_id))
        if c.rowcount == 0:
            print "ow!"
        self._conn.commit()    
        
    def scores(self):
        c = self._conn.cursor()
        c.execute('SELECT SCORE_ID, SCORE, DURATION_SEC, GAME_NAME, GAME_VERSION, LEVEL, USER_ID, TIMESTAMP, CRASHED FROM SCORE ORDER BY SCORE_ID DESC')
        ret = []
        r = c.fetchone()
        while r is not None:
            ret.append(Score().load_from_tuple(r))
            r = c.fetchone()
        self._conn.commit()     
        return ret           
              
if __name__ == '__main__':        
       
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--create',action='store_true',help='create the database')
    parser.add_argument('-s','--scores',action='store_true',help='dump the scores')

    args = parser.parse_args()

    sql = SqlitePersistence()

    if args.create:
        sql._create();
    elif args.scores:
        sql.load()
        print "%-23s %3s %-20s %3s %4s %s" % ("Timestamp","Usr","Game","Scr","Time","Crashed")
        for s in sql.scores():
            print "%-23s %3d %20s %3d %4.2f %d" % (s.timestamp,s.user_id,s.game_name,s.score,s.duration_sec,s.crashed)
    else:
        sql.load()
        print sql.get_anonymous()   
       
            
