import requests
import time
import json
import os
from pprint import pprint
from sys import getdefaultencoding


user_id = 171691064
token = '312c86ee9f02c0b2e15ee55cf72eacde308ff4c9ceb3e44db1ebe9d5f7fd954d2ad61d93740709896c896'
groups_get = 'groups.get'
members_groups_get = 'groups.getMembers'
name_groups_get = 'groups.getById'
number_of_friends = 0


def request(method, params):
    return requests.get(f'https://api.vk.com/method/{method}', params=params, verify=False)


def get_groups(user_id):
    params = dict(user_id=user_id, access_token=token, v=5.80)
    try:
        pprint('/')
        response = request(groups_get, params).json()['response']
        time.sleep(0.2)
    except KeyError as le:
        pprint('Ошибка: {}'.format(le))
    except Exception as e:
        pprint('Ошибка выполнения запроса: {}'.format(e))
    else:
        return response


def get_name_groups(group_id):
    params = dict(group_id=group_id, access_token=token, v=5.80, fields='members_count')
    try:
        pprint('/')
        response = request(name_groups_get, params).json()['response']
        time.sleep(0.2)
    except KeyError as le:
        pprint('Ошибка: {}'.format(le))
    except Exception as e:
        pprint('Ошибка выполнения запроса: {}'.format(e))
    else:
        for group in response:
            success_groups.append({'name': group['name'], 'gid': group['id'], 'members_count': group['members_count']})
        return success_groups


def get_members_groups(my_groups, success_groups):

    for group_id in my_groups['items']:
        params = dict(group_id=group_id, access_token=token, v=5.80, filter='friends')
        try:
            pprint('/')
            response = request(members_groups_get, params).json()['response']
            time.sleep(0.2)
        except KeyError as le:
            pprint('Ошибка: {}'.format(le))
        except Exception as e:
            pprint('Ошибка выполнения запроса: {}'.format(e))
        else:
            if number_of_friends != 0:
                if response['count'] <= number_of_friends:
                    get_name_groups(group_id)
            else:
                if response['count'] == 0:
                    get_name_groups(group_id)
    return success_groups


def write_json(data):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "groups.json"), "w", encoding=getdefaultencoding()) as file:
        json.dump(data, file, ensure_ascii=False)
    pprint('Информация по группам, в которых состоит пользователь записана в файл')


success_groups = []


my_groups_id = get_groups(user_id)


get_members_groups(my_groups_id, success_groups)


write_json(success_groups)
