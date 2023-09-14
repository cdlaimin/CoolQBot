from pathlib import Path

import nonebot
import pytest
from loguru import logger
from nonebug import NONEBOT_INIT_KWARGS
from nonebug.app import App


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {
        "datastore_database_url": "sqlite+aiosqlite:///:memory:"
    }


@pytest.fixture(scope="session", autouse=True)
def load_plugin(nonebug_init: None):
    from nonebot.adapters.onebot.v11 import Adapter

    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)

    nonebot.load_plugin("nonebot_plugin_datastore")
    nonebot.load_plugin("nonebot_plugin_apscheduler")
    nonebot.load_plugin("nonebot_plugin_saa")
    nonebot.load_plugin("nonebot_plugin_alconna")
    nonebot.load_plugin("nonebot_plugin_session")
    nonebot.load_plugin("nonebot_plugin_userinfo")

    nonebot.load_plugins(str(Path(__file__).parent.parent / "src" / "plugins"))


@pytest.fixture
async def app(nonebug_init: None, tmp_path: Path):
    from nonebot_plugin_datastore.config import plugin_config
    from nonebot_plugin_datastore.db import init_db

    driver = nonebot.get_driver()
    # 清除连接钩子，现在 NoneBug 会自动触发 on_bot_connect
    driver._bot_connection_hook.clear()

    # 插件数据目录
    plugin_config.datastore_cache_dir = tmp_path / "cache"
    plugin_config.datastore_config_dir = tmp_path / "config"
    plugin_config.datastore_data_dir = tmp_path / "data"

    await init_db()

    return App()


@pytest.fixture
def caplog(caplog):
    handler_id = logger.add(caplog.handler, format="{message}")
    yield caplog
    logger.remove(handler_id)
