import os.path

from aio_mcserver.downloader.base import BaseDownloader


class Floodgate(BaseDownloader):
    filename_regex = r"floodgate-spigot-(\d+(?:\.\d+)*)-(\d+).jar"

    async def get_download_info(self) -> dict:
        res = await self.client.get("https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds", follow_redirects=True)
        res_data = res.json()

        build_version = res_data["version"]
        build = {"build": 0}
        for build_candidate in res_data["builds"]:
            if build["build"] < build_candidate["build"]:
                build = build_candidate

        return {
            "filename": f"floodgate-spigot-{build_version}-{build["build"]}.jar",
            "url": f"https://download.geysermc.org/v2/projects/floodgate/versions/{build_version}/builds/{build["build"]}/downloads/spigot",
            "sha256": build["downloads"]["spigot"]["sha256"],
        }
