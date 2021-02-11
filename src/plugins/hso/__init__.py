import asyncio

from loguru import logger
from nonebot import on_command
from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, Event

from .data_source import Setu
from .model import Power

# -----------
# 事件响应
# -----------


# -----------------------------------------------------------------
setu = on_regex(pattern='来(.*?)[点丶份张幅](.*?)的?(|r18)[色瑟涩🐍][图圖🤮]', priority=1)
db = on_command("", priority=2)
asyncio.run(Power().update_all())

@setu.receive()
async def message_receive(bot: Bot, event: Event, state: dict):  # 涩图调用
    logger.info(bot.__dict__)
    logger.info(event.dict())
    logger.info(state)
    await Setu(bot, event, state).main()


# -----------------------------------------------------------------

@db.handle()
async def db_update(bot: Bot, event: Event, state: dict):  # 数据库
    args = str(event.get_message()).strip().split()
    state["key"] = args
    await Power().change(bot, event, state)
    logger.info(bot.__dict__)
    logger.info(event.dict())
    logger.info(state)

