from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar
from urllib.parse import urlparse

import httpx

if TYPE_CHECKING:
    from typing import Self


def _check_url_netloc(url: str, *netloc: str) -> bool:
    """
    Returns `bool` after checking whether any `netloc` value is equal to url's netloc.
    """
    return any(urlparse(url).netloc == i for i in netloc)


@dataclass(frozen=True)
class BaseDownloader(ABC):
    url: str
    _DEFAULT_FILENAME: ClassVar[str] = "file.txt"

    def request(self, url: str, client: httpx.Client) -> httpx.Response:
        res = client.get(url)
        if res.status_code == 200:
            return res
        raise httpx.HTTPStatusError(
            f"Response has not required status code 200 instead got {res.status_code}",
            request=res.request,
            response=res,
        )

    def infer(self) -> Self:
        if all(self._infer_conditions(self.url)):
            return self
        raise TypeError(f"url not inferred for {type(self).__name__}")

    @property
    @abstractmethod
    def download_url(self) -> str: ...

    def download(self, client: httpx.Client) -> tuple[str, bytes]:
        print(type(self).__name__, self.url)
        response = self.request(self.download_url, client)
        return self.filename(response), response.content

    @abstractmethod
    def _infer_conditions(self, url: str) -> tuple[bool, ...]: ...

    def filename(self, response: httpx.Response, /) -> str:
        filename = response.headers.get("content-disposition")
        if filename is None:
            return self._DEFAULT_FILENAME
        result = re.search(r"filename=\"(.*?)\"", filename)
        return self._DEFAULT_FILENAME if result is None else result.group(1)


class ColabNotebookDownloader(BaseDownloader):
    _DEFAULT_FILENAME = "notebook.ipynb"

    @property
    def download_url(self) -> str:
        _, file_id = self.url.split("?", 1)[0].rsplit("/", 1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    def _infer_conditions(self, url: str) -> tuple[bool, ...]:
        return (_check_url_netloc(url, "colab.research.google.com"),)


class GithubFileDownloader(BaseDownloader):
    """
    Only capture `.py`, `.pdf` and `.ipynb`
    """

    @property
    def download_url(self) -> str:
        return self.url.replace("/blob", "/raw")

    def _infer_conditions(self, url: str) -> tuple[bool, ...]:
        return (
            _check_url_netloc(url, "github.com", "www.github.com"),
            any(i in url for i in ("/blob/", "/raw/")),
            url.endswith((".py", ".pdf", ".ipynb")),
        )

    def filename(self, response: httpx.Response, /) -> str:
        filename = super().filename(response)
        return (
            filename
            if filename != self._DEFAULT_FILENAME
            else self.url.rsplit("/", 1)[-1]
        )


class GoogleDriveFileDownloader(BaseDownloader):
    _DEFAULT_FILENAME = "drive_file.txt"

    @property
    def download_url(self) -> str:
        base_url, *_ = self.url.split("/d/", 1)
        _, file_id, _ = self.url.rsplit("/", 2)
        return f"{base_url}/export?id={file_id}"

    def _infer_conditions(self, url: str) -> tuple[bool, ...]:
        return (
            _check_url_netloc(url, "drive.google.com"),
            "/file/d/" in url,
        )


class GoogleDocsDownloader(GoogleDriveFileDownloader):
    _DEFAULT_FILENAME = "gdoc_file.txt"

    def _infer_conditions(self, url: str) -> tuple[bool, ...]:
        return (
            _check_url_netloc(url, "docs.google.com"),
            "/edit" in url,
        )


ALL_DOWNLOADERS: list[type[BaseDownloader]] = [
    ColabNotebookDownloader,
    GithubFileDownloader,
    GoogleDocsDownloader,
    GoogleDriveFileDownloader,
]


def infer_downloader(url: str) -> BaseDownloader:
    for downloader in ALL_DOWNLOADERS:
        try:
            return downloader(url).infer()
        except TypeError:
            continue
    else:
        raise TypeError(f"{url = } not inferred for any defined `BaseDownloader`")
