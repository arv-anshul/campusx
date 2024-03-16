from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING
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

    def _request(self, url: str, client: httpx.Client) -> bytes:
        res = client.get(url)
        if res.status_code == 200:
            return res.content
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

    def download(self, client: httpx.Client) -> bytes:
        return self._request(self.download_url, client)

    @abstractmethod
    def _infer_conditions(self, url: str) -> tuple[bool, ...]: ...

    @property
    @abstractmethod
    def filename(self) -> str:
        """
        Decide the filename for the downloaded bytes.

        🤯 TODO: Write a function to infer files extension.

        Returns filename and file's extension.
        """
        ...


class ColabNotebookDownloader(BaseDownloader):
    @property
    def download_url(self) -> str:
        _, file_id = self.url.split("?", 1)[0].rsplit("/", 1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    def _infer_conditions(self, url: str) -> tuple[bool, ...]:
        return (_check_url_netloc(url, "colab.research.google.com"),)

    @property
    def filename(self) -> str:
        return "notebook.ipynb"


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

    @property
    def filename(self) -> str:
        ext = self.url.rsplit(".", 1)[-1]
        filename = {
            "py": "python",
            "pdf": "document",
            "ipynb": "notebook",
        }
        return filename.get(ext, "github_file") + f".{ext}"


class GoogleDriveFileDownloader(BaseDownloader):
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

    @property
    def filename(self) -> str:
        return "drive_file.txt"


class GoogleDocsDownloader(GoogleDriveFileDownloader):
    def _infer_conditions(self, url: str) -> tuple[bool, ...]:
        return (
            _check_url_netloc(url, "docs.google.com"),
            "/edit" in url,
        )

    @property
    def filename(self) -> str:
        filename = self.url.split(".com/")[-1].split("/")[0]
        ext = {
            "spreadsheets": ".xlsx",
            "presentation": ".pptx",
            "document": ".docx",
        }
        return f"drive_{filename}" + ext.get(filename, ".txt")


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
