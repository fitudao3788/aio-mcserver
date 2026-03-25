import re

from aio_mcserver.downloader.base import BaseDownloader
from aio_mcserver.downloader.download_info import DownloadInfo


class GitHubBase(BaseDownloader):
    repo_id: str
    asset_name: str
    asset_regex: str

    async def get_download_info(self) -> DownloadInfo:
        res = self.client.get("https://api.github.com/repos/{}/releases/latest".format(self.repo_id))
        res_data = await res.json()

        asset = None
        for asset_candidate in res_data["assets"]:
            if re.match(self.asset_regex, asset_candidate["browser_download_url"]):
                asset = asset_candidate
                break

        if asset is None:
            raise ValueError("No asset found for repo {}".format(self.repo_id))

        return DownloadInfo(
            filename="{}-{}.jar".format(self.asset_name, res_data["tag_name"]),
            url=asset["browser_download_url"],
            sha256=asset["digest"].repalce("sha256:", ""),
        )
