import datetime
import json

from flask import Blueprint, render_template, request
from flask_login import login_required
from server_api.linode import linode_getinfo

linode_token = Blueprint('linode_token', __name__)


@linode_token.route('/add', methods=['GET', 'POST'])
@login_required
def add_token():
    if request.method == 'POST':
        token_key = request.json['token_key']
        token_label = request.json['token_label']
        info = linode_getinfo(token_key)
        if info[1] == 'ok':
            add_date = datetime.datetime.now().strftime('%Y-%m-%d')
            token_sum = info[0]
            token_status = 'ok'
            from main import LinodeToken,db,LinodeServer
            token_1 = LinodeToken(token_key=token_key,add_date=add_date,sum=token_sum,status=token_status,label=token_label)
            db.session.add(token_1)
            db.session.commit()
            linode_token = LinodeToken.query.filter(LinodeToken.token_key == token_key).first()
            for item in info[2]:
                server_1 = LinodeServer(linode_id=item['id'], ipv4=item['ipv4'][0], ipv6=item['ipv6'], type=item['type'], region=item['region'], token_id = str(linode_token.id), label = item['label'])
                db.session.add(server_1)
                db.session.commit()
            return json.dumps(['ok'])
        else:
            return json.dumps(['error'])


@linode_token.route('/del', methods=['GET', 'POST'])
@login_required
def del_token():
    if request.method == 'POST':
        token_id = request.json['token_id']
        from main import LinodeToken, db, LinodeServer
        try:
            db.session.query(LinodeToken).filter(LinodeToken.id == token_id).delete()
            db.session.query(LinodeServer).filter(LinodeServer.token_id == token_id).delete()
            db.session.commit()
            db.session.close()
            return json.dumps(['ok'])
        except:
            return json.dumps(['error'])


@linode_token.route('/check', methods=['GET', 'POST'])
@login_required
def check_token():
    from main import LinodeToken, db
    if request.method == 'POST':
        data = LinodeToken.query.all()
        for item in data :
            info = linode_getinfo(item.token_key)
            if info[1] != 'ok':
                item.status = 'error'
                db.session.commit()
            else:
                item.status = 'ok'
                item.sum = int(info[0])
                db.session.commit()
    return json.dumps(['ok'])


@linode_token.route('/list', methods=['GET', 'POST'])
@login_required
def get_list():
    if request.method == 'POST':
        page_num = request.json['page_num']
        try:
            page_size = request.json['page_size']
        except:
            page_size = 10
        from main import LinodeToken
        linode_token_list_1 = LinodeToken.query.paginate(page=page_num, per_page=page_size)
        result_list = []
        for info in linode_token_list_1.items:
            linode_token_list_2 = [info.id, info.token_key, info.add_date, info.sum, info.status, info.label]
            result_list.append(linode_token_list_2)
        all_info = {
            'pages': linode_token_list_1.pages,
            'total': linode_token_list_1.total,
            'data': result_list
        }
        return json.dumps(all_info)