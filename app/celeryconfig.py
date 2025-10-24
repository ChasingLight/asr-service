from settings import settings

# 队列系统
broker_url = f"redis://:{settings.redis_password}@{settings.redis_host}:{settings.redis_port}/{settings.redis_db_broker}"
# 存储结果
result_backend = f"redis://:{settings.redis_password}@{settings.redis_host}:{settings.redis_port}/{settings.redis_db_result_backend}"

# 存储结果过期时间（单位秒），可参照 https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-expires
result_expires=settings.redis_result_expire_seconds

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "Asia/Shanghai"
enable_utc = True


