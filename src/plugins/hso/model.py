import httpx
from loguru import logger
from nonebot.adapters.cqhttp import MessageSegment, Message, Bot, Event
from nonebot.typing import T_State
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

Q = Query()


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


send = Send()


class Power:

    @staticmethod
    def _group_default():
        """
        setu_level默认等级 0:正常 1:性感 2:色情 3:All
        original   是否原图
        setu  色图功能开关
        r18 是否开启r18
        max_num 一次最多数量
        revoke 撤回消息延时(0为不撤回)"""
        data = {
            "group": {"setu_level": 1,
                      "original": False,
                      "setu": False,
                      "r18": False,
                      "max_num": 3,
                      "revoke": True,
                      "at": True,
                      "top": 10},
            "temp": {"setu_level": 3,
                     "original": False,
                     "setu": True,
                     "r18": True,
                     "max_num": 3,
                     "revoke": False,
                     "at": False}}
        # -----------------------------------------------------
        return data

    async def _update_data(self, group_id, data=None):
        if group_config.search(Q["group_id"] == group_id):
            logger.info('群:{}已存在,更新数据~'.format(group_id))
            group_config.update(data, Q['group_id'] == group_id)
        else:
            default = self._group_default()
            if data:
                default.update(data)
            logger.info("群:{}不存在,插入数据~".format(group_id))
            group_config.insert(default)

    async def group_build(self, group_id):
        admin = list()
        owner = 0
        group = dict()
        # data = group_config.search(Q["group_id"] == group_id)
        # if data:
        #    group = data
        member = await send.get_group_member_list(group_id=group_id)
        for i in member:
            if i["role"] == "admin":
                admin.append(i["user_id"])
            elif i["role"] == "owner":
                owner = i["user_id"]
        group["admins"] = admin  # 管理员列表 等级2
        group["owner"] = owner  # 群主 等级 1
        group["group_id"] = group_id
        await self._update_data(group_id, group)  # 更新配置

    async def update_all(self):
        logger.info("开始更新所有群数据~")
        data = await send.get_group_list()
        group_ids = [x["group_id"] for x in data]
        for group_id in group_ids:
            await self.group_build(group_id)
        logger.success("更新群信息成功~")
        return

    @staticmethod
    async def change(bot: Bot, event: Event, state: T_State):
        """修改配置\r\n
        type:\r\n
        group\r\n
        private\r\n
        order:\r\n
        "setu_level"\r\n
        "original"\r\n
        "setu"\r\n
        "r18"\r\n
        "max_num"\r\n
        "revoke"\r\n
        "at"\r\n
        """
        key = state["key"]
        data = dict()
        mold = event.dict()["message_type"]
        if mold == "group":
            config = group_config.search(Q["group_id"] == event.dict()['group_id'])[0]
            admins = config["admins"]
            admins.append(config["owner"])
            if event.get_user_id in admins:
                data = config
                before = str(config[key[1]])
                if key[0] == "开启":
                    data["group"][key[1]] = True
                    after = "True"
                elif key[0] == "关闭":
                    data["group"][key[1]] = False
                    after = "False"
                else:
                    try:
                        data["group"][key[1]] = int(key[2])
                    except:
                        data["group"][key[1]] = key[2]
                    after = key[2]
                group_config.update(data, Q["group_id"] == event.dict()['group_id'])
                return await bot.send(event=event,
                                      message=Message(MessageSegment.text('{}：{}-->{}'.format(key[1], before, after))))
            else:
                return await bot.send(event=event,
                                      message=Message(MessageSegment.text('¿没权限还玩🐎¿')))

        elif mold == 'private':
            pass  # todo
