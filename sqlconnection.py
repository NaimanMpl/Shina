import mysql.connector

class Database():

    def __init__(self, host, database, user, pwd):
        self.host = host
        self.database = database
        self.user = user
        self.pwd = pwd

