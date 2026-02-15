"""
nonebot-plugin-auto-emojimix

将两个emoji合成为一张图片
"""

from nonebot.plugin import PluginMetadata

from . import handler as handler
from .config import PuginConfig

__plugin_meta__ = PluginMetadata(
    name="emoji合成",
    description="将两个emoji合成为一张图片",
    usage="{emoji1}+{emoji2}，如：😎+😁",
    type="application",
    homepage="https://github.com/Misty02600/nonebot-plugin-auto-emojimix",
    config=PuginConfig,
    supported_adapters={"~onebot.v11"},
    extra={
        "example": "😎+😁",
    },
)
