import json
import os
import time
import requests
from datetime import datetime
from helper import get_domain, try_openai, rand_control_id, generate, generate_page, random_string
from get_activity import get_act_info

DESIGN_API_URL = get_domain() + "/api/h5hy/api/v0/visible/h5/save"
DESIGN_DEFAULT_POSTER = 'https://xzimg.aihoge.com/cj/images/6441ee5452f2c.png'
STANDARD_TYPES = ["Text", "Textarea", "Number", "Mobile", "IDCard", "MyRadio", "MyCheckbox", "MySelect", "Date",
                  "MyUpload"]

FIELD_TYPE_MAP = {
    "姓名": "Text",
    "名字": "Text",
    "手机": "Mobile",
    "手机号": "Mobile",
    "电话": "Mobile",
    "身份证": "IDCard",
    "年级": "Text",
    "班级": "Text",
    "学校": "Text",
    "地址": "Textarea",
    "居住地": "Textarea",
    "公司": "Text",
    "职位": "Text",
    "薪资": "Number",
    "照片": "MyUpload",
    "文件": "MyUpload",
    "作品": "MyUpload",
}

OPTION_DEFAULTS = [
    {"label": "选项1", "value": "1"},
    {"label": "选项2", "value": "2"},
]

UPLOAD_TYPE_MAP = {
    "照片": "picture",
    "图片": "picture",
    "头像": "picture",

    "视频": "video",
    "录像": "video",

    "音频": "audio",
    "录音": "audio",

    "申请表": "doc",
    "文件": "doc",
    "证明": "doc",
    "材料": "doc",
    "作品": "doc",
}
TEMPLATE_ID = 8229
MARK = 'designh5@form'


# 生成海报
def generate_poster(title, post) -> str:
    des_str = post.get('desc_str') or title
    size = post.get('size') or "818*1404"
    # OpenAI
    poster = try_openai(des_str, size)
    if poster:
        print("海报生成完成")
        return poster

    # 默认兜底
    return DESIGN_DEFAULT_POSTER

# 校准模板表单控件
def standardize_field(field):
    cid = field.get("cid", '')
    if cid:
        return field

    name = field.get("label", "").strip()
    field_type = field.get("type", "Text")
    required = field.get("isRequire", True)
    placeholder = field.get("placeholder", "")

    if field_type not in STANDARD_TYPES:
        field_type = FIELD_TYPE_MAP.get(name, "Text")

    control = {"type": field_type, "label": name, "id": rand_control_id(), "placeholder": placeholder,
               "isRequire": required}

    if field_type in {"MyRadio", "MyCheckbox", "MySelect"}:
        t_options = field.get('options', [])
        if not t_options:
            control["options"] = OPTION_DEFAULTS
        else:
            control["options"] = [{"label": item, "value": str(index + 1)} for index, item in enumerate(t_options)]

    if field_type == "MyUpload":
        file_type = field.get("fileType")
        # ① 优先用 LLM 给的
        if file_type not in {"picture", "video", "audio", "doc"}:
            # ② 用 label 推断
            file_type = UPLOAD_TYPE_MAP.get(name, "picture")

        control["fileType"] = file_type
        control["limit"] = 1
        control["limitSize"] = 10

    if field_type == "Date":
        control["dateType"] = "date"

    return control

# 校准表单格式
def parse_fields(llm_json):
    final_fields = []
    seen = set()
    for field in llm_json.get("fields", []):
        std_field = standardize_field(field)
        if std_field["label"] not in seen:
            final_fields.append(std_field)
            seen.add(std_field["label"])
    return final_fields

def get_default_scheme(tag_id):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, "..", "template", "scheme.json")
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data[tag_id] or {}

