import json
import os
import Utilities
from noisewords import noise_words


def get_users():
        get_users_command = "SELECT userid, name FROM user"
        db_result_users = Utilities.db_con.executeAndRetrieveCommand(get_users_command)
        user_vector_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'UserInfo')
        for user in db_result_users:
                content = {}
                get_content_command2 = "SELECT content FROM post WHERE postid IN " + \
                                       "(SELECT postid FROM favorite WHERE userid =" + str(user[0]) +")" +\
                                        "UNION ALL SELECT content FROM post WHERE postid IN " + \
                                       "(SELECT postid FROM heart WHERE userid =" + str(user[0]) + ")"

                db_result_content = Utilities.db_con.executeAndRetrieveCommand(get_content_command2)
                file_path = os.path.join(user_vector_dir, str(user[0])+".json")
                for i in db_result_content:
                        words = str(i[0])
                        words = words.lower()
                        words = words.split(" ")
                        for k in words:
                                if not k in noise_words:
                                        if k not in content:
                                                content[k] = 1
                                        else:
                                                content[k] +=1
                with open(file_path, 'w+') as f:
                        # if os.path.exists(file_path):
                        jsonWrite = json.dump(content,f, indent = 4)

get_users()
