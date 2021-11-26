import mysql.connector
from datetime import datetime


class DB_CONNECTION:
    DB = mysql.connector.connect(host="localhost", user="root", passwd="", database="socialweb", autocommit=True)
    db_cursor = DB.cursor()

    def executeAndRetrieveCommand(self, command):
        DB_CONNECTION.db_cursor.execute(command)
        return DB_CONNECTION.db_cursor.fetchall()

    def executeCommandOnly(self, command):
        DB_CONNECTION.db_cursor.execute(command)


db_con = DB_CONNECTION()


def create_user(name, username, password):
    existing_user = db_con.executeAndRetrieveCommand("SELECT * FROM user WHERE email ='" + username + "'")
    if len(existing_user) == 0:
        command = "INSERT INTO user (name, email, password) VALUES " \
                  "('{fname}', '{femail}', '{fpassword}')".format(fname=name, femail=username, fpassword=password)
        db_con.executeCommandOnly(command)
        return True
    else:
        return False


def get_user_id(username):
    user_id = -1
    existing_user = db_con.executeAndRetrieveCommand("SELECT userid FROM user WHERE email ='" + username + "'")
    if len(existing_user) == 1:
        user_id = existing_user[0]
    return user_id

def createpost(content, userid):
    command = "INSERT INTO post (content, userid ) VALUES " \
              "('{fcontent}', '{fuserid}')".format(fcontent=content, fuserid=userid)
    db_con.executeCommandOnly(command)
    return True


def checkUser(username):
    command = "SELECT * FROM user WHERE email='" + username + "'"
    user = db_con.executeAndRetrieveCommand(command)
    if len(user) == 1:
        return True
    return False


def check_username_pass(username, password):
    command = "SELECT * FROM user WHERE email='" + username + "' AND password='" + password + "'"
    user = db_con.executeAndRetrieveCommand(command)
    if len(user) == 1:
        return True
    return False


def get_posts_for_user(username):
    ### improve
    command = "SELECT * FROM user WHERE email != '" + username + " '"
    posts = db_con.executeAndRetrieveCommand(command)
    all_posts = []
    return all_posts


def get_posts_by_user(username):
    ### improve
    command = "SELECT name, userid FROM user WHERE email = '" + username + " ' "
    result = db_con.executeAndRetrieveCommand(command)
    all_posts = []
    if len(result) > 0:
        userid = result[1]
        name = result[0]
        command = "SELECT CONTENT FROM post WHERE userid = '" + userid + "' ORDER BY date DESC"
        db_result_posts = db_con.executeAndRetrieveCommand(command)
        for post in db_result_posts:
            all_posts.append({
                'name': name,
                'content': post[0]
            })
    return all_posts


def get_unlogged_user_posts(username):
    ### improve
    command = "SELECT * FROM user WHERE email = '" + username + " ' "
    posts = db_con.executeAndRetrieveCommand(command)
    return None
