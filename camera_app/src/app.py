from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import subprocess
import os
import time
from general_functionalities import capture_image, capture_video
from driver import camera, encoder

app = Flask(__name__)
app.secret_key = 'very_secret_key_here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    id = 1
    username = '488team7'
    password = '488team7'

@login_manager.user_loader
def load_user(user_id):
    return User() if int(user_id) == User.id else None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == User.username and password == User.password:
            user = User()
            login_user(user)
            return redirect(url_for('main'))
        else:
            return 'Invalid username or password'
    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/main')
@login_required
def main():
    return render_template('main.html')

@app.route('/logs')
@login_required
def logs():

    filepath = '../logs.txt'
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.readlines()[-10:]
            print(content)


    else:
        content = ['No logs found']
    return render_template('logs.html', logs=content)

@app.route('/take_picture')
@login_required
def take_picture():
    timestamp = time.strftime("%m-%d-%Y_%H-%M-%S")
    image_path = capture_image(camera, timestamp)
    return send_file(image_path, mimetype='image/jpeg')

@app.route('/take_video')
@login_required
def take_video():
    timestamp = time.strftime("%m-%d-%Y_%H-%M-%S")
    video_path = capture_video(camera, encoder, timestamp, 5)
    return send_file(video_path, mimetype='video/mpeg')

if __name__ == '__main__':
    app.run(debug=True)