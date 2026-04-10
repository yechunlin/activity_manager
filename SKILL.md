---
name: aixiu-activity-skill-openclaw
description: 对话式运营助手
---

# 爱秀活动管理 Skill

## 功能
- 管理"爱秀活动"
- 自动解析用户自然语言中的活动类型，字段
- 多轮对话支持补充活动参数

---

## 触发条件
用户表达意图：
- 创建爱秀活动，编辑爱秀活动，修改爱秀活动
- 创建报名活动，编辑报名活动，修改报名活动
- 发布报名表，编辑/修改报名表

---

## 执行规则（必须严格遵守）
- 必须按照 *_step_1 → *_step_2 → *_step_3 → *_step_4 → ... 顺序执行
- 每一步必须有明确输出结果，禁止跳步
- JSON输出必须合法、完整

---

## 识别流程模式
- 若用户意图为“创建” → 进入创建流程 create_step_1
- 若用户意图为“编辑|修改” → 进入编辑流程 edit_step_1

## 创建工作流程

### create_step_1：初步解析用户描述
- 用户一句话描述活动，例如：
> "我想创建一个爱秀报名活动，收集姓名、手机号、照片"
- LLM提取文字描述，根据以下活动类型JSON，分析判断活动类型，赋值给字段act_type，比如：act_type=designh5
```json
{"designh5":"报名"}
```
- 若类型分析不出，提示用户目前只支持报名活动
- LLM继续分析文字描述生成活动标题：title和活动介绍：brief，其中活动介绍，要求字数在100 - 150字之间，突出主题，语言精炼简洁

---

### create_step_2：生成活动动态参数
- LLM提取分析用户描述的文字，生成初步JSON表单配置fields，若没有，置空
```json
[
    {"label":"姓名","type":"Text","isRequire":true,"placeholder": "请输入姓名"},
    {"label":"照片","type":"MyUpload","isRequire":true,"placeholder": "请上传照片", "fileType": "picture"},
    {"label": "行业","type": "MySelect","isRequire":true,"placeholder": "请选择行业", "options": ["选项1","选项2"]}
]
```
- 当字段类型为上传（MyUpload）时，请根据字段含义推断 fileType：
  - 图片/照片/头像 → picture
  - 视频/录像 → video
  - 音频/录音 → audio
  - 文档/表格/申请表/证明 → doc
- 当字段类型为选择MyRadio | MyCheckbox | MySelect时，注意选项options的格式，若不能推断或提取选项，问："请问有哪些选择项"，等待补充再继续

---

### create_step_3：对create_step_2的结果做询问（必须询问，严格执行）
- 初步生成的JSON字段里fields为空，Skill 问：
> “请告诉我需要收集哪些报名信息（如：姓名、班级、手机号等）”
- 初步生成的JSON字段里fields不为空，Skill 问：
> “请问是否还需要收集其他信息？如果有，请列出”
- 用户补充字段后，合并初步字段 + 新字段，如果还是没有分析出有用字段，默认收集：姓名和手机号

---

### create_step_4：生成海报图（不可跳过）
- 需要为活动生成或获取海报图，并输出标准 JSON 结构。
- Skill询问用户（必须执行）：
> "请问是否有现成的海报图，如果有，请发送海报链接"
- 如果用户回答有，请等待用户发送
  - 获取海报链接，赋值给一下JSON的url
- 如果用户回答没有
  - 精简提取用户的描述，10~50字左右，赋值给赋值给JSON的desc_str，提示用户将由程序生成海报图
- 海报字段post_img的JSON格式如下：
```json
{
    "url": "海报地址[可为空]",
    "size": "海报尺寸，默认:818*1404",
    "desc_str": "提取的描述"
}
```

---

### create_step_5：生成风格配色（深度思考）
- 读取`template/scheme_conf.json`文件，提取内容，列出选项，问用户：
> "请选择其中一种风格，如果都不适合，可以选择由程序根据您的描述自动配色"
- 若用户选择其中一个，记住对应的tag_id，此流程结束，若用户选择程序生成，继续往下走
- 读取`template/designh5.json`模板文件，提取配色字段
- 仔细认真分析用户的描述（活动主题+海报风格），按照格式生成一套适配的配色scheme，格式如下：
```json
{
  "page_config": {
    "bgColor": ""
  },
  "form": {
    "cpBorderColor": "",
    "bgColor": "",
    "titColor": "",
    "btnTextColor": "",
    "btnColor": "",
    "controlBgColor": "",
    "controlBorderColor": "",
    "controlTextColor": "",
    "controlInnerTextColor": "",
    "controlInnerPhColor": ""
  },
  "long_text": {
    "bgColor": "",
    "cpBorderColor": "",
    "color": ""
  }
}
```
---

