import requests
from typing import List, Dict, Any

try:
    from bs4 import BeautifulSoup
except ImportError:
    pass


class Reddit:
    def __init__(self, **kwargs):
        """ """
        self.subreddit = kwargs.get("subreddit", "anarchism")
        self.interval = kwargs.get("interval", "week")
        self.content = []
        self.rss = None
        self._subreddit_atom_feed = (
            f"https://www.reddit.com/r/{self.subreddit}/top.rss?t={self.interval}"
        )
        self.headers = kwargs.get(
            "headers",
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            },
        )
        if self._subreddit_atom_feed:
            self.get()
        if self.rss:
            self.parse()

    def get(self) -> None:
        """Wrapper for requests GET method that can forge a convincing header for requests of a sub-reddit's ATOM feed url"""
        try:
            self.rss = requests.get(self._subreddit_atom_feed, headers=self.headers)
            if self.rss.status_code != 200:
                raise RuntimeError(
                    f"http GET request failed for url: {self._subreddit_atom_feed}"
                )
            self.rss = self.rss.content
            self.rss = BeautifulSoup(self.rss, "xml")
        except Exception as e:
            raise e

    def parse(self) -> None:
        """Parses an ATOM feed into a list of dictionaries with 'link' and 'title' key/value pairs"""
        if self.rss:
            try:
                self.content = [
                    BeautifulSoup(c.text, "html") for c in self.rss.find_all("content")
                ]
                self.content = [
                    {"link": c.find("a")["href"], "title": c.find("img")["title"]}
                    for c in self.content
                    if c.find("img") and c.find("a")
                ]
            except Exception as e:
                raise e
