import os
import sys

from loguru import logger
from ruamel.yaml import YAML

from aio_mcserver.config import AppConfig, Config
from aio_mcserver.downloader.floodgate import Floodgate
from aio_mcserver.downloader.geysermc import GeyserMC
from aio_mcserver.downloader.paper import Paper
from aio_mcserver.downloader.viabackwards import ViaBackwards
from aio_mcserver.downloader.viaversion import ViaVersion


class Setup:
    def __init__(self, conf: AppConfig, config_path: str):
        self.conf = conf
        self.config_path = config_path
        self.server_dir = conf.server.path
        self.bin_dir = os.path.join(self.server_dir, "bin")
        self.data_dir = os.path.join(self.server_dir, "data")
        self.plugins_dir = os.path.join(self.data_dir, "plugins")

        os.makedirs(self.server_dir, exist_ok=True)
        os.makedirs(self.bin_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.plugins_dir, exist_ok=True)

    def generate_startup_script(self, recommended_flags: list[str], filename: str):
        multiline = "^" if sys.platform == "win32" else "\\"

        startup_script = \
            ("@echo off" if sys.platform == "win32" else "#!/bin/bash") + "\n\n\n" + \
            ("rem" if sys.platform == "win32" else "#") + f" Startup Script for {filename}\n\n" + \
            ("mkdir %~dp0data > nul 2>&1\ncd /d %~dp0data" if sys.platform == "win32" else "mkdir $(dirname $0)/data > /dev/null 2>&1\ncd $(dirname $0)/data") + "\n\n" + \
            "echo eula=true> eula.txt\n\n" + \
            f"java {multiline}\n  {(" " + multiline + "\n  ").join(recommended_flags)} {multiline}\n  -jar {os.path.join("..", "bin", filename)}{multiline}\n  nogui"

        with open(os.path.join(self.server_dir, "run." + ("bat" if sys.platform == "win32" else "sh")), "w") as f:
            f.write(startup_script)

        if sys.platform != "win32":
            os.chmod(os.path.join(self.server_dir, "run.sh"), 0o755)

    async def download_server(self) -> str:
        async with Paper() as paper:
            logger.info("Checking for server version...")

            if self.conf.server.version:
                full_version = self.conf.server.version
            else:
                major_versions = await paper.get_major_versions()
                major_version = major_versions[0]
                minor_versions = await paper.get_full_versions(major_version)
                full_version = minor_versions[0]

                self.conf.server.version = full_version
                Config.save(self.conf, self.config_path)

            download_info = await paper.get_download_info(full_version)
            recommended_flags = await paper.get_recommended_flags(full_version)

            logger.info("Latest server file is {}".format(download_info["filename"]))

            if not os.path.exists(os.path.join(self.bin_dir, download_info["filename"])):
                logger.info("Updating server version...")

                await paper.cleanup_old_files(self.bin_dir)
                await paper.download(self.bin_dir, download_info)

        self.generate_startup_script(recommended_flags, download_info["filename"])

        return full_version

    async def download_geysermc(self):
        async with GeyserMC() as geyser:
            logger.info("Checking for GeyserMC version...")

            download_info = await geyser.get_download_info()

            logger.info("Latest GeyserMC file is {}".format(download_info["filename"]))

            if not os.path.exists(os.path.join(self.plugins_dir, download_info["filename"])):
                logger.info("Updating GeyserMC version...")

                await geyser.cleanup_old_files(self.plugins_dir)
                await geyser.download(self.plugins_dir, download_info)

    async def download_floodgate(self):
        async with Floodgate() as floodgate:
            logger.info("Checking for Floodgate version...")

            download_info = await floodgate.get_download_info()

            logger.info("Latest Floodgate file is {}".format(download_info["filename"]))

            if not os.path.exists(os.path.join(self.plugins_dir, download_info["filename"])):
                logger.info("Updating Floodgate version...")

                await floodgate.cleanup_old_files(self.plugins_dir)
                await floodgate.download(self.plugins_dir, download_info)

    async def download_viaversion(self):
        async with ViaVersion() as viaversion:
            logger.info("Checking for ViaVersion version...")

            download_info = await viaversion.get_download_info()

            logger.info("Latest ViaVersion file is {}".format(download_info["filename"]))

            if not os.path.exists(os.path.join(self.plugins_dir, download_info["filename"])):
                logger.info("Updating ViaVersion version...")

                await viaversion.cleanup_old_files(self.plugins_dir)
                await viaversion.download(self.plugins_dir, download_info)

    async def download_viabackwards(self):
        async with ViaBackwards() as viabackwards:
            logger.info("Checking for ViaBackwards version...")

            download_info = await viabackwards.get_download_info()

            logger.info("Latest ViaBackwards file is {}".format(download_info["filename"]))

            if not os.path.exists(os.path.join(self.plugins_dir, download_info["filename"])):
                logger.info("Updating ViaBackwards version...")

                await viabackwards.cleanup_old_files(self.plugins_dir)
                await viabackwards.download(self.plugins_dir, download_info)

    async def configure_geysermc(self):
        geysermc_config_path = os.path.join(self.data_dir, "plugins", "Geyser-Spigot", "config.yml")

        yaml = YAML()

        with open(geysermc_config_path, "r") as f:
            geysermc_config = yaml.load(f)

        geysermc_config["java"]["auth-type"] = "floodgate"

        with open(geysermc_config_path, "w") as f:
            yaml.dump(geysermc_config, f)
