import asyncio
import logging
import base64
import pathlib
import sys
import time

import nonebot
from nonebot import on_message, on_regex
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment
from loguru import logger
from nonebot import on_command
from nonebot.typing import T_State

from .data_source import Setu
from .config import Config
from .model import Power
from nonebot.rule import to_me, regex
from nonebot.permission import Permission

# -----------
# 事件响应
# -----------
try:
    pathlib.Path("db").mkdir()
    logger.success("数据库创建成功")
except FileExistsError:
    logger.info("数据库目录已存在")
# -----------------------------------------------------------------
setu = on_regex(pattern='来(.*?)[点丶份张幅](.*?)的?(|r18)[色瑟涩🐍][图圖🤮]', priority=1)
db = on_command("", priority=2)
update_all = on_command("更新所有数据")


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
    await Power(bot, event).change(state)
    logger.info(bot.__dict__)
    logger.info(event.dict())
    logger.info(state)
    # asyncio.run(Power().update_all())


@update_all.handle()
async def update(bot: Bot, event: Event, state: dict):
    await Power(bot, event).update_all()


"""
x = {'time': 1612683655, 'self_id': 850558946, 'post_type': 'message', 'sub_type': 'normal', 'user_id': 2593603256,
     'message_type': 'group', 'message_id': 680281838,
     'message': [MessageSegment(
         type='image',
         data={
             'file': 'bcb8da591de5231eab798e41d19ba881.image',
             'url': 'http://gchat.qpic.cn/gchatpic_new/2593603256/1040904822-2738385081-BCB8DA591DE5231EAB798E41D19BA881/0?term=255'})],
     'raw_message': '[CQ:image,file=bcb8da591de5231eab798e41d19ba881.image]', 'font': 0,
     'sender': {'user_id': 2593603256, 'nickname': '妖', 'sex': 'unknown', 'age': 0, 'card': '', 'area': '', 'level': '',
                'role': 'member', 'title': ''}, 'to_me': False, 'reply': None, 'group_id': 1040904822,
'anonymous': None, 'message_seq': 73622}
"""
