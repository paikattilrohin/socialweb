import mysql.connector
from datetime import datetime

class DB_CONNECTION:
    DB = mysql.connector.connect(host ="localhost", user ="root", passwd ="", database ="socialweb")
    db_cursor = DB.cursor()

    def executeCommand(self, command):
        DB_CONNECTION.db_cursor.execute(command)
        return DB_CONNECTION.db_cursor.fetchall()



db_con = DB_CONNECTION()

print(db_con.executeCommand("show tables"))




