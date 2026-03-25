from aio_mcserver.downloader.github_base import GitHubBase


class MCXboxBroadcast(GitHubBase):
    filename_regex = r"^MCXboxBroadcastExtension-(\d+)\.jar$"

    repo_id = "MCXboxBroadcast/Broadcaster"
    asset_name = "MCXboxBroadcastExtension"
    asset_regex = "MCXboxBroadcastExtension.jar"
