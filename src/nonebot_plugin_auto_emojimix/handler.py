"""命令处理器"""

import re

from cachetools import TTLCache
from nonebot import on_message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import EventPlainText
from nonebot.rule import Rule
from nonebot.typing import T_State

from .config import plugin_config
from .service import (
    ComboNotFoundError,
    DownloadError,
    UnsupportedEmojiError,
    emoji_mix_service,
)

# 用户冷却缓存：key=user_id，过期自动清理
_cooldown_cache: TTLCache[str, bool] | None = (
    TTLCache(maxsize=4096, ttl=plugin_config.emojimix_cd)
    if plugin_config.emojimix_cd > 0
    else None
)


# Rule 函数


async def _check_cooldown(event: MessageEvent) -> bool:
    """冷却检查：用户是否在冷却中（只读，不设置冷却）。"""
    if _cooldown_cache is None:
        return True
    return event.get_user_id() not in _cooldown_cache


async def _check_explicit(state: T_State, text: str = EventPlainText()) -> bool:
    """显式模式匹配：emoji1+emoji2。"""
    if not plugin_config.emojimix:
        return False
    text = text.strip()
    if not text or "+" not in text:
        return False
    if matched := re.match(emoji_mix_service.explicit_pattern, text):
        state["code1"] = matched.group("code1")
        state["code2"] = matched.group("code2")
        return True
    return False


async def _check_auto(state: T_State, text: str = EventPlainText()) -> bool:
    """自动模式匹配：两个相邻 emoji。"""
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


# Matcher 注册
emojimix = on_message(Rule(_check_explicit, _check_cooldown), block=True)
auto_emojimix_matcher = on_message(
    Rule(_check_auto, _check_cooldown), block=False, priority=20
)


# Handler


@emojimix.handle()
async def handle_emojimix(event: MessageEvent, state: T_State, matcher: Matcher):
    """处理显式 emoji 合成请求 (emoji1+emoji2)"""
    if _cooldown_cache is not None:
        _cooldown_cache[event.get_user_id()] = True
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
async def handle_auto_emojimix(event: MessageEvent, state: T_State, matcher: Matcher):
    """处理自动 emoji 合成（检测相邻 emoji 对）"""
    if _cooldown_cache is not None:
        _cooldown_cache[event.get_user_id()] = True
    try:
        result = await emoji_mix_service.mix_emoji(state["code1"], state["code2"])
        await matcher.finish(MessageSegment.image(result))
    except (UnsupportedEmojiError, ComboNotFoundError, DownloadError):
        # 自动模式下，合成失败时静默忽略
        pass
