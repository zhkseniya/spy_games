import requests
import time
import json
import os
from pprint import pprint

user_id = 171691064
token = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'

def get_groups(token,user_id):
    response = requests.get('https://api.vk.com/method/groups.get',params=dict(user_ids=user_id, access_token=token, v=5.80), verify=False).json()['response']
    return {item for item in response['items']}

def get_members_groups(token,group_id):
    response = requests.get('https://api.vk.com/method/groups.getMembers', params=dict(group_id=group_id, access_token=token, v=5.80, filter='friends'), verify=False)
    return response.json()['response']

def get_name_groups(token,group_id):
    response = requests.get('https://api.vk.com/method/groups.getById', params=dict(group_id=group_id, access_token=token, v=5.80, fields='members_count'), verify=False)
    return response.json()['response']

def wright_json(data):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "groups.json"), "w", encoding='utf8') as file:
        json.dump(data, file)

my_groups_id = get_groups(token, user_id)

success_groups = []

for id in my_groups_id:
    try:
        pprint('/')
        resp = get_members_groups(token, id)
    except:
        time.sleep(2)
        pprint('/')
        resp = get_members_groups(token, id)
    if resp['count'] == 0:
        try:
            pprint('/')
            name_groups = get_name_groups(token, id)
        except:
            time.sleep(2)
            pprint('/')
            name_groups = get_name_groups(token, id)
        for group in name_groups:
            success_groups.append({'name': group['name'], 'gid': group['id'], 'members_count': group['members_count']})

wright_json(success_groups)
pprint('Информация по группам, в которых состоит пользователь записана в файл')