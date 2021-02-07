
import json
import pathlib
import sys
import asyncio
import httpx

from loguru import logger
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
# ---------
# 公用数据库
# ---------
group_config = TinyDB("./db/group_config.json")
friend_config = TinyDB("./db/friend_config.json")
tag_db = TinyDB("./db/tag.json")
status = TinyDB("./db/status.json")
db_tmp = TinyDB(storage=MemoryStorage)


class Send:
    def __init__(self):
        self.url = "http://127.0.0.1:5700/"

    async def get_group_list(self):  # 获得群列表
        async with httpx.AsyncClient() as client:
            res = await client.post(self.url + "get_group_list")
            return res.json()["data"]

    async def get_group_member_list(self, group_id):  # 获得群成员列表
        async with httpx.AsyncClient() as client:
            res = await client.post(self.url + "get_group_member_list", params={"group_id": group_id})
            return res.json()["data"]

    async def send_msg(self, message_typ: str = None,
                       user_id: int = None,
                       group_id: int = None,
                       message=None,
                       auto_escape: bool = False):  # 发送消息
        async with httpx.AsyncClient() as client:
            res = await client.post(self.url + "send_msg",
                                    params={
                                        "message_typ": message_typ,
                                        "user_id": user_id,
                                        "group_id": group_id,
                                        "message": message,
                                        "auto_escape": auto_escape})
            return res.json()


Q = Query()
send = Send()


class Power:
    @staticmethod
    def _default_data(config=None):
        data = {"setu_level": {"group": 1, "temp": 3}, "original": {"group": False, "temp": False},
                "setu": {"group": False, "temp": True}, "r18": {"group": False, "temp": True},
                "max_num": {"group": 3, "temp": 3}, "revoke": {"group": 20, "temp": 0}, "at": False}
        # -----------------------------------------------------
        if config:
            data["setu_level"] = config.setu_level
            data["original"] = config.original
            data["setu"] = config.setu
            data["r18"] = config.r18
            data["max_num"] = config.max_num
            data["revoke"] = config.revoke
            data["at"] = config.at
        return data

    async def _update_data(self, data, group_id):
        if await group_config.search(Q["GroupId"] == group_id):
            logger.info('群:{}已存在,更新数据~'.format(group_id))
            await group_config.update(data, Q['GroupId'] == group_id)
        else:
            default = self._default_data(data)
            logger.info("群:{}不存在,插入数据~".format(group_id))
            await group_config.insert(default)

    async def update_all(self):
        logger.info("开始更新所有群数据~")
        data = await send.get_group_list()
        group_ids = [await x["group_id"] async for x in data]
        for group_id in group_ids:
            admin = list()
            owner = 0
            group = dict()
            member = await send.get_group_member_list(group_id)
            async for i in member:
                if i["role"] == "admin":
                    admin.append(i["user_id"])
                elif i["role"] == "owner":
                    owner = await i["user_id"]
            group["admins"] = admin  # 管理员列表 等级2
            group["owner"] = owner  # 群主 等级 1
            await self._update_data(group, group_id)  # 更新配置
        logger.success("更新群信息成功~")
        return
