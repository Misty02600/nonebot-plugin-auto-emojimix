from nonebot import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    auto_emojimix: bool = True
    """是否自动触发表情合成。启用后，用户发送的纯文本中包含两个相邻的可合成 emoji 时，会自动发送合成图片。"""


plugin_config = get_plugin_config(Config)
