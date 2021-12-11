from typing import Any

import httpx

from ..post import Post
from ..types import RawPost, Target
from .platform import NewMessage, NoTargetMixin


class FF14(NewMessage, NoTargetMixin):

    categories = {}
    platform_name = "ff14"
    name = "最终幻想XIV官方公告"
    enable_tag = False
    enabled = True
    is_common = False
    schedule_type = "interval"
    schedule_kw = {"seconds": 60}

    async def get_target_name(self, _: Target) -> str:
        return "最终幻想XIV官方公告"

    async def get_sub_list(self, _) -> list[RawPost]:
        async with httpx.AsyncClient() as client:
            raw_data = await client.get(
                "http://api.act.sdo.com/UnionNews/List?gameCode=ff&category=5309,5310,5311,5312,5313&pageIndex=0&pageSize=5"
            )
            return raw_data.json()["Data"]

    def get_id(self, post: RawPost) -> Any:
        """用发布时间当作 ID

        因为有时候官方会直接编辑以前的文章内容
        """
        return post["PublishDate"]

    def get_date(self, _: RawPost) -> None:
        return None

    async def parse(self, raw_post: RawPost) -> Post:
        text = f'{raw_post["Title"]}\n{raw_post["Summary"]}'
        url = raw_post["Author"]
        return Post("ff14", text=text, url=url, target_name="最终幻想XIV官方公告")
