""" 复读
"""
import secrets
from datetime import datetime, timedelta

from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.log import logger
from nonebot.typing import T_State

from .config import plugin_config
from .recorder import recorder_obj


def need_repeat(bot: Bot, event: Event, state: T_State) -> bool:
    """是否复读这个消息"""
    if not isinstance(event, GroupMessageEvent):
        return False

    # 不复读对机器人说的，因为这个应该由闲聊插件处理
    if event.to_me:
        return False

    group_id = event.group_id
    user_id = event.user_id

    # 只复读指定群内消息
    if group_id not in plugin_config.group_id:
        return False

    # 不要复读指令
    if event.raw_message.startswith("/"):
        return False

    # 记录群内发送消息数量和时间
    now = datetime.now()
    recorder_obj.add_msg_send_time(now, group_id)

    # 不要复读应用消息
    if user_id == 1000000:
        return False

    # 不要复读签到，分享，小程序，转发
    if event.message[0].type in ["sign", "share", "json", "forward"]:
        return False

    # 不要复读带网址的消息
    if (
        "http://" in event.raw_message.lower()
        or "https://" in event.raw_message.lower()
    ):
        return False

    # 复读之后一定时间内不再复读
    time = recorder_obj.last_message_on(group_id)
    if now < time + timedelta(minutes=plugin_config.repeat_interval):
        return False

    repeat_rate = plugin_config.repeat_rate
    # 当10分钟内发送消息数量大于30条时，降低复读概率
    # 因为排行榜需要固定概率来展示欧非，暂时取消
    # if recorder.message_number(10) > 30:
    #     logger.info('Repeat rate changed!')
    #     repeat_rate = 5

    # 记录每个人发送消息数量
    recorder_obj.add_msg_number_list(user_id, group_id)

    # 按照设定概率复读
    random = secrets.SystemRandom()
    rand = random.randint(1, 100)
    logger.info(f"repeat: {rand}")
    if rand > repeat_rate:
        return False

    # 记录复读时间
    recorder_obj.reset_last_message_on(group_id)

    # 记录复读次数
    recorder_obj.add_repeat_list(user_id, group_id)

    return True
