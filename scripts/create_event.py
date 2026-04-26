import json
from urllib.parse import quote
import requests
import os
import uuid

from helper import fix_url_scheme, get_domain, get_user_id, get_user_token
import designh5, raffle

# 开启活动
def open_activity(activity_id, token):
    url = get_domain() + '/api/designh5hy/ax/design-h5/manage/activity/' + activity_id + '/status/auto'
    headers = {'Authorization': token}
    requests.put(url, headers=headers)

# 创建活动二维码
def create_qrcode(link, token) -> str:
    url = get_domain() + '/api/i/qrcode/create?text=' + quote(link)
    headers = {'Authorization': token}
    res = requests.get(url, headers=headers).json()
    qrcode_url = res.get('qrcode_url') or ''
    return fix_url_scheme(qrcode_url)

# 活动生成控制器
def create_event(data):
    # 获取用户id
    user_id = get_user_id()
    user_token = get_user_token(user_id)
    token = user_token.get('token')
    # 获取活动类型
    act_type = data['act_type']
    if act_type == "designh5":
        # 报名
        res = designh5.add(token, data)
    elif act_type == "raffle":
        # 抽奖
        res = raffle.add(token, data)
    else:
        # 默认
        res = {"err_code": -1}

    if res['err_code'] == 0:
        title = res.get('title')
        act_url = res.get('url')
        act_id = res.get('act_id')
        # 尝试开启活动，成功与否都行
        open_activity(act_id, token)
        # 生成二维码
        qr_code = create_qrcode(act_url, token)
        return {
            'title': title,
            'act_id': act_id,
            'url': act_url,
            'platform': get_domain() + '?code=' + user_id,
            'qr_code': qr_code
        }
    else:
        return {'title': '活动创建失败', 'url': ''}


if __name__ == "__main__":
    temp_file = json.loads(input())
    with open(temp_file['temp_file_path'], "r") as p:
        params = json.load(p)
    # 用完删除
    os.remove(temp_file['temp_file_path'])
    result = create_event(params)
    print(result)
