import json

from helper import get_user_id, get_user_token, generate


# 获取模板预览
def get_preview(mark, template_id) -> dict:
    if (not mark) or (not template_id):
        return {"preview_url":""}

    # 获取用户id
    user_id = get_user_id()
    user_token = get_user_token(user_id)
    token = user_token.get('token')
    payload = generate(mark, template_id, token)
    if not payload['tid']:
        return {"preview_url":""}

    return {
        "preview_url": f"https://m.aihoge.com/h5?mark={mark}&tid={payload['tid']}&path=index&isPcShow=true&isPreview=true"
    }


if __name__ == "__main__":
    act = json.loads(input())
    result = get_preview(act['mark'], act['template_id'])
    print(result)
