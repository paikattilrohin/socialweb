import mysql.connector
from datetime import datetime


class DB_CONNECTION:

    DB = mysql.connector.connect(host ="localhost", user ="root", passwd = "", database = "socialweb")
    db_cursor = DB.cursor()

    def executeAndRetrieveCommand(self, command):
        DB_CONNECTION.db_cursor.execute(command)
        return DB_CONNECTION.db_cursor.fetchall()

    def executeCommandOnly(self, command):
        DB_CONNECTION.db_cursor.execute(command)

db_con = DB_CONNECTION()

def createUser(name, username, password):
    existing_user = db_con.executeAndRetrieveCommand("SELECT * FROM user WHERE email ='" + username+"'")
    if(len(existing_user) == 0):
        command = "INSERT INTO user (name, email, password) VALUES " \
                  "('{fname}', '{femail}', '{fpassword}')".format(fname= name, femail = username, fpassword=password)
        db_con.executeCommandOnly(command)
        return True
    else:
        return False

def createpost(posts):
        print('post func')
        command = "INSERT INTO post (posts) VALUES " \
                  "('{fposts}')".format(fposts = posts)
        db_con.executeCommandOnly(command)
        return True


def checkUser(username):
    command = "SELECT * FROM user WHERE email='" + username +"'"
    user = db_con.executeAndRetrieveCommand(command)
    if len(user) == 1:
        return True
    return False

def check_username_pass(username, password):
    command = "SELECT * FROM user WHERE email='" + username +"' AND password='" +password+"'"
    user = db_con.executeAndRetrieveCommand(command)
    if len(user) == 1:
        return True
    return False