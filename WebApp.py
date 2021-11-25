from flask import Flask, render_template, url_for, request, redirect
import flask_login

app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    users = []
    ## todo get db connection for user
    ## users = getUser()
    if username not in users:
        return
    user = User()
    user.id = username
    return user



@login_manager.request_loader
def request_loader(request):
    # username = request.form.get('username')
    # if username not in users:
    #     return
    # user = User()
    # user.id = username
    # user.is_authenticated = request.form['password'] == users[username]['password']
    # ## can be improved
    # return user
    pass

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route("/")
def template_test():
    return render_template('index.html')
    # if request.method == 'GET':
    #     return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass
    # if request.method == 'GET':
    #     return render_template('index.html')
    #     username = request.form['username']
    # else:
    #     if request.form['username'] in users.keys():
    #         username = request.form['username']
    #         if request.form['password'] == users[username]['password']:
    #             user = User()
    #             user.id = username
    #             flask_login.login_user(user)
    #             return redirect(url_for('protected'))
    #     else:
    #         return 'Username invalid '
    #     return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Hi You are special ,Logged in as: ' + flask_login.current_user.id

if __name__ == '__main__':
    app.run(debug=True)