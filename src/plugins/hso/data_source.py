import asyncio
import random
import re

import httpx
import nonebot
from loguru import logger
from nonebot.adapters.cqhttp import MessageSegment, Message, Bot, Event
from tinydb import Query

from .config import Config
from .model import group_config, friend_config, Power, status

# -------------------------------------------------------
#                       Setu 类包装
# -------------------------------------------------------
# todo tag_db,status 用于统计
global_config = nonebot.get_driver().config
hso_config = Config(**global_config.dict())  # 载入配置
logger.info(hso_config)
Q = Query()


class Setu:
    def __init__(self, bot: Bot, event: Event, state: dict, **requests_kwargs):
        self.r18 = state["_matched_groups"][2]
        self.num = state["_matched_groups"][0]
        self._REQUESTS_KWARGS = requests_kwargs
        self.tag: list = [i for i in list(set(re.split(r",|，|\.|-| |_|/|\\", state["_matched_groups"][1]))) if
                          i != ""]  # 分割tag+去重+去除空元素
        # -----------------------------------
        self.bot = bot
        self.event = event
        self.config = hso_config  # 全局设置
        self.message = event.dict()
        self.type = self.message["message_type"]
        self.setu_level = 1  # 默认涩图等级
        self.current_config = None  # 当前配置
        self.power = Power()
        self.del_list = list()

    async def send(self, file: str = "", msg: str = "", at: bool = False):  # 发送图片或文字
        # if file[1:4] != "http" and file[1:4] != "":  # 本地文件
        #    file = "file:///" + file
        message_segment = list()
        if file:
            message_segment.append(MessageSegment.image(file=file))
        if msg:
            message_segment.append(MessageSegment.text(msg))
        if at:
            message_segment.append(MessageSegment.at(self.event.dict()["user_id"]))
        message = Message(message_segment)
        return await self.bot.send(event=self.event, message=message)

    async def withdraw(self, id=None):
        await asyncio.sleep(30)
        if id:
            return await self.bot.delete_msg(message_id=id)
        for x in self.del_list:
            await self.bot.delete_msg(message_id=x)

    @staticmethod
    async def build_msg(api: int = -1,
                        title="",
                        author="",
                        uid="",
                        author_id="",
                        url="",
                        url_original=""):  # 构建消息
        if api == 0:  # lolicon.app
            msg = "标题:{title}\r\n作者:{author}\r\n[www.pixiv.net/users/{author_id}]\r\n作品id:{id}\r\n" \
                  "[www.pixiv.net/artworks/{id}]\r\n原图:{url_original}\r\n".format(title=title, id=uid, url=url,
                                                                                  author_id=author_id, author=author,
                                                                                  url_original=url_original)
        elif api == 1:  # yande.re
            msg = "标题:{title}\r\n作者:{author}\r\n原图:{url_original}\r\n(需要科学上网)\r\n".format(
                title=title,
                author=author,
                url_original=url_original
            )
        else:
            msg = "msg配置错误,请联系管理员"
        return msg

    def data_build(self, mold):
        if mold == "status":
            data = {
                'group_id': self.message["group_id"],
                'num': 0
            }
            return data

    async def api_1(self):  # https://api.lolicon.app/
        if not self.config.api1 or self.num < 1:  # 兼容api0
            return
        if self.setu_level == 1:
            r18 = 0
        elif self.setu_level == 3:
            r18 = random.choice([0, 1])
        elif self.setu_level == 2:
            r18 = 1
        else:
            r18 = 0
        get_num = 0
        url = "https://api.lolicon.app/setu"
        params = {"r18": r18,
                  "apikey": self.config.lolicon_key,
                  "num": self.num,
                  "size1200": not bool(self.current_config[self.type]["original"])}
        if self.num > 10:
            params["num"] = 10
        if len(self.tag) != 1 or (len(self.tag[0]) != 0 and not self.tag[0].isspace()):  # 如果tag不为空(字符串字数不为零且不为空)
            params["keyword"] = self.tag
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(url, params=params, timeout=5)
                setu_data = res.json()
        except Exception as e:
            logger.warning("api1 boom~ :{}".format(e))
        else:
            if res.status_code == 200:
                for data in setu_data["data"]:
                    msg = await self.build_msg(api=1, title=data["title"], uid=data["pid"], author=data["author"],
                                               author_id=data["uid"],
                                               url_original="https://i.pixiv.cat/img-original/img/{}".format(
                                                   re.findall("img/(.*)", data["url"])[0].replace("_master1200", "")))
                    id = await self.send(file=data["url"], msg=msg)
                    get_num += 1
                    self.num -= 1
                    self.del_list.append(id['message_id'])  # 撤回表单
                logger.info(
                    "从loliconのapi获取到{}张关于{}的Setu  实际发送{}张".format(setu_data["count"], self.tag, get_num))  # 打印获取到多少条
            else:
                logger.warning("api1:{}".format(res.status_code))

    """
    def api_2(self):  # https://yande.re/ 需要梯子且速度极其慢，不建议使用,异步用法未写
        url = "https://yande.re/post.json"
        if config["proxies"]:
            _REQUESTS_KWARGS = {
                "proxies": {
                    "https": config["proxy"],  # "http://127.0.0.1:10809"  代理
                }
            }
        else:
            _REQUESTS_KWARGS = dict()
        if len(self.tag) > 0:
            tag_switch = 1
        else:
            tag_switch = 0
        params = {"api_version": 2,
                  "tags": self.tag,
                  "limit": self.num,
                  "include_tags": tag_switch,
                  "filter": 1}
        if self.num > 10:  # api限制不能大于10
            params["num"] = 10
        try:
            res = requests.get(url, params, **_REQUESTS_KWARGS)
            setu_data = res.json()
        except Exception as e:
            logger.error("api0 boom~")
            logger.error(e)
        else:
            if res.status_code == 200:
                for data in setu_data["posts"]:
                    id = data["id"]
                    file_url = data["file_url"]
                    if self.if_sent(id):  # 判断是否发送过
                        continue
                    url_original = data["source"]
                    msg = self.build_msg(level="api0", title=data["tags"], author=data["author"],
                                         url_original=url_original)
                    with requests.get(file_url, **_REQUESTS_KWARGS) as resp:
                        with open("./tmp.jpg", "wb") as fd:
                            fd.write(resp.content)
                    sendMsg.send_pic(self.ctx, msg, picPath="./tmp.jpg")
                    self.api_0_realnum += 1
                # else:
                #     logger.warning("api0:{}".format(res.status_code))
            logger.info(
                "从yandeのapi获取到{}张setu  实际发送{}张".format(len(setu_data["posts"]), self.api_0_realnum))  # 打印获取到多少条
    """

    async def processing_and_inspect(self):  # 处理消息+调用
        # -----------------------------------------------
        if self.num == "一" or self.num == "":
            self.num = 1
        elif self.num == "二" or self.num == "俩" or self.num == "两":
            self.num = 2
        elif self.num == "三":
            self.num = 3
        elif self.num != "":
            # 如果指定了数量
            try:
                self.num = int(self.num)
            except ValueError:  # 出错就说明不是数字
                await self.send(msg="不会真的有人连数数字都不会输入吧！")
                return
            if self.num <= 0:  # ?????
                await self.send(msg="你想笑死我好继承我的负产吗¿¿¿")
                return
        else:  # 未指定默认1
            self.num = 1
        # -----------------------------------------------
        if self.type in ["group", "temp"]:
            if not self.current_config[self.type]["setu"]:
                return await self.send(msg="啊嘞啊嘞，涩图还没开呢~")
            if self.num > self.current_config[self.type]["max_num"]:
                return await self.send(msg="要这么多涩图你怎么不冲死呢¿")
            if self.r18:
                self.setu_level = self.current_config[self.type]["setu_level"]
                if self.setu_level < 2:
                    await self.send(msg="太涩了，你不能看哼~")
                    return
            if self.type == "group":  # 统计调用数量
                info = status.search(Q["group_id"] == self.message["group_id"])
                now_num = info[0]["num"] + self.num
                if self.current_config["group"]["top"] >= now_num:  # 上限判断
                    self.call = await self.send(
                        msg="当天已调用：{}\r\n群剩余调用：{}".format(str(now_num),
                                                          str(self.current_config["group"]["top"] - now_num)))
                elif self.current_config["group"]["top"] == 0:
                    pass
                else:
                    return await self.send(
                        msg="当天已调用：{}\r\n再调用{}超过上限了呢~".format(str(info[0]["num"]), str(self.num)))
                if info:
                    info = info[0]
                    info["num"] += self.num
                    logger.info(info["num"])
                    status.update(info, Q["group_id"] == self.message["group_id"])
                else:
                    info = self.data_build("status")
                    info["num"] += self.num
                    logger.info(info["num"])
                    status.insert(info)

        elif self.type == "private":
            if self.r18:
                self.setu_level = 2
            if self.current_config[self.type]["setu_level"] is vars():
                self.setu_level = self.current_config[self.type]["setu_level"]

        await self.action()

    async def main(self):  # 判断消息类型给对应函数处理
        if self.type != "private":  # 群聊or临时会话
            data = group_config.search(Q["group_id"] == self.message["group_id"])[0]  # 数据库
            if data:  # 查询group数据库数据
                self.current_config = data
            else:
                await self.power.group_build(self.message["group_id"])
                self.current_config = group_config.search(Q["group_id"] == self.message["group_id"])[0]
            await self.processing_and_inspect()
        else:  # 好友会话
            data = friend_config.search(Q["user_id"] == self.message["user_id"])
            if data:  # 该QQ如果自定义过
                self.current_config = data
            else:
                self.current_config = {}
            # 如果没有自定义 就是默认行为
            await self.processing_and_inspect()

    async def action(self):  # 判断数量
        for i in self.config.priority:
            if getattr(self.config, "api{}".format(i)):
                t = eval("self.api_{}".format(i))
                await t()
        await self.withdraw(id=self.call['message_id'])
        if self.current_config[self.type]["revoke"]:  # 撤回
            await self.withdraw()
        if self.num != 0:
            await self.send(msg="淦！你的xp好奇怪啊！")
            return
        return