# 创建活动
def run(token, data)->dict:
    title = data["title"]
    brief = data['brief']
    fields = data["fields"]
    post = data['post'].get('post_img', [])
    scheme = data['scheme']
    tag_id = data['tag_id']
    # 判断是否去默认风格
    if tag_id:
        sc = get_default_scheme(tag_id)
        post['url'] = sc['post_url']
        scheme = sc['scheme']

    # 开始生成活动参数
    now = int(time.time())
    start_at = now
    end_at = start_at + (86400 * 7)
    # 默认模板id与模板标识
    template_id = TEMPLATE_ID
    mark = MARK
    # 模板表单id
    form_control_tpl_id = ''
    # 海报图
    poster_url = post.get('url') or generate_poster(title, post)
    # 获取模板数据
    payload = generate(mark, template_id, token)
    # 校准formControls
    fields = parse_fields(fields)
    # 修改模板表单控件
    for item in payload['data']:
        if item['path'] == 'index':
            item['data']['pageConfig']['bgColor'] = scheme['page_config']['bgColor']
            for tpl_item in item['data']['tpl']:
                if tpl_item['item']['type'] == 'Image' and tpl_item['item']['config']['cpName'] == 'Image':
                    tpl_item['item']['config']['imgUrl'][0]['url'] = poster_url

                if tpl_item['item']['type'] == 'Form':
                    form_control_tpl_id = tpl_item['id']
                    tpl_item['item']['config']['formControls'] = fields
                    tpl_item['item']['config']['bgColor'] = scheme['form']['bgColor']
                    tpl_item['item']['config']['btnColor'] = scheme['form']['btnColor']
                    tpl_item['item']['config']['btnTextColor'] = scheme['form']['btnTextColor']
                    tpl_item['item']['config']['controlBgColor'] = scheme['form']['controlBgColor']
                    tpl_item['item']['config']['controlBorderColor'] = scheme['form']['controlBorderColor']
                    tpl_item['item']['config']['controlInnerPhColor'] = scheme['form']['controlInnerPhColor']
                    tpl_item['item']['config']['controlInnerTextColor'] = scheme['form']['controlInnerTextColor']
                    tpl_item['item']['config']['controlTextColor'] = scheme['form']['controlTextColor']
                    tpl_item['item']['config']['cpBorderColor'] = scheme['form']['cpBorderColor']
                    tpl_item['item']['config']['titColor'] = scheme['form']['titColor']


                if brief and tpl_item['item']['type'] == 'LongText':
                    tpl_item['item']['config']['text'] = brief
                    tpl_item['item']['config']['bgColor'] = scheme['long_text']['bgColor']
                    tpl_item['item']['config']['cpBorderColor'] = scheme['long_text']['cpBorderColor']
                    tpl_item['item']['config']['color'] = scheme['long_text']['color']

    # 赋值活动数据
    forward = {
        "data": {
            "type": "designh5",
            "mark": mark,
            "indexpic": poster_url,
            "title": title,
            "introduce": brief,
            "date": [
                datetime.fromtimestamp(start_at).strftime("%Y-%m-%d %H:%M:%S"),
                datetime.fromtimestamp(end_at).strftime("%Y-%m-%d %H:%M:%S")
            ],
            "limit": {
                "global_style": {
                    "open_global_style": 0,
                    "page_bg_color": "rgba(198,242,189,1)",
                    "index_bg_img": {
                        "indexpic": [],
                        "mode": 1
                    },
                    "dialog_bg_color": [
                        "rgba(198,242,189,1)",
                        "rgba(239,251,196,1)"
                    ]
                },
                "lottery_config": {
                    "open": 0,
                    "activity_id": "",
                    "mode": 1,
                    "times": 1,
                    "give_times": 1,
                    "share": {
                        "open": 0,
                        "mode": 1,
                        "type": 1
                    }
                },
                "wechat_collect_info": 0,
                "source_limit": {
                    "source_limit": "wechat",
                    "default_download_app": "",
                    "app_download_link": "",
                    "user_app_source": [
                        {
                            "name": "微信",
                            "sign": "wechat"
                        }
                    ],
                    "app_id": ""
                },
                "hide_records": 0,
                "show_statistic": 0,
                "form": {
                    "num_limit": -1,
                    "max_limit": -1,
                    "open_submit_limit": 0,
                    "submit_limit": {
                        "user_daily_max": 1,
                        "user_max": 1
                    },
                    "portrait_collect": 0
                },
                "score": {
                    "is_open": 0,
                    "min_score": 1,
                    "max_score": 100
                },
                "check": {
                    "is_open": 0,
                    "repeat_for_pass": 1
                },
                "allow_members": {
                    "is_open": 0,
                    "tags": []
                },
                "templateId": template_id
            },
            "share_settings": {
                "wxShareStart": 1,
                "share_title": "活动上线啦",
                "share_url": "",
                "share_brief": "赶紧扫码来体验吧~",
                "share_indexpic": [
                    "//xzimg.aihoge.com/xiuzan/1634205427542/ercode.png"
                ],
                "list_indexpic": [
                    "https://xzimg.aihoge.com/xiuzan/1682042096535/1.png"
                ]
            },
            "start_time": start_at,
            "end_time": end_at,
            "form_controls": [
                {
                    'id': form_control_tpl_id,
                    'controls': fields
                }
            ]
        },
        "service": "designh5@form"
    }

    payload['forward'] = forward
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    resp = requests.post(DESIGN_API_URL, json=payload, headers=headers)
    resp = resp.json()
    if resp['state'] == 200 and resp['result']['forward_id']:
        act_id = resp['result']['forward_id']
        act_url = f"https://m.aihoge.com/h5?mark=designh5@form&tid={act_id}&path=index"
        return {
            'err_code': 0,
            'activity_id': act_id,
            'title': title,
            'url': act_url
        }
    return {'err_code': -1}


