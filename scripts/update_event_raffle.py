import json
import requests
from datetime import datetime
from helper import get_domain, get_user_id, get_user_token, generate_page
from get_activity import get_act_info
import raffle

DESIGN_API_URL = get_domain() + "/api/h5hy/api/v0/visible/h5/save"

def update_event(act_id, is_raffle):
    # 获取用户id
    user_id = get_user_id()
    user_token = get_user_token(user_id)
    token = user_token.get('token')

    # 获取模板数据
    payload = generate_page(act_id, token)
    # 查询活动信息
    act_data = get_act_info(act_id, token)

    # 保留活动开始和结束时间，可覆盖
    start_at = act_data['response']['activity']['start_time']
    end_at = act_data['response']['activity']['end_time']
    # 模板标识
    mark = act_data['response']['activity']['mark']

    form_controls = act_data['response']['rules']['form_controls']

    # 赋值活动数据
    forward = {
        "data": {
            "activity_id": act_id,
            "type": "designh5",
            "mark": mark,
            "indexpic": act_data['response']['activity']['indexpic'],
            "title": act_data['response']['activity']['title'],
            "introduce": act_data['response']['activity']['introduce'],
            "date": [
                datetime.fromtimestamp(start_at).strftime("%Y-%m-%d %H:%M:%S"),
                datetime.fromtimestamp(end_at).strftime("%Y-%m-%d %H:%M:%S")
            ],
            "limit": act_data['response']['rules']['limit'],
            "share_settings": act_data['response']['rules']['share_settings'],
            "start_time": start_at,
            "end_time": end_at,
            "form_controls": form_controls
        },
        "service": "designh5@form"
    }

    if int(is_raffle) == 1:
        raffle_data = {
            "title": act_data['response']['activity']['title'] + "抽奖活动",
            "brief": "抽奖规则"
        }
        raffle_res = raffle.add(token, raffle_data)
        if raffle_res['err_code'] == 0:
            raffle_activity_id = raffle_res.get('act_id', '')
            if raffle_activity_id:
                forward['data']['limit']['lottery_config']['open'] = 1
                forward['data']['limit']['lottery_config']['activity_id'] = raffle_activity_id


    payload['forward'] = forward
    payload['tid'] = act_id
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    # 再保存活动
    resp = requests.post(DESIGN_API_URL, json=payload, headers=headers)
    resp = resp.json()
    if resp['state'] == 200 and resp['result']['forward_id']:
        act_id = resp['result']['forward_id']
        return {
            'err_code': 0,
            'act_id': act_id
        }
    return {'err_code': -1}



if __name__ == "__main__":
    act = json.loads(input())
    result = update_event(act['act_id'], act['is_raffle'])
    print(result)