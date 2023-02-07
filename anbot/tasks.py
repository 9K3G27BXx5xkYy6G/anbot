import hashlib
from typing import Dict, List, Any
from anbot.reddit import Reddit as RedditBackend

sha1 = lambda x: hashlib.sha1(str(x).encode("utf-8")).hexdigest()


def cache_reddit_top_post(
    hash: bool = True, timeframe: str = "weekly"
) -> Dict[str, str]:
    top_post = {}
    try:
        top_post = RedditBackend(timeframe=timeframe)
        if top_post.content:
            top_post = top_post_weekly.content[0]
        else:
            top_post = {}
    except Exception:
        pass
    if hash:
        top_post["hash"] = sha1(top_post["title"])
    return top_post
