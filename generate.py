from volcenginesdkarkruntime import Ark
import app
import os
import re
from openai import OpenAI


def generate():
    # 获取 text_to_pass 的值
    textget = app.get_audio_transcription()
    if textget is None:
        textget = ''  # 或者其他默认值

    # 设置 Ark 客户端
    client = Ark(api_key=os.environ.get("ARK_API_KEY"))
    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
    )
    input = '请你分析一下这段上课的音频，总结教师的教学风格和语言风格。' + textget +'请严格按照以下格式输出：整体语言风格（10个字及以下）： 。课堂风格分析及建议（200字及以下 ）： 。'
    completion = client.chat.completions.create(
        model="ep-20241207202047-vv45w",
        messages=[
            {"role": "system", "content": "你是一个专业的教授，现在需要来评判不同教师上课的教学风格。"},
            {"role": "user", "content": input},
        ],
    )
    return completion.choices[0].message.content

def outline():
    # 设置 Ark 客户端
    textget = app.fb()
    client = Ark(api_key=os.environ.get("ARK_API_KEY"))
    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
    )
    input = '请你分析一下这段上课的音频文本，总结教师的课程大纲' + textget +'请严格按照以下格式输出，字数在200字左右，不要有序号：课程大纲： 。'
    completion = client.chat.completions.create(
        model="ep-20241207202047-vv45w",
        messages=[
            {"role": "system", "content": "你是一个专业的教授，现在需要来记录不同老师的课程大纲。"},
            {"role": "user", "content": input},
        ],
    )
    return completion.choices[0].message.content

def parse_generated_content(content):
    pattern = r"整体语言风格：\s*(.*?)。\s*课堂风格分析及建议：\s*(.*)"
    match = re.search(pattern, content)
    if match:
        language_style = match.group(1)
        class_style = match.group(2)
        print(language_style)
        return language_style, class_style
    else:
        return None, None

def parse_generated_outline(content):
    pattern = r"课程大纲：\s*(.*)"
    match = re.search(pattern, content)
    if match:
        dagang = match.group(1)
        print(dagang)
        return dagang
    else:
        return None, None


def trans():
    language_style, class_style = parse_generated_content(generate())
    return language_style,class_style

def out():
    outlinefinal = parse_generated_outline(outline())
    return outlinefinal
