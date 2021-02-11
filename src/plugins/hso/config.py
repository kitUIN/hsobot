from pydantic import BaseSettings


# -----------
# 配置
# -----------
class Config(BaseSettings):
    # 全局
    superusers: list = [0]  # 超级管理员
    api1 = True  # setu库开启状况 api1=lolicon
    priority: tuple = 1  # 优先级(1,2,3)表示api1->api2->api3
    friend: bool = True  # 好友开关
    lolicon_key: str = ""  # lolicon Key

    class Config:
        extra = "ignore"
