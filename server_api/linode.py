import json

import requests


def linode_getinfo(token_key):
    token_info = []
    url = "https://api.linode.com/v4/linode/instances"
    h = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token_key
    }
    res = requests.get(url=url, headers=h)
    data = res.json()
    try:
        token_info.append(data['results'])
        token_info.append('ok')
        token_info.append(data['data'])
    except KeyError:
        token_info.append(data['errors'])
        token_info.append('errors')
    return token_info


def linode_creat_server(select_type, select_region, select_token, select_image, root_pass, server_label: str):
    url = "https://api.linode.com/v4/linode/instances"
    h = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + select_token
    }
    d = {
        'image': select_image,
        'root_pass': root_pass,
        'label': server_label,
        'type': select_type,
        'region': select_region
    }
    try:
        res = requests.post(url=url, headers=h, data=json.dumps(d))
        data = res.json()
        server_info = ['ok', data['id'], data['ipv4'][0], data['ipv6'], data['label']]
        return server_info
    except:
        return ['error']


def linode_del_server(linode_id, linode_key):
    url = "https://api.linode.com/v4/linode/instances/" + str(linode_id)
    h = {
        "Authorization": "Bearer " + linode_key
    }
    try:
        res = requests.delete(url=url, headers=h)
        data = res.json()
        print(data)
        if data == {}:
            return 'ok'
        else:
            return 'error'
    except:
        return 'error'


def linode_info_server(linode_id, linode_key):
    url = "https://api.linode.com/v4/linode/instances/" + str(linode_id)
    h = {
        "Authorization": "Bearer " + linode_key
    }
    res = requests.get(url=url, headers=h)
    data = res.json()
    return data

