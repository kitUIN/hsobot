from pydantic import BaseSettings
from pydantic.types import Path, Any, Union, Optional

# -----------
# 配置
# -----------
class Config(BaseSettings):
    # 全局
    superusers: list = [0]  # 超级管理员
    api0 = True  # 色图库是否开启 api0=yuban,api1=lolicon
    api1 = True  # setu库开启状况
    priority: tuple = (0, 1)  # 优先级
    friend: bool = True  # 好友开关
    lolicon_key: str = ""  # lolicon Key
    plugin_setting: str = "default"


    class Config:
        extra = "ignore"
