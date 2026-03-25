from aio_mcserver.downloader.papermc_base import PaperMCBase


class Paper(PaperMCBase):
    filename_regex = r"^paper-(\d+(?:\.\d+)*)-(\d+)\.jar$"
    product_id = "paper"
