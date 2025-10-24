from fastapi import FastAPI
from tasks import run_asr

app = FastAPI()

@app.post("/api/v1/asr")
def submit_asr_task(audio_path: str, lang: str = "auto"):
    """提交识别任务"""
    task = run_asr.delay(audio_path, lang)
    return {"task_id": task.id, "status": "submitted"}

@app.get("/api/v1/asr/result/{task_id}")
def get_asr_result(task_id: str):
    """查询识别结果"""
    result = run_asr.AsyncResult(task_id)
    if result.ready():
        return result.result
    else:
        return {"status": "pending"}
