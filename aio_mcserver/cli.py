import asyncio

import click
from loguru import logger

from aio_mcserver.config import Config, AppConfig
from aio_mcserver.server import Server
from aio_mcserver.setup import Setup

DEFAULT_CONFIG = "aio-mcserver.yaml"


async def start_server(conf: AppConfig):
    logger.info("Starting server...")

    server = Server(conf)
    await server.start()
    await server.wait()


async def cli_async(config_path: str):
    conf = Config.load_or_create(config_path)
    setup = Setup(conf, config_path)

    await setup.download_server()
    await setup.download_geysermc()
    await setup.download_mcxboxbroadcast()
    await setup.download_floodgate()
    await setup.download_viaversion()
    await setup.download_viabackwards()

    if not conf.initialized:
        logger.info("Initializing server...")

        server = Server(conf, True)
        await server.start()
        await server.wait()

        await setup.configure_geysermc()

        conf.initialized = True
        Config.save(conf, config_path)

    await start_server(conf)


@click.group(invoke_without_command=True)
@click.option("-c", "--config", type=click.Path(), default=DEFAULT_CONFIG, help="Specify the configuration file")
@click.pass_context
def cli(ctx, config):
    asyncio.run(cli_async(config))
