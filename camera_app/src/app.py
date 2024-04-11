from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import subprocess
import os
from general_functionalities import capture_image, capture_video

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
            content = f.readlines()[-5:]
            print(content)


    else:
        content = ['No logs found']
    return render_template('logs.html', logs=content)


def capture_img():
    subprocess.run(["libcamera-still", "-o", "../images/photo.jpg"])

def capture_vid():
    subprocess.run(["libcamera-vid", "-o", "../videos/video.h264", "-t", "5000"])

@app.route('/take_picture')
@login_required
def take_picture():
    capture_image()
    return send_file("../images/photo.jpg", mimetype='image/jpeg')

@app.route('/take_video')
@login_required
def take_video():
    capture_video()
    return send_file("../videos/video.h264", mimetype='video/h264')

if __name__ == '__main__':
    app.run(debug=True)
