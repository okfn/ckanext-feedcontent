

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

    return True, 'atom', content


def fetch_feed_content(url):
    """
        Fetches the content from the supplied url
    """
    import urllib2
    try:
        content = urllib2.urlopen(url).read()
    except:
        content = ''
    return content