import json
from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import login_user
from models import Users

public = Blueprint('public', __name__)


@public.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return redirect(url_for('panel.index'))


@public.route('/login', methods=['GET', 'POST'])
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
