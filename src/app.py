from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os
import time
import glob
from general_functionalities import capture_image, capture_video

# initial setup
app = Flask(__name__)
app.secret_key = 'very_secret_key_here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    id = 1
    username = '488team7'
    password = '488team7'

# load user with corresponding ID
@login_manager.user_loader
def load_user(user_id):
    return User() if int(user_id) == User.id else None

# login for authentication functionality
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

# logout for authentication functionality
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# main page
@app.route('/main')
@login_required
def main():
    return render_template('main.html')

# for logging messages
@app.route('/logs')
@login_required
def logs():
    filepath = '../logs.txt'
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.readlines()[-10:]
    else:
        content = ['No logs found']
    return render_template('logs.html', logs=content)

# for retrieval of last image stored
@app.route('/take_picture')
@login_required
def take_picture():
    image_folder = '/media/ecse488-7/group7/images'
    list_of_files = glob.glob(f'{image_folder}/*.jpg')  # Assuming the images are in jpg format
    if not list_of_files:
        return "No images found"
    latest_image = max(list_of_files, key=os.path.getctime)
    return send_file(latest_image, mimetype='image/jpeg')

# for retrieval of last video stored
@app.route('/take_video')
@login_required
def take_video():
    video_folder = '/media/ecse488-7/group7/videos'
    list_of_files = glob.glob(f'{video_folder}/*.mpg')  # Adjusted to .mpg file extension
    if not list_of_files:
        return "No videos found"
    latest_video = max(list_of_files, key=os.path.getctime)
    return send_file(latest_video, mimetype='video/mpeg')  # Corrected MIME type for MPG

# for turning off the system
@app.route('/turn_off', methods=['POST'])
@login_required
def turn_off():
    os.system("sudo supervisorctl stop driver")
    return redirect(url_for('main'))

# for restarting the system
@app.route('/restart', methods=['POST'])
@login_required
def restart():
    os.system("sudo supervisorctl restart driver")
    return redirect(url_for('main'))

# run program for website
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
