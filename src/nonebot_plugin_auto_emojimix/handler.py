"""命令处理器"""

import re

from nonebot import on_message
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import EventPlainText
from nonebot.typing import T_State

from .config import plugin_config
from .service import (
    ComboNotFoundError,
    DownloadError,
    UnsupportedEmojiError,
    emoji_mix_service,
)


async def check_emojis(state: T_State, text: str = EventPlainText()) -> bool:
    text = text.strip()
    if not text or "+" not in text:
        return False
    if matched := re.match(emoji_mix_service.explicit_pattern, text):
        state["code1"] = matched.group("code1")
        state["code2"] = matched.group("code2")
        return True
    return False


async def check_auto_emojis(state: T_State, text: str = EventPlainText()) -> bool:
    """检查纯文本消息中是否包含两个相邻的可合成 emoji。

    仅在 auto_emojimix 配置启用时生效。
    跳过包含 '+' 号的消息，避免与显式合成处理器冲突。
    """
    if not plugin_config.auto_emojimix:
        return False
    text = text.strip()
    if not text or "+" in text:
        return False
    if matched := re.search(emoji_mix_service.auto_pattern, text):
        state["code1"] = matched.group("code1")
        state["code2"] = matched.group("code2")
        return True
    return False


emojimix = on_message(check_emojis, block=True)
auto_emojimix_matcher = on_message(check_auto_emojis, block=False, priority=20)


@emojimix.handle()
async def handle_emojimix(state: T_State, matcher: Matcher):
    """处理显式 emoji 合成请求 (emoji1+emoji2)"""
    try:
        result = await emoji_mix_service.mix_emoji(state["code1"], state["code2"])
        await matcher.finish(MessageSegment.image(result))
    except UnsupportedEmojiError as e:
        await matcher.finish(f"不支持的emoji：{e.emoji}")
    except ComboNotFoundError:
        await matcher.finish("不支持该emoji组合")
    except DownloadError:
        await matcher.finish("下载表情出错")


@auto_emojimix_matcher.handle()
async def handle_auto_emojimix(state: T_State, matcher: Matcher):
    """处理自动 emoji 合成（检测相邻 emoji 对）"""
    try:
        result = await emoji_mix_service.mix_emoji(state["code1"], state["code2"])
        await matcher.finish(MessageSegment.image(result))
    except (UnsupportedEmojiError, ComboNotFoundError, DownloadError):
        # 自动模式下，合成失败时静默忽略
        pass
