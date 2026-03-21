import os.path

from aio_mcserver.downloader.base import BaseDownloader


class GeyserMC(BaseDownloader):
    filename_regex = r"Geyser-Spigot-(\d+(?:\.\d+)*)-(\d+).jar"

    async def get_download_info(self) -> dict:
        res = await self.client.get("https://download.geysermc.org/v2/projects/geyser/versions/latest/builds", follow_redirects=True)
        res_data = res.json()

        build_version = res_data["version"]
        build_id = res_data["builds"][0]["build"]

        return {
            "filename": f"Geyser-Spigot-{build_version}-{build_id}.jar",
            "url": f"https://download.geysermc.org/v2/projects/geyser/versions/{build_version}/builds/{build_id}/downloads/spigot",
            "sha256": res_data["builds"][0]["downloads"]["spigot"]["sha256"],
        }
