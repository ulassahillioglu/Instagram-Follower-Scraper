import sqlite3
import os
import json

class sqlClass:
    def __init__(self,db):
        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        self.create_columns = "id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, followers INTEGER, followees TEXT"
        self.columns = "username, followers, followees"
        
        
    def createTable(self,table):
        self.c.execute("CREATE TABLE IF NOT EXISTS {}({})".format(table,self.create_columns))
        self.conn.commit()
    
    def insertData(self,table,values):
        # if len(values) == 2:
        #     values + tuple("None")
        placeholders = ', '.join('?' * len(values))
        query = "INSERT INTO {}({}) VALUES({})".format(table,self.columns,placeholders)
        self.c.execute(query,values)
        self.conn.commit()
    
    def selectData(self,table):
        query = "SELECT {} FROM {}".format(self.columns,table)
        self.c.execute(query)
        data = self.c.fetchall()
        return data
    
    def removeDuplicatesByUserName(self,table):
        query = "DELETE FROM {} WHERE id NOT IN (SELECT MIN(id) FROM {} GROUP BY username)".format(table,table)
        self.c.execute(query)
        self.conn.commit()
    
    def commit(self):
        self.conn.commit()
        
    def close(self):
        self.conn.close()
    
    def __del__(self):
        self.conn.close()
        
    