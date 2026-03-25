from aio_mcserver.downloader.geysermc_base import GeyserMCBase


class Floodgate(GeyserMCBase):
    filename_regex = r"floodgate-spigot-(\d+(?:\.\d+)*)-(\d+).jar"
    product_id = "floodgate"
