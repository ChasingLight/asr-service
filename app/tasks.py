from functools import wraps

import requests
from celery import Celery

from settings import settings

celery_app = Celery("tasks")
celery_app.config_from_object("celeryconfig")


def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} 执行耗时: {elapsed_time:.2f} 秒")
        return result
    return wrapper


@timing_decorator
def __invoke_l20_sensevoice_asr(audio_file_path:str,
                                lang: str = "auto") -> tuple[str, str]:
    """
    调用 l20（云公测） 语音识别接口进行转换
    :param audio_file_path: 录音文件路径（支持网络、本地文件路径）
    :param lang: 语言
    :return: "success","识别结果" 或 "failed","识别失败的原因"
    """
    url = settings.l20_url
    # 请求参数
    data = {
        "local_audio_file_path": audio_file_path,
        "lang": lang
    }
    # 请求数据，设置超时时间-单位秒
    response = requests.post(url, params=data, timeout=10*60)
    # 返回数据
    if response.status_code == 200:
        # 返回解析到的数据
        return "success", response.text
    else:
        return "failed", f"请求l20语音识别接口失败：{response.status_code}---{response.text}"


@timing_decorator
def __invoke_xjtu_sensevoice_asr(audio_file_path:str,
                                 lang: str = "auto")-> tuple[str, str]:
    """
    调用 xjtu（西交大本地）语音识别接口进行转换
    :param audio_file_path: 录音文件路径（支持网络、本地文件路径）
    :param lang: 语言
    :return: "success","识别结果" 或 "failed","识别失败的原因"
    """
    url = settings.xjtu_url
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": settings.xjtu_api_key
    }
    data = {
        "file_paths": [audio_file_path],
        'lang': lang
    }
    # 设置超时时间-单位秒
    response = requests.post(url, headers=headers, json=data, timeout=10 * 60)

    # 解析响应
    if response.status_code == 200:
        return "success", response.text
    else:
        return "failed", f"请求西交大语音识别接口失败：{response.status_code}---{response.text}"


@celery_app.task(bind=True)
def run_asr(self, audio_path: str, lang: str = "auto"):
    """执行语音识别"""
    try:
        strategy = settings.asr_strategy
        if strategy == "l20":
            flag, result = __invoke_l20_sensevoice_asr(audio_path, lang)
        else:
            flag, result  = __invoke_xjtu_sensevoice_asr(audio_path, lang)
        return {"status": flag, "data": result}
    except Exception as e:
        return {"status": "failed", "data": f"代码处理异常:{str(e)}"}