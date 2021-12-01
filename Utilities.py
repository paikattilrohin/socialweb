import mysql.connector
from datetime import datetime
import constants
from noisewords import noise_words
import json
import os


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


def get_suggested_posts(user_id):
    name = get_name_for_user(user_id)
    suggested_posts = []
    if name is not None:
        userid = user_id
        command1 = " SELECT userid from post WHERE postid IN (SELECT postid from heart where userid =" + str(userid)
        command2 = " SELECT postid from post WHERE postid IN (SELECT postid from heart where userid =" + str(userid)
        command = "SELECT content, postid, name FROM post WHERE postid IN (SELECT postid FROM heart WHERE userid IN (" +command1 + "))) AND postid NOT IN (" + command2 + "))"
        db_result_posts = db_con.executeAndRetrieveCommand(command)
        for post in db_result_posts:
            suggested_posts.append({
                'name': post[2],
                'content': post[0],
                'postid': post[1]
            })
    return suggested_posts


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

def get_dashboard_stats(user_id):
    command_likes = "SELECT COUNT(likeid) FROM heart WHERE userid="+str(user_id)
    command_favorite = "SELECT COUNT(favoriteid) FROM favorite WHERE userid="+ str(user_id)
    command_posts = "SELECT COUNT(postid) FROM post WHERE userid="+ str(user_id)
    db_like = db_con.executeAndRetrieveCommand(command_likes)
    db_favorite = db_con.executeAndRetrieveCommand(command_favorite)
    db_post = db_con.executeAndRetrieveCommand(command_posts)
    dashboard = {'like':db_like[0][0], 'favorite': db_favorite[0][0], 'post':db_post[0][0]}
    return dashboard

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




# select content, (case when content like '%python%' then 1 else 0 end +
# case when content like '%write%' then 1 else 0 end +
# case when content like '%file%' then 1 else 0 end) as "value" from post
# where content like '%python%' OR content like '%write%' OR content like '%file%'
# order by value DESC;
#
def get_unlogged_search_posts(search_query):
    all_posts = []
    search_words = search_query.split()
    case_command =""
    where_command =""
    for k in range(len(search_words)):
        search_words[k] = "content like \'%" + search_words[k] + "%\'"
        if k is not len(search_words)-1:
            case_command += "case when " + search_words[k] + " then 1 else 0 end + "
            where_command += search_words[k] + " OR "
        else:
            case_command += "case when " + search_words[k] +" then 1 else 0 end"
            where_command += search_words[k]

        k+=1
    command = "SELECT content, postid, name, (" + case_command + ") as \"value\"  FROM post WHERE " + where_command + " ORDER BY VALUE DESC"
    # print(command)
    db_result_posts = db_con.executeAndRetrieveCommand(command)
    for post in db_result_posts:
        all_posts.append({
            'name': post[2],
            'content': post[0],
            'postid': post[1],
            'rank': post[3]
         })
    return all_posts

def swap(post1, post2):
    #swapping names
    tname = post1['name']
    post1['name'] = post2['name']
    post2['name'] = tname

    #swapping content
    tcontent = post1['content']
    post1['content'] = post2['content']
    post2['content']= tcontent

    # swapping scores
    tscore = post1['score']
    post1['score'] = post2['score']
    post2['score'] = tscore

    #swapping postids
    tpostid = post1['postid']
    post1['postid'] = post2['postid']
    post2['postid'] = tpostid
    return post1, post2

def get_logged_search_posts(search_query, user_id):
    all_posts = get_unlogged_search_posts(search_query)
    user_vector_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'UserInfo')
    file_path = os.path.join(user_vector_dir, str(user_id) + ".json")
    if os.path.exists(file_path):
        f = open(file_path, 'r')
        data = json.load(f)
        for post in all_posts:
            score = 0
            words = str(post['content'])
            words = words.lower()
            words = words.split(" ")
            for k in words:
                if k in data:
                    score += data[k]
                    post['score'] = score
                else:
                    post['score'] = 0
        for i in range(len(all_posts)):
            for j in range(i + 1, len(all_posts)):
                if (all_posts[i]['rank'] == all_posts[j]['rank']):
                    if(all_posts[i]['score'] < all_posts[j]['score']):
                        swap(all_posts[i], all_posts[j])
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

