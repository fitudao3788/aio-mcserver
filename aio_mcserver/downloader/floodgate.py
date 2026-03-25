import os.path

from aio_mcserver.downloader.base import BaseDownloader


class Floodgate(BaseDownloader):
    filename_regex = r"floodgate-spigot-(\d+(?:\.\d+)*)-(\d+).jar"

    async def get_download_info(self) -> dict:
        res = await self.client.get("https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds", follow_redirects=True)
        res_data = res.json()

        build_version = res_data["version"]
        build_id = 0
        for build in res_data["builds"]:
            if build_id < build["build"]:
                build_id = build["build"]

        return {
            "filename": f"floodgate-spigot-{build_version}-{build_id}.jar",
            "url": f"https://download.geysermc.org/v2/projects/floodgate/versions/{build_version}/builds/{build_id}/downloads/spigot",
            "sha256": res_data["builds"][0]["downloads"]["spigot"]["sha256"],
        }
