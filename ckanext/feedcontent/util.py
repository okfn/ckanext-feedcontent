
import re
import requests
import feedparser
import ckanext.feedcontent.model as model

def normalised_entry(entry,short_size):
    fields = ["title", "link", "description", "author", "pubDate"]
    e = {}
    for f in fields:
        e[f] = entry.get(f, '')
    e['short_description'] = e['description'][0:short_size]
    if len(e['description']) > short_size:
        e['short_description'] = e['short_description'] + "..."
    return e


def find_entry(feed_string, title, short_size):
    feed = feedparser.parse(feed_string)
    if feed.bozo:
        raise model.FeedException("Feed not valid")

    r = re.compile(title)
    for item in feed['items']:
        if r.match(item.title):
            return normalised_entry(item,short_size)
    return None


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