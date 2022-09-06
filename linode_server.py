import json

from flask import Blueprint, render_template, request
from flask_login import login_required
from linode import linode_creat_server, linode_del_server

linode_server = Blueprint('linode_server', __name__)


@linode_server.route('/linode_server/list', methods=['GET', 'POST'])
@login_required
def get_server_list():
    if request.method == 'POST':
        page_num = request.json['page_num']
        from main import LinodeServer
        linode_server_list_1 = LinodeServer.query.paginate(page=page_num, per_page=10)
        result_list = []
        for info in linode_server_list_1.items:
            linode_token_list_2 = [info.linode_id, info.ipv4, info.ipv6, info.type, info.region, info.token_id,
                                   info.label]
            result_list.append(linode_token_list_2)
        all_info = {
            'pages': linode_server_list_1.pages,
            'total': linode_server_list_1.total,
            'data': result_list
        }
        return json.dumps(all_info)


@linode_server.route('/linode_server/server_view', methods=['GET', 'POST'])
@login_required
def get_server_view():
    linode_id = request.args.get('linode_id')
    from main import LinodeServer, LinodeToken
    linode_server_token_1 = LinodeServer.query.filter(LinodeServer.linode_id == linode_id).first()
    linode_server_token_2 = LinodeToken.query.filter(LinodeToken.id == linode_server_token_1.token_id).first()
    return render_template("linode_server.html", linode_server=linode_server_token_1, token_key=linode_server_token_2.token_key)


@linode_server.route('/linode_server/creat', methods=['GET', 'POST'])
@login_required
def server_creat():
    if request.method == 'POST':
        select_token = request.json['linode_token']
        select_type = request.json['linode_type']
        select_region = request.json['linode_region']
        select_image = request.json['linode_image']
        root_pass = request.json['root_pass']
        server_label_1 = request.json['server_label']
        from main import LinodeToken, LinodeServer, db
        select_key = LinodeToken.query.filter(LinodeToken.id == select_token).first()
        result = linode_creat_server(select_type, select_region, select_key.token_key, select_image, root_pass,
                                     server_label_1)
        if result[0] == 'ok':
            server_1 = LinodeServer(linode_id=result[1], ipv4=result[2], ipv6=result[3], type=select_type,
                                    region=select_region, token_id=str(select_token), label=result[4])
            db.session.add(server_1)
            db.session.commit()
        return json.dumps(result)


@linode_server.route('/linode_server/del', methods=['GET', 'POST'])
@login_required
def server_del():
    if request.method == 'POST':
        server_id = request.json['server_id']
        server_key = get_key(server_id)
        result = linode_del_server(server_id, server_key)
        if result == 'ok':
            from main import LinodeServer, db
            db.session.query(LinodeServer).filter(LinodeServer.linode_id == server_id).delete()
            db.session.commit()
            db.session.close()
        return json.dumps([result])


@linode_server.route('/linode_server/info', methods=['GET', 'POST'])
@login_required
def server_info():
    if request.method == 'POST':
        server_id = request.json['server_id']
        server_key = get_key(server_id)
        result = linode_del_server(server_id, server_key)
        return json.dumps([result])


def get_key(server_id):
    from main import LinodeToken, LinodeServer, db
    linode_server_token_1 = LinodeServer.query.filter(LinodeServer.linode_id == server_id).first()
    linode_server_token_2 = LinodeToken.query.filter(LinodeToken.id == linode_server_token_1.token_id).first()
    return linode_server_token_2.token_key
