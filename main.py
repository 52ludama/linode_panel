import base64
import json
import os

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from linode_token import linode_token
from linode_server import linode_server

app = Flask(__name__)
app.secret_key = base64.b64encode(os.urandom(48))  # 前后端通信密钥
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.register_blueprint(linode_token)
app.register_blueprint(linode_server)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///linode_panel.sqlite'  # 数据库文件
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(16))

    def __init__(self):
        self.username = 'admin'
        self.password = 'admin'


class LinodeToken(db.Model):
    __tablename__ = 'linode_token'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    token_key = db.Column(db.String(50))
    add_date = db.Column(db.String(10))
    sum = db.Column(db.Integer)
    status = db.Column(db.String(10))
    label = db.Column(db.String(50))


class LinodeServer(db.Model):
    __tablename__ = 'linode_server'
    linode_id = db.Column(db.Integer, primary_key=True)
    ipv4 = db.Column(db.String(15))
    ipv6 = db.Column(db.String(50))
    type = db.Column(db.String(30))
    region = db.Column(db.String(30))
    token_id = db.Column(db.Integer)
    label = db.Column(db.String(50))


@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    return Users.query.get(user_id)


@app.errorhandler(404)  # 传入错误码作为参数状态
def error_date(error):  # 接受错误作为参数
    return render_template("404.html"), 404  # 返回对应的http状态码，和返回404错误的html文件


@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return redirect(url_for('index'))


@app.route('/index', methods=['GET'])
@login_required
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():  # 登录模块
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        if not all([username, password]):
            return json.dumps(['error', '参数不完整'])
        else:
            user = Users.query.filter(Users.username == username, Users.password == password).first()
            if user:
                login_user(user)
                return json.dumps(['ok'])
            else:
                return json.dumps(['error', '登录失败'])
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    return render_template('setting.html')


@app.route('/reset_admin', methods=['GET', 'POST'])
def reset_admin():  # 登录模块
    if request.method == 'POST':
        old_username = request.json['old_username']
        old_password = request.json['old_password']
        new_username = request.json['new_username']
        new_password = request.json['new_password']
        if not all([old_username, old_password, new_username, new_password]):
            return json.dumps(['error', '参数不完整'])
        else:
            user = Users.query.filter(Users.username == old_username, Users.password == old_password).first()
            if user:
                user.username = new_username
                user.password = new_password
                db.session.commit()
                logout_user()
                return json.dumps(['ok', '修改成功，即将退出登录'])
            else:
                return json.dumps(['error', '修改失败'])


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', threaded=True)
