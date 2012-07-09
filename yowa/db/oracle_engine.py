import os
os.environ['NLS_LANG'] = 'American_America.UTF8'
from cx_Oracle import Connection

class Oracle_Connection(Connection):
    def __new__(cls, user, pwd, dsn):
        if '_conn' not in vars(cls):
            cls._conn = Connection.__new__(cls, user, pwd, dsn = dsn)
        
        return cls._conn
