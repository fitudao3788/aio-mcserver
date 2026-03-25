from aio_mcserver.downloader.base import BaseDownloader


class ViaBackwards(BaseDownloader):
    filename_regex = r"^ViaBackwards-(\d+(?:\.\d+)*)\.jar$"
    product_id = "ViaBackwards"
