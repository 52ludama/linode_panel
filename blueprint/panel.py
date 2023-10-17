import json
from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import login_required, logout_user

from main import db
from models import Users

panel = Blueprint('panel', __name__)


@panel.route('/index', methods=['GET'])
@login_required
def index():
    return render_template("index.html")


@panel.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@panel.route('/linode_token', methods=['GET', 'POST'])
@login_required
def token():
    return render_template("linode_token.html")


@panel.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    return render_template('setting.html')


@panel.route('/reset_admin', methods=['GET', 'POST'])
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
