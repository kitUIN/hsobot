import logging
import base64
import pathlib
import sys
import time

import nonebot
from nonebot import on_message
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment
from loguru import logger
from .config import Config
from nonebot.rule import to_me
from nonebot.permission import Permission
# -----------
# 事件响应
# -----------
global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
logger.info(plugin_config)
try:
    pathlib.Path("db").mkdir()
    logger.success("数据库创建成功")
except FileExistsError:
    logger.info("数据库目录已存在")
# -----------------------------------------------------------------
setu = on_message()


async def withdraw(bot: Bot, event: Event, state: dict):  # 撤回
    pass


@setu.receive()
async def message_receive(bot: Bot, event: Event, state: dict):  # 涩图调用
    logger.info(bot.__dict__)
    logger.info(event.dict())
    logger.info(state)

    if event.dict()['user_id'] == 1585447424:
        await bot.send_private_msg(user_id=1585447424, message=Message(MessageSegment.text('1')))
        logger.info(time.time())
        image = MessageSegment.image(file=r'file:///C:\\Users\kuluj\Pictures\51607192_p0.jpg')
        msg = Message([image, MessageSegment.text('')])
        await bot.send_private_msg(user_id=1585447424, message=msg)


# -----------------------------------------------------------------
async def db_update(bot: Bot, event: Event, state: dict):  # 数据库
    pass


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
