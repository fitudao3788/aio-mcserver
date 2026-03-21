from aio_mcserver.downloader.base import BaseDownloader


class ViaBackwards(BaseDownloader):
    filename_regex = r"^ViaBackwards-(\d+(?:\.\d+)*)\.jar$"

    async def get_download_info(self) -> dict:
        info_res = await self.client.get("https://hangar.papermc.io/api/v1/projects/ViaBackwards/versions?limit=1&offset=0&channel=Release&platform=PAPER&includeHiddenChannels=true")
        info_data = info_res.json()

        return {
            "filename": info_data["result"][0]["downloads"]["PAPER"]["fileInfo"]["name"],
            "url": info_data["result"][0]["downloads"]["PAPER"]["downloadUrl"],
            "sha256": info_data["result"][0]["downloads"]["PAPER"]["fileInfo"]["sha256Hash"],
        }
