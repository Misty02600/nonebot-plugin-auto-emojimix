# from nonebot import logger, require
from nonebot.plugin import PluginMetadata  # , inherit_supported_adapters

# require("nonebot_plugin_uninfo")
# require("nonebot_plugin_alconna")
# require("nonebot_plugin_localstore")
# require("nonebot_plugin_apscheduler")
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="名称",
    description="描述",
    usage="用法",
    type="application",  # application: 功能性插件 | library: 库插件
    homepage="https://github.com/owner/nonebot-plugin-template",
    config=Config,
    # supported_adapters=inherit_supported_adapters(
    #     "nonebot_plugin_alconna", "nonebot_plugin_uninfo"
    # ),
    supported_adapters={"~onebot.v11"},
    extra={"author": "owner <your@mail.com>"},
)
