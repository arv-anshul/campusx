from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from typing import Self


class BaseDownloader(ABC):
    def __init__(self, client: httpx.Client, url: str) -> None:
        self._url = url
        self._client = client

    def _request(self, url: str) -> bytes:
        res = self._client.get(url)
        if res.status_code == 200:
            return res.content
        raise httpx.HTTPStatusError(
            f"Response has not the required status code {res.status_code}.",
            request=res.request,
            response=res,
        )

    @classmethod
    def infer(cls, client: httpx.Client, url: str) -> Self:
        if all(cls._infer_conditions(url)):
            return cls(client, url)
        raise TypeError(f"url is not inferred as {type(cls).__name__}")

    @abstractmethod
    def download(self) -> bytes:
        ...

    @classmethod
    @abstractmethod
    def _infer_conditions(cls, url: str) -> tuple[bool, ...]:
        ...


class ColabNotebookDownloader(BaseDownloader):
    def download(self) -> bytes:
        _, file_id = self._url.rsplit("/", 1)
        file_id, _ = file_id.split("?", 1)
        return self._request(f"https://drive.google.com/uc?id={file_id}")

    @classmethod
    def _infer_conditions(cls, url: str) -> tuple[bool, ...]:
        return (url.startswith("https://docs.google.com/"),)


class GithubFileDownloader(BaseDownloader):
    def download(self) -> bytes:
        return self._request(self._url.replace("/blob", "/raw"))

    @classmethod
    def _infer_conditions(cls, url: str) -> tuple[bool, ...]:
        return (
            url.startswith("https://github.com/"),
            url.endswith((".py", ".pdf", ".ipynb")),
        )


class GoogleDriveFileDownloader(BaseDownloader):
    def download(self) -> bytes:
        _, file_id, _ = self._url.rsplit("/", 2)
        return self._request(f"https://drive.google.com/uc?id={file_id}")

    @classmethod
    def _infer_conditions(cls, url: str) -> tuple[bool, ...]:
        return (url.startswith("https://drive.google.com/file/d/"),)


class GoogleDocsDownloader(GoogleDriveFileDownloader):
    @classmethod
    def _infer_conditions(cls, url: str) -> tuple[bool, ...]:
        return (url.startswith("https://docs.google.com/spreadsheets/d/"),)


ALL_DOWNLOADERS: list[type[BaseDownloader]] = [
    ColabNotebookDownloader,
    GithubFileDownloader,
    GoogleDocsDownloader,
    GoogleDriveFileDownloader,
]


def infer_downloader(client: httpx.Client, url: str) -> BaseDownloader:
    for downloader in ALL_DOWNLOADERS:
        try:
            return downloader.infer(client, url)
        except TypeError:
            continue
    else:
        raise TypeError("url is not inferred as any defined `DownloaderFactory`")
