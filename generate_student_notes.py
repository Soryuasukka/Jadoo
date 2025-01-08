import requests
import json


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=GnArphNvN1w7vv2gQmR1Zzbn&client_secret=Y4cKfqiLqQyufWnZBta8Hj3AipkyMgux"
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def generate_student_notes(text):
    if text is None or not isinstance(text, str):
        print("传入的text变量无效，请检查其获取逻辑。")
        raise ValueError("无效的文本输入")

    access_token = get_access_token()
    note_generation_url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/qianfan-agent-speed-8k?access_token={access_token}"
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "请根据以下提供的课堂文本内容生成学生笔记，笔记要求输出三个方面，首先是要点，以关键词、简短标题等形式，第二个是笔记，记录重点内容，借助符号、缩写等形式，言简意赅。第三个是总结，写下感受、思考和体会。呈现课堂文本内容如下：" + text
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", note_generation_url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        if 'result' in data:
            student_notes = data['result']
            # 先按照换行符进行初步分割，因为每个部分之间大概率是换行隔开的
            parts_by_line = student_notes.splitlines()
            points = ""
            note = ""
            summary = ""
            flag_points = False
            flag_note = False
            flag_summary = False
            for line in parts_by_line:
                if "要点" in line:
                    flag_points = True
                    continue
                elif "笔记" in line:
                    flag_note = True
                    flag_points = False
                    continue
                elif "总结" in line:
                    flag_summary = True
                    flag_note = False
                    continue
                if flag_points:
                    points += line + "\n"
                elif flag_note:
                    note += line + "\n"
                elif flag_summary:
                    summary += line + "\n"
            # 去除末尾多余的换行符
            points = points.rstrip()
            note = note.rstrip()
            summary = summary.rstrip()
            return points, note, summary
        else:
            print("接口返回数据格式不符合预期，无法提取学生笔记内容。")
            return "", "", ""
    except requests.RequestException as e:
        if isinstance(e, requests.ConnectionError):
            print("网络连接出现问题，请检查网络设置。")
        elif isinstance(e, requests.Timeout):
            print("请求超时，请稍后再试或检查网络稳定性。")
        elif isinstance(e, requests.HTTPError):
            print(f"HTTP请求返回错误状态码，详细信息: {e.response.text}")
        else:
            print(f"其他请求相关错误: {e}")
        return "", "", ""


def generate_graph_student_notes(text):
    """
    根据输入文本生成适合用于知识图谱的学生笔记格式，包含学科、实体、关系等信息
    """
    if text is None or not isinstance(text, str):
        print("传入的text变量无效，请检查其获取逻辑。")
        raise ValueError("无效的文本输入")

    access_token = get_access_token()
    graph_note_generation_url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/qianfan-agent-speed-8k?access_token={access_token}"
    # 这里提示语调整为要求大模型按照期望格式生成笔记，示例中以语文举例，可根据实际传入学科信息调整
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "请根据以下提供的课堂文本内容生成适合用于知识图谱的学生笔记，格式要求如下：\n"
                           "{\n"
                           "    \"subject\": \"语文\",\n"
                           "    \"entities\": [具体的实体内容，多个实体用逗号隔开],\n"
                           "    \"relations\": [[实体1, 关系描述, 实体2], [实体3, 关系描述, 实体4]]\n"
                           "}\n"
                           "呈现课堂文本内容如下：" + text
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", graph_note_generation_url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        if 'result' in data:
            graph_student_notes = data['result']
            print(graph_student_notes)
            print(type(graph_student_notes))
            return graph_student_notes
        else:
            print("接口返回数据格式不符合预期，无法提取用于知识图谱的学生笔记内容。")
            return {}
    except requests.RequestException as e:
        if isinstance(e, requests.ConnectionError):
            print("网络连接出现问题，请检查网络设置。")
        elif isinstance(e, requests.Timeout):
            print("请求超时，请稍后再试或检查网络稳定性。")
        elif isinstance(e, requests.HTTPError):
            print(f"HTTP请求返回错误状态码，详细信息: {e.response.text}")
        else:
            print(f"其他请求相关错误: {e}")
        return {}
