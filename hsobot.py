import pathlib

import nonebot
from loguru import logger
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

nonebot.init()
nonebot.load_plugins("src/plugins")
app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.config.command_start = {"#"}  # 更改指令符
driver.register_adapter("cqhttp", CQHTTPBot)


if __name__ == "__main__":
    logger.info(nonebot.get_driver().config)
    nonebot.run()

