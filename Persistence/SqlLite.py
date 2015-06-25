import sqlite3
from Base import Persistence
import os

class SqlLitePersistence(Persistence)

    def __init__(self)
        self._conn = None
        pass
        
    def load(self):
        self._conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),'pcg.db')
        
        c = self._conn.cursor
        
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
        if len(c.fetchall()) == 0:
            c.execute("CREATE TABLE USER
            (user_id int auto_increment,
            first_name varchar(50),
            last_name varchar(50),
            email varchar(100),
            pin char(4))")