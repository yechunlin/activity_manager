import time
import requests
from datetime import datetime
from helper import get_domain, get_uuid_4_hex, generate

RAFFLE_API_URL = get_domain() + '/api/h5hy/api/v0/visible/h5/save'
RAFFLE_DEFAULT_POSTER = 'https://xzimg.aihoge.com/xiuzan/2024/03/b8fba610d15761051d2679518dad0858.png'

def run(token, data)->dict:
    title = data["title"]
    brief = data['brief']
    prizes = data["prizes"]
    # 开始生成活动参数
    now = int(time.time())
    start_at = now
    end_at = start_at + (86400 * 7)
    # 默认模板id与模板标识
    template_id = 8168
    mark = 'raffle@designh5'
    # 获取模板数据
    payload = generate(mark, template_id, token)
    # 赋值活动数据
    forward = {
        "service": "raffle@designh5",
        "data": {
            "template_id": template_id,
            "type": 1,
            "mark": mark,
            "themeMark": {
                "sign": "egg-default",
                "theme_url": "https://xzimg.aihoge.com/cj/images/61b706ae8b64c.png",
                "mark": "raffle@designh5",
                "title": "自定义抽奖",
                "indexpic": "http://xzimg.aihoge.com/xiuzan/1678957096701/index.jpg"
            },
            "indexpic": RAFFLE_DEFAULT_POSTER,
            "title": title,
            "is_display_title": 1,
            "date": [
                datetime.fromtimestamp(start_at).strftime("%Y-%m-%d %H:%M:%S"),
                datetime.fromtimestamp(end_at).strftime("%Y-%m-%d %H:%M:%S")
            ],
            "introduce": "<p>"+brief+"</p>",
            "is_open_list": 1,
            "is_activity_end": "本次活动已结束，敬请关注后续活动",
            "page_setup": {
                "background": {
                    "indexpic": [
                        "https://xzimg.aihoge.com/xiuzan/1634262445666/bg.png"
                    ],
                    "mode": 1
                },
                "background_color": "#ea0c20",
                "rankpic": [
                    "https://xiuzan-h5.oss-cn-beijing.aliyuncs.com/media/6ihn4tb04f1490604551000"
                ],
                "font_color": "1",
                "activity_rule": "2",
                "activity_rule_title": "活动规则"
            },
            "store": [],
            "limit": {
                "global_style": {
                    "open_global_style": 0,
                    "open_dialog_style": 0,
                    "page_bg_color": "rgba(252,202,185,1)",
                    "index_bg_img": {
                        "indexpic": [
                            "http://xzimg.aihoge.com/xiuzan/2024/03/1b423dd3fd329b4c8f888f3a0da3bc24.png"
                        ],
                        "mode": 1
                    },
                    "dialog_bg_color": [
                        "rgba(255,255,255,1)",
                        "rgba(255,255,255,1)"
                    ],
                    "dialog_border_color": "rgba(106,34,255,0.5)",
                    "dialog_border_width": 0,
                    "prize_text_color": "rgba(203,38,34,1)",
                    "prize_bg_color_A": "rgba(255,236,232,1)",
                    "prize_bg_color_B": "rgba(255,251,246,1)",
                    "raffle_btn_text_color": "rgba(255,255,255,1)",
                    "plate_bg_img": {
                        "indexpic": [
                            "http://xzimg.aihoge.com/xiuzan/2024/03/5cff5d3a252c171f91799780305396eb.png"
                        ]
                    },
                    "raffle_btn_bg_img": {
                        "indexpic": [
                            "http://xzimg.aihoge.com/xiuzan/2024/03/4a54b4fae552df6381019ba1f56b56fb.png"
                        ]
                    },
                    "record_bg_img": {
                        "indexpic": [
                            "http://xzimg.aihoge.com/xiuzan/2024/03/117403c38a8117b3b1b2daf1621a2786.png"
                        ],
                        "mode": 1
                    }
                },
                "open_daily_enable_time": 0,
                "daily_enable_time": [
                    "09:00:00",
                    "18:00:00"
                ],
                "show_result_list": 1,
                "join_raffle_num": 1,
                "source_limit": {
                    "is_source_limit": 1,
                    "source_limit": "wechat",
                    "default_download_app": "",
                    "is_send": "",
                    "send_type": "",
                    "is_scope_limit": "",
                    "scope_limit": "",
                    "share_link": "",
                    "_scope_limit": "",
                    "_share_link": "",
                    "user_app_source": [
                        {
                            "icon": "http://xzimg.aihoge.com/xiuzan/1657336330264/wechat.jpeg?x-oss-process=image/resize,w_228",
                            "name": "微信",
                            "sign": "wechat"
                        }
                    ]
                },
                "app_download_prompt": {
                    "app_type_radio": 1,
                    "app_download_text": "打开App 查看更多精彩",
                    "app_download_radio": 1
                },
                "time_down_isOpen": 0,
                "link_prize_content": 0,
                "card_limit": {
                    "is_lottery_row": 1,
                    "is_lottery_unit": 1,
                    "is_lottery_times": 3,
                    "is_winning_unit": 1,
                    "is_winning_times": 1
                },
                "is_virtual_phone_limit": 0,
                "is_open_prize_rule": 0,
                "internal_setting": 0,
                "is_open_interact": {
                    "status": 0,
                    "interact_activity": []
                },
                "collection_form": {
                    "is_collection_timeCount": 1,
                    "portrait_collect": 0,
                    "is_collection_row": 0,
                    "is_open_collect": 2,
                    "collect_type": 1,
                    "user_info_settings": [
                        {
                            "name": "姓名",
                            "placeholder": "姓名",
                            "unique_name": "name",
                            "isRequire": True,
                            "value": "姓名"
                        },
                        {
                            "name": "手机号",
                            "placeholder": "手机号",
                            "unique_name": "mobile",
                            "isRequire": True,
                            "value": "手机号"
                        }
                    ],
                    "address_info_setting": [
                        {
                            "name": "姓名",
                            "placeholder": "姓名",
                            "unique_name": "name",
                            "values": "姓名",
                            "isRequire": True
                        },
                        {
                            "name": "手机号",
                            "placeholder": " 手机号",
                            "unique_name": "mobile",
                            "values": "手机号",
                            "isRequire": True
                        },
                        {
                            "name": "详细地址",
                            "placeholder": " 详细地址",
                            "unique_name": "address",
                            "values": "详细地址",
                            "isRequire": True
                        }
                    ]
                },
                "is_collection_tips": "请填写以下信息，中奖后奖品才能送到您手中",
                "lottery_limit": {
                    "is_lottery_row": 1,
                    "is_lottery_unit": 1,
                    "is_lottery_times": 1,
                    "is_winning_unit": 1,
                    "is_winning_times": 1,
                    "get_open": 0,
                    "single_card_max": 1
                },
                "is_min_point_limit": 0,
                "min_point_limit": 0,
                "integral_limit": {
                    "give_integral_open": 0,
                    "give_integral_unit": 1,
                    "give_integral_num": 10,
                    "is_integral_row": 0,
                    "is_lottery_integral": 10,
                    "is_exchanges": 1,
                    "is_winning_unit": 1,
                    "is_winning_times": 1
                },
                "led_securities": 0,
                "lottery_status_limit": [
                    {
                        "label": "奖品已抽完状态",
                        "key": "no_pirce_number",
                        "value": [
                            "来晚了",
                            "奖品已发完，下次记得早点来！"
                        ],
                        "limit": 20
                    },
                    {
                        "label": "未抽中状态",
                        "key": "no_lottery",
                        "value": [
                            "未抽中",
                            "很遗憾，没有抽中哦！"
                        ],
                        "limit": 20
                    },
                    {
                        "label": "活动暂停状态",
                        "key": "activity_pause",
                        "value": [
                            "操作提示",
                            "活动已暂停，请稍后再来哦！"
                        ],
                        "limit": 20
                    },
                    {
                        "label": "活动未开始",
                        "key": "activity_no_start",
                        "value": "活动未开始，请稍后再来",
                        "limit": 20
                    },
                    {
                        "label": "活动已结束",
                        "key": "activity_end",
                        "value": "本次活动已结束，敬请关注后续活动",
                        "limit": 20
                    },
                    {
                        "label": "虚拟号段",
                        "key": "virtual_phone_limit",
                        "value": "请使用真实的手机号注册信息 参与活动",
                        "limit": 20
                    },
                    {
                        "label": "不满足积分抽奖条件的状态",
                        "key": "no_min_point_limit",
                        "value": [
                            "操作提示",
                            "本次活动App积分≥0才能参与抽奖"
                        ],
                        "limit": 20
                    },
                    {
                        "label": "抽奖次数提示文案：当活动开启了积分抽奖且活动抽奖次数等于0",
                        "key": "integral_lottery_number",
                        "value": "请使用积分抽奖",
                        "limit": 12
                    },
                    {
                        "label": "积分弹窗状态：当活动开启了积分抽奖且活动抽奖次数等于0",
                        "key": "integral_dialog",
                        "value": "确认使用积分兑换抽奖机会吗？",
                        "limit": 50
                    },
                    {
                        "label": "积分弹窗状态：用户当天消耗积分兑换抽奖的次数已用完",
                        "key": "integral_dialog_unnumber",
                        "value": "今日积分抽奖次数已用完，无法参与抽奖，下次再来吧",
                        "limit": 50
                    },
                    {
                        "label": "积分弹窗状态：用户默认的抽奖机会已用完，可使用积分抽奖",
                        "key": "integral_dialog_integral",
                        "value": "你今日的抽奖机会已用完，可以使用积分继续抽奖喔~",
                        "limit": 50
                    },
                    {
                        "label": "积分弹窗状态：账户积分余额不足，无法参与抽奖",
                        "key": "integral_dialog_unintegral",
                        "value": "账户积分余额不足，无法参与抽奖，下次再来吧",
                        "limit": 50
                    }
                ],
                "pwd_lottery_limit": {
                    "is_pwd_lottery": 0
                },
                "is_pwd": "恭喜发财",
                "is_pwdTips": "请前往爱秀公众号获取口令",
                "share_lottery_limit": {
                    "is_share_lottery": 0,
                    "is_share_unit": 1,
                    "is_share_times": 1
                },
                "is_share_before": "疯狂派“兑”，邀请好友一起来参与吧！",
                "is_share_after": "分享成功，赠送你一次抽奖机会",
                "card_level": {
                    "levels": [],
                    "maxMount": 50
                },
                "card_list": [
                    {
                        "is_award_count_add": 0,
                        "is_award_count_less": 0,
                        "is_send_number": 0,
                        "is_winning_limit": 0,
                        "is_lottery_fields": 0,
                        "is_award_on": 1,
                        "is_award_on_show": True,
                        "is_award_del": True,
                        "is_send_number_show": True,
                        "is_winning_limit_show": True,
                        "is_lottery_fields_show": True,
                        "is_unEdit": False,
                        "choose_award": {},
                        "type": 8,
                        "images": [
                            "https://xzimg.aihoge.com/cj/images/61dc22fb5c259.png"
                        ],
                        "prize_id": "",
                        "uuid": "a5feaecddc22d66eb33e4a30c32b41ff",
                        "is_award_name": "",
                        "card_level_uuid": "",
                        "is_award_count": 0,
                        "is_award_dof": 0,
                        "is_award_content": ""
                    }
                ],
                "api_limit": {
                    "sync_draw_member": 0,
                    "trigger_draw": 0,
                    "trigger_type": 0
                },
                "awardTabel": [
                    {
                        "is_award_name": "再来一次",
                        "card_level_uuid": "",
                        "is_award_content": "获得再来一次的抽奖机会",
                        "is_award_count": 1,
                        "is_award_count_add": 0,
                        "is_award_count_less": 0,
                        "is_award_dof": "10",
                        "is_send_number": 0,
                        "is_winning_limit": 0,
                        "is_lottery_fields": 0,
                        "is_award_on": 1,
                        "is_award_on_show": True,
                        "is_award_del": True,
                        "is_send_number_show": True,
                        "is_winning_limit_show": True,
                        "is_lottery_fields_show": True,
                        "is_unEdit": False,
                        "choose_award": {},
                        "type": 6,
                        "images": "",
                        "prize_id": "",
                        "uuid": "c806586517dad7aab492a98bd2a48459",
                        "draw_order": 1
                    },
                    {
                        "is_award_name": "谢谢参与",
                        "card_level_uuid": "",
                        "is_award_content": "很遗憾您没有中奖，感谢参与",
                        "is_send_number_show": False,
                        "is_winning_limit_show": False,
                        "is_lottery_fields_show": False,
                        "is_award_on": 1,
                        "is_award_on_show": False,
                        "is_award_del": False,
                        "is_unEdit": True,
                        "choose_award": {},
                        "prize_id": "",
                        "uuid": "3834732ed6b9fefd095e14b7d35e90e5",
                        "draw_order": 2
                    }
                ],
                "choose_award": {
                    "is_prize_type": 0,
                    "is_packet_cate": 1,
                    "is_packet_type": 1,
                    "is_packet_min": "",
                    "is_packet_max": "",
                    "is_packet_prefixed": "",
                    "is_packet_amountList": [
                        None,
                        None
                    ],
                    "is_prize_name": "",
                    "is_prize_tips": "",
                    "is_prize_desc": "",
                    "is_prize_date": [],
                    "is_prize_img": [],
                    "is_merchants": {
                        "name": "",
                        "id": None,
                        "logo_url": ""
                    },
                    "is_blessing": "",
                    "is_give_aways": 0,
                    "is_select_merchant": {
                        "id": None,
                        "name": "",
                        "address": "",
                        "leader": "",
                        "start_time": "",
                        "end_time": ""
                    },
                    "is_give_times_type": 1,
                    "is_give_date": "",
                    "is_give_datetimerange": [],
                    "is_give_times": 15,
                    "is_give_tips": "",
                    "is_qr_code": [],
                    "is_expiry_type": 0,
                    "is_expiry": "",
                    "is_expiry_address": "http://",
                    "is_upload_file": "",
                    "outlink": ""
                },
                "share_settings": {
                    "wxShareStart": 1,
                    "share_title": "分享抽奖赢好礼",
                    "share_url": "",
                    "share_brief": "快去分享吧",
                    "share_indexpic": [
                        "//xzimg.aihoge.com/xiuzan/1634205427542/ercode.png"
                    ],
                    "list_indexpic": [
                        "http://xzimg.aihoge.com/xiuzan/2024/03/b8fba610d15761051d2679518dad0858.png"
                    ]
                },
                "unlock_pic": {
                    "is_unlock_pic": 1,
                    "unlock_indexpic": [
                        "//xzimg.aihoge.com/xiuzan/1599470131011/二维码2.png"
                    ]
                },
                "wallpapers_config": {
                    "is_open": 1,
                    "img_url": [
                        "//xzimg.aihoge.com/xiuzan/1599470131011/二维码2.png"
                    ]
                },
                "card_collect_complete": {
                    "give_raffle_open": 0,
                    "give_raffle_activity_id": "",
                    "give_raffle_count": 1
                },
                "card_level_config": [
                    {
                        "uuid": "5c1b35cc64bb842d76d0bb54c765af6b",
                        "title": "等级1"
                    }
                ],
                "portraithy_setting": {},
                "templateId": template_id
            }
        }
    }

    payload['forward'] = forward
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    resp = requests.post(RAFFLE_API_URL, json=payload, headers=headers)
    resp = resp.json()
    if resp['state'] == 200 and resp['result']['forward_id']:
        act_id = resp['result']['forward_id']
        act_url = f"https://m.aihoge.com/h5?mark=raffle@designh5&tid={act_id}&path=index"
        return {
            'err_code': 0,
            'activity_id': act_id,
            'title': title,
            'url': act_url
        }
    return {'err_code': -1}


def edit(token, data)->dict:
    return {}
