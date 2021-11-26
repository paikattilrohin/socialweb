import mysql.connector
from datetime import datetime
import constants


class DB_CONNECTION:
    DB = mysql.connector.connect(host="localhost", user="root", passwd=constants.password, database=constants.database, autocommit=True)
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
        user_id = existing_user[0][0]
    return user_id


def create_post(content, userid):
    name = get_name_for_user(userid)
    command = "INSERT INTO post (content, userid, name ) VALUES " \
              "('{fcontent}', '{fuserid}', '{fname}')".format(fcontent=content, fuserid=userid, fname=name)
    db_con.executeCommandOnly(command)
    return True


def check_user(username):
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


def get_posts_for_user(user_id):
    name = get_name_for_user(user_id)
    all_posts = []
    if name is not None:
        userid = user_id
        command = "SELECT content, postid, name FROM post WHERE userid != '" + str(userid) + "' ORDER BY date DESC"
        db_result_posts = db_con.executeAndRetrieveCommand(command)
        for post in db_result_posts:
            all_posts.append({
                'name': post[2],
                'content': post[0],
                'postid': post[1]
            })
    return all_posts


def get_name_for_user(user_id):
    command = "SELECT name FROM user WHERE userid = '" + str(user_id) + " ' "
    result = db_con.executeAndRetrieveCommand(command)
    if len(result) == 1:
        return result[0][0]
    return None


def get_posts_by_user(user_id):
    name = get_name_for_user(user_id)
    all_posts = []
    if name is not None:
        userid = user_id
        command = "SELECT content, postid FROM post WHERE userid = '" + str(userid) + "' ORDER BY date DESC"
        db_result_posts = db_con.executeAndRetrieveCommand(command)
        for post in db_result_posts:
            all_posts.append({
                'name': name,
                'content': post[0],
                'postid': post[1]
            })
    return all_posts


def get_unlogged_user_posts():
    all_posts = []
    command = "SELECT content, postid, name FROM post ORDER BY date DESC"
    db_result_posts = db_con.executeAndRetrieveCommand(command)
    for post in db_result_posts:
        all_posts.append({
            'name': post[2],
            'content': post[0],
            'postid': post[1]
        })
    return all_posts


def add_like(user_id, post_id):
    command = "SELECT * FROM heart WHERE postid =" + str(post_id) + " AND userid =" + str(user_id)
    likes = db_con.executeAndRetrieveCommand(command)
    if len(likes) == 0:
        command = "INSERT INTO heart (userid, postid ) VALUES " \
                  "('{fuser_id}', '{fpost_id}')".format(fpost_id=post_id, fuser_id=user_id)
        db_con.executeCommandOnly(command)
        return True
    else:
        db_con.executeCommandOnly("DELETE FROM heart WHERE postid =" + str(post_id) + " AND userid =" + str(user_id) +"")


def add_favorite(user_id, post_id, tags):
    command = "SELECT * FROM favorite WHERE postid =" + str(post_id) + " AND userid =" + str(user_id) + ""
    favorites = db_con.executeAndRetrieveCommand(command)
    if len(favorites) == 0:
        command = "INSERT INTO favorite (userid, postid, tag) VALUES " \
                  "('{fuser_id}', '{fpost_id}', '{ftags}')".format(fpost_id=post_id, fuser_id=user_id, ftags=tags)
        db_con.executeCommandOnly(command)
        return True
    else:
        db_con.executeCommandOnly("DELETE FROM favorite WHERE postid =" + str(post_id) + " AND userid =" + str(user_id) + "")

