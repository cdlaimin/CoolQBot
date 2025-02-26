""" 日程表

https://pcrbot.github.io/pcr-calendar/#cn
"""
from datetime import datetime, timedelta
from typing import Dict, Optional, Set

import httpx
from nonebot import get_bot
from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler

from .config import plugin_config


class Calender:
    def __init__(self):
        # 动态的地址
        self._url = "https://pcrbot.github.io/calendar-updater-action/cn.json"
        # 定时任务
        self._job = None
        # 日程表
        self._timeline: Dict[str, Set[str]] = {}
        self._timeline_update_time: datetime = datetime.now()

        self.init()

    def init(self):
        """初始化日程自动推送"""
        logger.info("初始化 公主连结Re:Dive 日程推送")
        self._job = scheduler.add_job(
            self.push_calender,
            "cron",
            hour=plugin_config.calender_hour,
            minute=plugin_config.calender_minute,
            second=plugin_config.calender_second,
            id="push_calender",
        )

    async def refresh_calender(self) -> None:
        """获取最新的日程表"""
        if self._timeline:
            # 最近四小时内才更新的不用再次更新
            if self._timeline_update_time > datetime.now() - timedelta(hours=4):
                return None
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(self._url)
                if r.status_code != 200:
                    # 如果 HTTP 响应状态码不是 200，说明调用失败
                    return None

                # 清楚以前的时间线
                self._timeline.clear()
                for event in r.json():
                    start_time = datetime.strptime(
                        event["start_time"], "%Y/%m/%d %H:%M:%S"
                    )
                    end_time = datetime.strptime(event["end_time"], "%Y/%m/%d %H:%M:%S")
                    name = event["name"]
                    self.add_event(start_time, end_time, name)

                self._timeline_update_time = datetime.now()
                logger.info("公主连结Re:Dive 日程表刷新成功")
        except (httpx.HTTPError, KeyError) as e:
            logger.error(f"获取日程表出错，{e}")
            # 抛出上面任何异常，说明调用失败
            return None

    def add_event(self, start_time: datetime, end_time: datetime, name: str) -> None:
        """添加日程至日程表"""
        t = start_time
        while t <= end_time:
            daystr = t.strftime("%Y%m%d")
            if daystr not in self._timeline:
                self._timeline[daystr] = set()
            self._timeline[daystr].add(name)
            t += timedelta(days=1)

    async def push_calender(self):
        """推送日程"""
        # 没有启用的群则不推送消息
        if not plugin_config.push_calender_group_id:
            return

        logger.info("推送今日 公主连结Re:Dive 日程")

        await self.refresh_calender()

        date = datetime.now()
        events = self._timeline.get(date.strftime("%Y%m%d"))
        if events is None:
            events_str = "无活动或无数据"
        else:
            events_str = "\n".join(events)

        try:
            bot = get_bot()
        except ValueError:
            bot = None

        reply = "公主连结Re:Dive 今日活动：\n{}".format(events_str)
        for group_id in plugin_config.push_calender_group_id:
            if bot:
                await bot.send_msg(
                    message_type="group", group_id=group_id, message=reply
                )
            else:
                logger.warning("no bot connected")

    async def get_week_events(self) -> str:
        """获取日程表"""
        await self.refresh_calender()

        reply = "一周日程："
        date = datetime.now()

        for _ in range(7):
            events = self._timeline.get(date.strftime("%Y%m%d"), ())
            events_str = "\n⨠".join(sorted(events))
            if events_str == "":
                events_str = "没有记录"
            daystr = date.strftime("%Y%m%d")
            reply += f"\n======{daystr}======\n⨠{events_str}"
            date += timedelta(days=1)

        reply += "\n\n更多日程：https://pcrbot.github.io/pcr-calendar/#cn"

        return reply


calender_obj = Calender()
