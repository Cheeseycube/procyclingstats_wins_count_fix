from typing import Any, Dict, Literal

from requests_html import HTML, HTMLSession


class Scraper:
    base_url: Literal["https://www.procyclingstats.com/"] = \
        "https://www.procyclingstats.com/"

    def __init__(self, url: str, print_request_url: bool = False) -> None:
        """
        Used as base class for scraping classes

        :param url: URL to be parsed from
        :param print_request_url: whether to print URL when making request, 
        defaults to True
        """
        # .html and .url are going to be overridden by subclasses
        self.url: str = self._format_url(url)
        self.print_request_url: bool = print_request_url
        self.html: HTML = self._request_html()
        self.content: Dict[str, Any] = {}

    def __repr__(self) -> str:
        """:return: `self.url`"""
        return self.url

    def _format_url(self, url: str) -> str:
        """
        Makes full URL from given url (adds `self.base_url` to URL if needed)

        :param url: URL to format
        :return: full URL
        """
        if "https" not in url:
            if url[-1] == "/":
                url = self.base_url + url[:-1]
            else:
                url = self.base_url + url
        return url

    def _cut_base_url(self) -> str:
        """
        Makes relative URL from absolute url (cuts `self.base_url` from URL)

        :return: relative URL
        """
        return "/".join(self.url.split("/")[3:])

    def _request_html(self) -> HTML:
        """
        Makes request to `self.url` and returns it's HTML

        :raises ValueError: if URL isn't valid (after making request)
        :return: HTML obtained from `self.url`
        """
        session = HTMLSession()
        if self.print_request_url:
            print(self.url)
        html = session.get(self.url).html
        if html.find(".page-title > .main > h1")[0].text == "Page not found":
            raise ValueError(f"Invalid URL: {self.url}")
        return html

    def update_html(self) -> None:
        """
        Calls request to `self.url` using `RequestWrapper._request_html` and
        updates `self.html` to returned HTML
        """
        self.html = self._request_html()