import random
import string
import os
import uuid

import requests
import time

DOMAIN = "https://openclaw.aihoge.com"

def fix_url_scheme(url: str, default_scheme: str = "https") -> str:
    if not url:
        return url

    url_stripped = url.strip()
    low_url = url_stripped.lower()

    if low_url.startswith(("http://", "https://")):
        return url_stripped

    return f"{default_scheme}://{url_stripped.lstrip('/')}"


def rand_control_id() -> str:
    letters = "".join(random.choice(string.ascii_lowercase) for _ in range(6))
    digits = "".join(random.choice(string.digits) for _ in range(4))
    return letters + digits


def random_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def get_domain() -> str :
    return DOMAIN

def try_openai(title, size):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return ''

    # 创建图
    try:
        # 建立任务
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
        headers = {
            "X-DashScope-Async": "enable",
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "wan2.2-t2i-flash",
            "input": {
                "prompt": f"{title}"
            },
            "parameters": {
                "n": 1,
                "size": size
            }
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=8)
        data = resp.json()
        output = data.get('output', {})
        task_id = output.get('task_id', '')
        if not task_id:
            return ''
        else:
            # 开启轮询，查询任务结果;每5秒尝试一次，最多10次
            time.sleep(1)
            times_num = 10
            while times_num > 0:
                url = "https://dashscope.aliyuncs.com/api/v1/tasks/" + task_id
                headers = {
                    "Authorization": f"Bearer {api_key}"
                }
                resp = requests.get(url, headers=headers)
                data = resp.json()
                output = data.get('output', {})
                print("海报生成状态：" + output.get('task_status'))
                post_url_result = output.get('results', [])
                if len(post_url_result) > 0:
                    post_url = post_url_result[0].get('url', '')
                    if post_url:
                        return post_url

                times_num -= 1
                time.sleep(5)

            return ''
    except Exception as e:
        print("海报未生成")

    return ''

# 获取模板数据
def generate(mark, template_id, token):
    tid = ''
    template_data = []
    url = get_domain() + '/api/h5hy/api/v0/visible/preview/generate?mark=' + mark + '&template_id=' + str(
        template_id)
    headers = {'Authorization': token}
    res = requests.get(url, headers=headers)
    res = res.json()
    if res['state'] == 200:
        tid = res['result']['success']['id'] or ''
        template_data = res['result']['success']['data'] or []

    return {'tid': tid, 'data': template_data}

# 获取活动页面数据
def generate_page(tid, token):
    template_data = []
    url = get_domain() + '/api/h5hy/api/v0/visible/preview?tid=' + tid
    headers = {'Authorization': token}
    res = requests.get(url, headers=headers)
    res = res.json()
    if res['state'] == 200:
        template_data = res['result']['data'] or []

    return {'data': template_data}

# uuid . 4 . hex
def get_uuid_4_hex() -> str:
    return uuid.uuid4().hex

# 获取本地用户id
def get_user_id():
    user_id_file = os.path.expanduser("~/.aixiu_user_id")
    if os.path.exists(user_id_file):
        with open(user_id_file, "r") as f:
            user_id = f.read().strip()
    else:
        user_id = str(uuid.uuid4())
        with open(user_id_file, "w") as f:
            f.write(user_id)
    return user_id

# 获取token
def get_user_token(user_id):
    try:
        url = get_domain() + '/api/i/user/claw?uuid=' + user_id
        res = requests.get(url).json()
        return {
            'token': res['response']['xiuzan_token'] or ''
        }
    except Exception as e:
        return {'token': ''}
