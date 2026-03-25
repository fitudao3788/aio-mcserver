from aio_mcserver.downloader.base import BaseDownloader
from aio_mcserver.downloader.download_info import DownloadInfo


class GeyserMCBase(BaseDownloader):
    product_id: str

    async def get_download_info(self) -> DownloadInfo:
        res = await self.client.get("https://download.geysermc.org/v2/projects/{}/versions/latest/builds".format(self.product_id), follow_redirects=True)
        res_data = res.json()

        build_version = res_data["version"]
        build = {"build": 0, "downloads": {"spigot": {"sha256": ""}}}
        for build_candidate in res_data["builds"]:
            if build["build"] < build_candidate["build"]:
                build = build_candidate

        return DownloadInfo(
            filename="Geyser-Spigot-{}-{}.jar".format(build_version, build["build"]),
            url="https://download.geysermc.org/v2/projects/geyser/versions/{}/builds/{}/downloads/spigot".format(build_version, build["build"]),
            sha256=build["downloads"]["spigot"]["sha256"],
        )
