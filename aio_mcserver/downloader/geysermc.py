from aio_mcserver.downloader.geysermc_base import GeyserMCBase


class GeyserMC(GeyserMCBase):
    filename_regex = r"Geyser-Spigot-(\d+(?:\.\d+)*)-(\d+).jar"
    product_id = "geyser"
