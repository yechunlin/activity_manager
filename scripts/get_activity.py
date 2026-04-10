import json

import requests

from helper import get_domain, get_user_id, get_user_token

API = '/api/designh5hy/ax/design-h5/manage/activity/'

def get_act_info(act_id, token):
    url = get_domain() + API + act_id
    headers = {'Authorization': token}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        return {}


def get_activity(act_id):
    # 获取用户id
    user_id = get_user_id()
    user_token = get_user_token(user_id)
    token = user_token.get('token')
    res = get_act_info(act_id, token)
    if res:
        return {
            "act_id": act_id,
            "act_type": "designh5",
            "title": res['response']['activity']['title'],
            "brief": res['response']['activity']['introduce'],
            "post": {
                "post_img": {
                    "url": res['response']['activity']['indexpic'],
                    "size": "",
                    "desc_str": ""
                }
            },
            "fields": {
                "fields": res['response']['rules']['form_controls'][0]['controls']
            }
        }
    else:
        return {"msg": "获取失败"}


if __name__ == "__main__":
    act = json.loads(input())
    result = get_activity(act['act_id'])
    print(result)
