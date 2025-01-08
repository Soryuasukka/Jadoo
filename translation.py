import requests


def get_audio_file_path():
    audio_file_path = 'assets/video/金沙江小区 6.mp3'  # 替换为实际音频文件路径
    return audio_file_path


def get_audio_transcription():
    url = "https://api.siliconflow.cn/v1/audio/transcriptions"
    audio_file_path = get_audio_file_path()
    model_name = "FunAudioLLM/SenseVoiceSmall"

    # 构建要发送的文件数据和其他表单数据
    files = {
        'file': (audio_file_path, open(audio_file_path, 'rb')),
        'model': (None, model_name)
    }
    headers = {
        "Authorization": "Bearer sk-puyhjrhxfvuxewqvnjpxuhrrzzflbtfcojlvcaruvnqxehyi"
    }

    try:
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()
        text = response.text  # 获取音频转录文本内容赋值给text变量
        print(text)
        return text
    except requests.exceptions.RequestException as e:
        print(f"请求出现错误: {e}")
        return None