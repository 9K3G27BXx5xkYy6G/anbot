import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    pass


class ANews:
    def __init__(self, **kwargs):
        """ """
        self.content = []
        self.rss = None
        self._anews_rss_feed = "https://anarchistnews.org/rss.xml"
        self.headers = kwargs.get(
            "headers",
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            },
        )
        if self._anews_rss_feed:
            self.get()
        if self.rss:
            self.parse()

    def get(self) -> None:
        """Wrapper for requests GET method that can forge a convincing header for requests of a RSS feed url"""
        try:
            self.rss = requests.get(self._anews_rss_feed, headers=self.headers)
            if self.rss.status_code != 200:
                raise RuntimeError(
                    f"http GET request failed for url: {self._anews_rss_feed}"
                )
            self.rss = self.rss.content
            self.rss = BeautifulSoup(self.rss, "xml")
        except Exception as e:
            raise e

    def parse(self) -> None:
        """Parses an RSS feed into a list of dictionaries with 'link' and 'title' key/value pairs"""
        if self.rss:
            try:
                self.content = [
                    BeautifulSoup(c.text, "html") for c in self.rss.find_all("item")
                ]
                self.content = [
                    {"link": c.find("link"), "title": c.find("title")}
                    for c in self.content
                    if c.find("link") and c.find("title")
                ]
            except Exception as e:
                raise e