# 修改活动
def edit(token, data)->dict:
    act_id = data["act_id"]
    title = data["title"]
    brief = data['brief']
    fields = data["fields"]
    post = data['post'].get('post_img', [])
    scheme = data['scheme']
    # 查询活动信息
    act_data = get_act_info(act_id, token)
    # 保留活动开始和结束时间，可覆盖
    start_at = act_data['response']['activity']['start_time']
    end_at = act_data['response']['activity']['end_time']
    # 默认模板id与模板标识
    template_id = TEMPLATE_ID
    mark = MARK
    # 海报图
    poster_url = post.get('url') or generate_poster(title, post)
    # 推送页面表单设置
    form_item_id = random_string(6)

    # 获取模板数据
    payload = generate_page(act_id, token)
    # 校准formControls
    form_controls = act_data['response']['rules']['form_controls']
    fields = parse_fields(fields)
    form_controls[0]['id'] = form_item_id
    form_controls[0]['controls'] = fields
    # 修改模板表单控件
    for item in payload['data']:
        if item['path'] == 'index':
            item['data']['pageConfig']['bgColor'] = scheme['page_config']['bg']
            for tpl_item in item['data']['tpl']:
                if tpl_item['item']['type'] == 'Image' and tpl_item['item']['config']['cpName'] == 'ShowImage':
                    tpl_item['item']['config']['imgUrl'][0]['url'] = poster_url

                if tpl_item['item']['type'] == 'Form':
                    tpl_item['item']['config']['formControls'] = fields
                    tpl_item['item']['config']['bgColor'] = scheme['form']['bg']
                    tpl_item['item']['config']['btnColor'] = scheme['form']['btn']
                    tpl_item['item']['config']['btnTextColor'] = scheme['form']['btntext']
                    tpl_item['item']['config']['controlBgColor'] = scheme['form']['ctbg']
                    tpl_item['item']['config']['controlBorderColor'] = scheme['form']['ctborder']
                    tpl_item['item']['config']['controlInnerPhColor'] = scheme['form']['ctph']
                    tpl_item['item']['config']['controlInnerTextColor'] = scheme['form']['cttext']
                    tpl_item['item']['config']['controlTextColor'] = scheme['form']['ctlabel']
                    tpl_item['item']['config']['cpBorderColor'] = scheme['form']['border']
                    tpl_item['item']['config']['titColor'] = scheme['form']['ctph']


                if brief and tpl_item['item']['type'] == 'RichText':
                    tpl_item['item']['config']['content'] = "<p class=\"p1\"><span style=\"font-size:14px\"><span style=\"line-height:1.75\"><span style=\"color:#cccccc\">"+brief+"</span></span></span></p>"
                    tpl_item['item']['config']['bgColor'] = scheme['rich_text']['bg']
                    tpl_item['item']['config']['cpBorderColor'] = scheme['rich_text']['border']

    # 赋值活动数据
    forward = {
        "data": {
            "activity_id": act_id,
            "type": "designh5",
            "mark": mark,
            "indexpic": poster_url,
            "title": title,
            "introduce": brief,
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

    payload['forward'] = forward
    payload['tid'] = act_id
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    resp = requests.post(DESIGN_API_URL, json=payload, headers=headers)
    resp = resp.json()
    if resp['state'] == 200 and resp['result']['forward_id']:
        act_id = resp['result']['forward_id']
        act_url = f"https://m.aihoge.com/h5?mark=designh5@form&tid={act_id}&path=index"
        return {
            'err_code': 0,
            'activity_id': act_id,
            'title': title,
            'url': act_url
        }
    return {'err_code': -1}
