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
    userexists = Utilities.check_user(username)
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
    return redirect(url_for('login'))


@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        posts = Utilities.get_unlogged_user_posts()
        return render_template('index.html', all_posts=posts)


@app.route('/search', methods=['GET'])
def search():
    search_query = request.args['search'] ## this is the searched string use this to apply the logic
    if current_user.is_authenticated:
        posts = []
        return render_template('index.html', all_posts=posts)
        # return render_template('logged_search.html', all_posts=posts)  ## create these templates
    else:
        posts = Utilities.get_unlogged_user_posts()
        # return render_template('unlogged_search.html', all_posts=posts)
        return render_template('index.html', all_posts=posts)  ## create these templates




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
            return redirect(url_for('home'))
        else:
            return 'wrong'


@app.route('/redirect', methods=['POST'])
def redir():
    return redirect(url_for('signup'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if flask.request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['name']
        email = request.form['emailID']
        password = request.form['password']
        success = Utilities.create_user(name, email, password)
        if success:
            user = User()
            user.id = email
            flask_login.login_user(user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('signup'))


@app.route('/createpost', methods=['POST'])
@flask_login.login_required
def posting():
    content = request.form['postcontent']
    user_id = Utilities.get_user_id(current_user.id)
    success = Utilities.create_post(content, user_id)
    if success:
        return redirect('profile')
    else:
        return 'post not created'


@app.route('/logout', methods=['GET'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


@app.route('/home', methods=['GET'])
@flask_login.login_required
def home():
    user_id = Utilities.get_user_id(current_user.id)
    name = Utilities.get_name_for_user(user_id)
    posts = Utilities.get_posts_for_user(user_id)
    return render_template('loggedin.html', all_posts = posts )


@app.route('/profile', methods=['GET'])
@flask_login.login_required
def profile():
    user_id = Utilities.get_user_id(current_user.id)
    name = Utilities.get_name_for_user(user_id)
    posts = Utilities.get_posts_by_user(user_id)
    return render_template('loggedin.html', all_posts = posts, name = name )


@app.route('/like', methods=['POST'])
@flask_login.login_required
def like():
    user_id = Utilities.get_user_id(current_user.id)
    post_id = request.form['postid']
    Utilities.add_like(user_id, post_id)
    return "1"


@app.route('/favorite', methods=['POST'])
@flask_login.login_required
def favorite():
    user_id = Utilities.get_user_id(current_user.id)
    post_id = request.form['postid']
    tags = request.form['tag']
    Utilities.add_favorite(user_id, post_id, tags)
    return "1"



if __name__ == '__main__':
    app.run(debug=True, threaded=True)
