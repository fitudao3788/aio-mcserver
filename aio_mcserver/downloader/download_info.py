import dataclasses


@dataclasses.dataclass
class DownloadInfo:
    filename: str
    url: str
    sha256: str
