import asyncio
import os.path
import sys

import click
from loguru import logger

from aio_mcserver.config import Config, AppConfig
from aio_mcserver.setup import Setup

DEFAULT_CONFIG = "aio-mcserver.yaml"


async def start_server(conf: AppConfig):
    startup_path = os.path.join(".", "run.bat" if sys.platform == "win32" else "run.sh")

    logger.info("Starting server...")

    proc = await asyncio.create_subprocess_shell(startup_path, cwd=conf.server.path)
    await proc.wait()


async def cli_async(config_path: str):
    conf = Config.load_or_create(config_path)
    setup = Setup(conf, config_path)

    await setup.download_server()
    await setup.download_geysermc()
    await setup.download_floodgate()
    await setup.download_viaversion()
    await setup.download_viabackwards()

    await start_server(conf)


@click.group(invoke_without_command=True)
@click.option("-c", "--config", type=click.Path(), default=DEFAULT_CONFIG, help="Specify the configuration file")
@click.pass_context
def cli(ctx, config):
    asyncio.run(cli_async(config))
