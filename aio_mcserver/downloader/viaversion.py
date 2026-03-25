from aio_mcserver.downloader.hangar_base import HangarBase


class ViaVersion(HangarBase):
    filename_regex = r"^ViaVersion-(\d+(?:\.\d+)*)\.jar$"
    product_id = "ViaVersion"
