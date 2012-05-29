import requests
import feedparser

def validate_feed(url):
    """
        Validates the feed supposedly at url by fetching it
        and checking that we can determine its type

        Returns the success, type and content
            e.g. True, 'atom', 'content....'
            or False, None, None
    """
    content = fetch_feed_content(url)
    if not content:
        return False, None, None

    feed = feedparser.parse(content)
    if feed.bozo:
        return False, None, None

    return True, feed.version, content


def fetch_feed_content(url):
    """
        Fetches the content from the supplied url
    """
    r = requests.get(url)
    if r.status_code == 200:
        return r.content
    return ""