### create_step_6：确认活动（不可跳过）
- 呈现之前流程生成的数据，询问是否创建活动
  - 若用户的回答里解析出语义为“是”，则创建
  - 若用户的回答里解析出语义为“否”，则中断流程，等待继续或者开启新任务

---

### create_step_7：创建活动
- 将之前流程生成的活动类型、标题、活动介绍和收集字段JSON，以下方JSON形式写入临时文件，并返回临时文件地址：
```json
{
  "act_type": "活动类型",
  "title": "活动标题",
  "brief": "活动描述",
  "post_img": "海报JSON->post_img",
  "scheme": "配色JSON->scheme:{}",
  "fields": "报名的初步JSON->fields",
  "tag_id": "预设风格->tag_id"
}
```
- 调用 `scripts/create_event.py` 创建活动，传入参数{"temp_file_path":f"{临时文件地址}"}
- 创建成功后,读取返回值，将活动标题，活动地址，平台，二维码呈现给用户，如：
  - 活动标题："title"
  - 活动地址：xxxxxxxxxx
  - 平台：xxxxxxxxxxx
  - 活动地址二维码（图片）
- 二维码必须展示给用户看并且提示用户用微信客户端扫码体验
- 创建失败时，直接显示创建失败


## 编辑工作流程

## edit_step_1：获取活动信息（必须）
- 提示用户：
> 请提供需要编辑修改的活动ID或活动链接
- 等待用户输入后，提取输入信息
  - 若输入为链接，从链接中提取活动ID，ID为32位字符串或者18位纯数字，无法提取时，提示用户：
  > "请提供正确的活动链接"
  - 若输入为普通字符，不满足32位字符串或者18位纯数字时，提示用户
  > "去提供正确的活动ID"
- 严格校验ID长度，32字符串或者18位纯数字，不符合的，继续提示："请提供再确认的ID或者链接"
- 正确获得获得ID后，赋值:act_id，调用`scripts/get_activity.py`，调用参数如下：
```json
{"act_id": "32cwc4wdew***********"}
```
- 获取失败时，提示：
> "活动未查询到，请确认好活动ID或链接，再次尝试"
- 获取成功时呈现活动信息：JSON格式，如下，并且要求用户确认是否正确
```json
{
  "act_id": "",
  "act_type": "",
  "title": "",
  "brief": "",
  "post": {},
  "fields": {},
  "scheme": {}
}
```
--- 

## edit_step_2：询问修改内容
- 提示：
> "请问需要修改哪些内容？如：标题、表单字段、海报、配色等"

---

## edit_step_3：解析修改意图（核心）
- 修改意图包含标题：
  - 新标题赋值给title
- 修改意图包含活动介绍(描述)
  - 新介绍(描述)赋值给brief
- 修改意图包含海报时
  - 请复用流程：create_step_4，并将结果赋值给post
- 修改意图包含配色时
  - 请复用流程：create_step_5，并将结果赋值给scheme
- 修改意图包含表单字段时
  - 若有新增，请提取分析新增字段，学习流程：create_step_2，生成字段格式
  - 若有修改，请提取分析字段，修改字段元素
  - 若有删除，请取分析字段，直接删除即可
  - 请注意，整体表单字段的格式要遵循create_step_2的要求，保持一致
- 每一步修改后都必须询问：
> "请问还需要修改其他数据吗"
- 找到判断到用户给出“否定”回到时，才结束本流程，否则一直轮询
- 结束后，将需要修改的信息呈现给用户

--- 

## edit_step_4：确认修改活动（必须）
- 提示：
> "是否确认更新活动？"

---

## edit_step_5: 提交更新
- 将要更新的数据写入临时文件，并返回临时文件地址：
- 调用`scripts/update_event.py`，传入参数{"temp_file_path":f"{临时文件地址}"}
- 修改失败时，直接显示修改失败
- 修改成功时返回：
  - 活动标题：title
  - 活动链接：url
