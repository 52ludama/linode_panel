import base64
import json
import os

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = base64.b64encode(os.urandom(48))  # 前后端通信密钥
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'public.login'
login_manager.session_protection = 'strong'
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///linode_panel.sqlite'  # 数据库文件
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Users, LinodeToken, LinodeServer
from views import views


@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    return Users.query.get(user_id)


@app.errorhandler(404)  # 传入错误码作为参数状态
def error_date(error):  # 接受错误作为参数
    return render_template("404.html"), 404  # 返回对应的http状态码，和返回404错误的html文件


if __name__ == '__main__':
    db.create_all()
    user = Users.query.all()
    if user:
        pass
    else:
        print("====创建用户====")
        username = input("用户名：")
        password = input("密码：")
        user_admin = Users(username=username, password=password)
        db.session.add(user_admin)
        db.session.commit()
        print("====创建成功====")
    app.run(host='0.0.0.0', threaded=True)
