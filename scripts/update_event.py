import json
import os
from urllib.parse import quote
import requests

from helper import fix_url_scheme, get_domain, get_user_id, get_user_token
import designh5, raffle

# 创建活动二维码
def create_qrcode(link, token) -> str:
    url = get_domain() + '/api/i/qrcode/create?text=' + quote(link)
    headers = {'Authorization': token}
    res = requests.get(url, headers=headers).json()
    qrcode_url = res.get('qrcode_url') or ''
    return fix_url_scheme(qrcode_url)

def update_event(data):
    # 获取用户id
    user_id = get_user_id()
    user_token = get_user_token(user_id)
    token = user_token.get('token')
    # 获取活动类型
    act_type = data['act_type']
    if act_type == "designh5":
        # 报名
        res = designh5.edit(token, data)
    elif act_type == "raffle":
        # 抽奖
        res = raffle.edit(token, data)
    else:
        # 默认
        res = {"err_code": -1}

    if res['err_code'] == 0:
        title = res.get('title')
        act_url = res.get('url')
        # 生成二维码
        qr_code = create_qrcode(act_url, token)
        return {
            'title': title,
            'url': act_url,
            'platform': get_domain() + '?code=' + user_id,
            'qr_code': qr_code
        }
    else:
        return {'title': '活动修改失败', 'url': ''}


if __name__ == "__main__":
    temp_file = json.loads(input())
    with open(temp_file['temp_file_path'], "r") as p:
        params = json.load(p)
    # 用完删除
    os.remove(temp_file['temp_file_path'])
    result = update_event(params)
    print(result)