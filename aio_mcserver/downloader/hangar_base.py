from aio_mcserver.downloader.base import BaseDownloader
from aio_mcserver.downloader.download_info import DownloadInfo


class HangarBase(BaseDownloader):
    product_id: str

    async def get_download_info(self) -> DownloadInfo:
        res = await self.client.get("https://hangar.papermc.io/api/v1/projects/{}/versions?limit=1&offset=0&channel=Release&platform=PAPER&includeHiddenChannels=true".format(self.product_id))
        res_data = res.json()

        return DownloadInfo(
            filename=res_data["result"][0]["downloads"]["PAPER"]["fileInfo"]["name"],
            url=res_data["result"][0]["downloads"]["PAPER"]["downloadUrl"],
            sha256=res_data["result"][0]["downloads"]["PAPER"]["fileInfo"]["sha256Hash"],
        )
