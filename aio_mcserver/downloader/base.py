import hashlib
import os
import re

import httpx

from aio_mcserver.downloader.download_info import DownloadInfo


class BaseDownloader:
    filename_regex: str

    async def __aenter__(self):
        self.client = httpx.AsyncClient()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def cleanup_old_files(self, target_dir: str):
        for filename in os.listdir(target_dir):
            if re.match(self.filename_regex, filename):
                os.remove(os.path.join(target_dir, filename))

    async def download(self, target_dir: str, download_info: DownloadInfo):
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        dl_res = await self.client.get(download_info.url)
        dl_res.raise_for_status()

        if hashlib.sha256(dl_res.content).digest().hex() != download_info.sha256:
            raise ValueError("Invalid sha256 hash: {}".format(download_info.filename))

        with open(os.path.join(target_dir, download_info.filename), "wb") as f:
            f.write(dl_res.content)
