from aio_mcserver.downloader.papermc_base import PaperMCBase


class Paper(PaperMCBase):
    filename_regex = r"^paper-(\d+(?:\.\d+)*)-(\d+)\.jar$"
    product_id = "paper"


async def main():
    paper = Paper()

    major_versions = await paper.get_major_versions()
    print("Major Versions:", major_versions)

    major_version = major_versions[0]

    minor_versions = await paper.get_full_versions(major_version)
    print(f"Minor Versions for {major_version}:", minor_versions)

    full_version = minor_versions[0]

    download_info = await paper.get_download_info(full_version)
    print(f"Download Info for {full_version}:", download_info)

    recommended_flags = await paper.get_recommended_flags(full_version)
    print(f"Recommended Flags for {full_version}:", recommended_flags)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
