import flask
from flask import Flask, render_template, url_for, request, redirect
import flask_login
from flask_login import current_user

import Utilities

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'Enterprise Web Dev'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    userexists = Utilities.checkUser(username)
    if userexists:
        user = User()
        user.id = username
        return user


@login_manager.request_loader
def request_loader(req):
    username = req.form.get('username')
    password = req.form.get('password')
    if username and password:
        login_status = Utilities.check_username_pass(username, password)
        if login_status:
            user = User()
            # user.id = username
            # user.is_authenticated = login_status
            return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/view', methods=['GET'])
def view_post():
    return render_template('index.html')


@app.route('/', methods=['GET'])
def index():

    posts = [{'postid': 1000, 'content': 'Hello', 'name': 'Rohin '},
             {'postid': 1001, 'content': 'Goodbye', 'name': 'DUMBASS'}]


    return render_template('index.html', all_posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        login_status = Utilities.check_username_pass(username, password)
        if login_status:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect('home')
        else:
            return 'wrong'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if flask.request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['name']
        email = request.form['emailID']
        password = request.form['password']
        success = Utilities.createUser(name, email, password)
        if success:
            user = User()
            user.id = email
            flask_login.login_user(user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('signup'))


@app.route('/content', methods=['GET', 'POST'])
def posting():
    posts = request.form['content']
    success = Utilities.createpost(posts)
    print('step2')
    if success:
        return 'post created'
    else:
        return 'post not created'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


@app.route('/logout', methods=['GET'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


@app.route('/home', methods=['GET'])
@flask_login.login_required
def home():
    return render_template('loggedin.html')


@app.route('/post', methods=['POST'])
@flask_login.login_required
def post():
    return render_template('loggedin.html')


@app.route('/profile', methods=['GET'])
@flask_login.login_required
def profile():
    return render_template('loggedin.html')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
