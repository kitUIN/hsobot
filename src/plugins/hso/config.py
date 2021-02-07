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

    # --------------------------------------库设置--------------------------------------
    plugin_setting: str = "default"
    setu_level = {"group": 1, "temp": 3}  # 默认等级 0:正常 1:性感 2:色情 3:All
    original = {"group": False, "temp": False}  # 是否原图
    setu = {"group": False, "temp": True}  # 色图功能开关
    r18 = {"group": False, "temp": True}  # 是否开启r18
    max_num = {"group": 3, "temp": 3}  # 一次最多数量
    revoke = {"group": 20, "temp": 0}  # 撤回消息延时(0为不撤回)

    class Config:
        extra = "ignore"
