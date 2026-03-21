import os.path

from aio_mcserver.downloader.base import BaseDownloader


class PaperMCBase(BaseDownloader):
    product_id: str

    async def get_major_versions(self) -> list[str]:
        res = await  self.client.post("https://fill.papermc.io/graphql", json={
            "operationName": "ProjectFamilies",
            "query": "query ProjectFamilies($id: String!) { project(key: $id) { id families { id key __typename } __typename } }",
            "variables": {"id": self.product_id},
        })
        res_data = res.json()

        return [family["key"] for family in res_data["data"]["project"]["families"]]

    async def get_full_versions(self, major_version: str) -> list[str]:
        res = await self.client.post("https://fill.papermc.io/graphql", json={
            "operationName": "Family",
            "query": "query Family($project: String!, $id: String!) { project(key: $project) { id family(key: $id) { id key java { version { minimum __typename } flags { recommended __typename } __typename } __typename } versions(filterBy: {familyKey: $id}, first: 100, orderBy: {direction: DESC}) { edges { node { id key family { id key __typename } support { status end __typename } __typename } __typename } pageInfo { hasNextPage endCursor __typename } __typename } __typename }}",
            "variables": {"id": major_version, "project": self.product_id},
        })
        res_data = res.json()

        return [version["node"]["key"] for version in res_data["data"]["project"]["versions"]["edges"]]

    async def get_download_info(self, full_version: str) -> dict:
        res = await self.client.post("https://fill.papermc.io/graphql", json={
            "operationName": "VersionBuilds",
            "query": "query VersionBuilds($projectKey: String!, $versionKey: String!, $after: String) { project(key: $projectKey) { id version(key: $versionKey) { id builds(first: 25, after: $after, orderBy: {direction: DESC}) { edges { node { id number channel createdAt downloads { name size url checksums { sha256 __typename } __typename } commits { sha message __typename } __typename } __typename } pageInfo { hasNextPage hasPreviousPage startCursor endCursor __typename } __typename } __typename } __typename }}",
            "variables": {"projectKey": self.product_id, "versionKey": full_version},
        })
        res_data = res.json()

        if res_data["data"]["project"]["version"] is None:
            raise ValueError(f"Version {full_version} not found for product {self.product_id}")

        return {
            "filename": res_data["data"]["project"]["version"]["builds"]["edges"][0]["node"]["downloads"][0]["name"],
            "url": res_data["data"]["project"]["version"]["builds"]["edges"][0]["node"]["downloads"][0]["url"],
            "sha256": res_data["data"]["project"]["version"]["builds"]["edges"][0]["node"]["downloads"][0]["checksums"]["sha256"],
        }

    async def get_recommended_flags(self, full_version: str) -> list[str]:
        res = await self.client.post("https://fill.papermc.io/graphql", json={
            "operationName": "Version",
            "query": "query Version($projectKey: String!, $versionKey: String!) { project(key: $projectKey) { id version(key: $versionKey) { id key support { status end __typename } java { version { minimum __typename } flags { recommended __typename } __typename } family { id key java { version { minimum __typename } flags { recommended __typename } __typename } __typename } __typename } __typename }}",
            "variables": {"projectKey": self.product_id, "versionKey": full_version},
        })
        res_data = res.json()

        return res_data["data"]["project"]["version"]["family"]["java"]["flags"]["recommended"]
