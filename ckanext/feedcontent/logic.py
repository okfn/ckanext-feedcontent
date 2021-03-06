from pylons.i18n import _

import ckan.logic as logic
import ckan.lib.navl.dictization_functions as df
import ckan.lib.base as base
import ckan.model as model
import ckan.lib.munge as m
import ckan.logic.action as action

import ckanext.feedcontent.schema as fs
import ckanext.feedcontent.model as feedmodels
import ckanext.feedcontent.util as util

def _generate_name(title):
    """
    Generates a valid slug for the specified title. It does this by checking
    the database for an existing match, and if it exsits then it tries again
    with a number appended.
    """
    name = m.munge_title_to_name(title).replace('_', '-')
    while '--' in name:
        name = name.replace('--', '-')
    like_q = u"%s%%" % name
    query = model.Session.query(feedmodels.Feed).\
                filter(feedmodels.Feed.name.ilike(like_q)).limit(100)
    taken = [do.name for do in query]
    if name not in taken:
        return name
    else:
        counter = 1
        while counter < 101:
            if name+str(counter) not in taken:
                return name+str(counter)
            counter+=1

def get_feed(name):
    """ Fetches a single feed object by name """
    return model.Session.query(feedmodels.Feed).\
                filter(feedmodels.Feed.name==name).first()

def get_feeds():
    """ Fetches all of the current Feeds """
    return model.Session.query(feedmodels.Feed).\
                order_by(feedmodels.Feed.updated.desc()).all()


def create_feed(data_dict):
    """ Creates a new feed after validating the information provided,
    and then validates the data held at the specified URL is in fact a
    feed """
    data, errors = df.validate(data_dict, fs.feed_schema())
    if errors:
        raise logic.ValidationError(errors, action.error_summary(errors))

    ok,format,content = util.validate_feed(data.get('url'))
    if not ok:
        raise feedmodels.FeedException(_("Unable to fetch feed"))

    feed = feedmodels.Feed(
            name = _generate_name(data.get('title')),
            title = data.get('title'),
            url = data.get('url'),
            format = format,
            updated = data.get('updated'),
            content = content,
            template = data.get('template'),
            html_entries = data.get('html_entries')
        )
    feed.save()

    return feed

def update_feed(feed):
    """
    Fetches the data for the feed and updates the object in the
    database.
    """
    feed.content = unicode(util.fetch_feed_content(feed.url))
    feed.save()


def delete_feed(feed):
    """ Deletes the specified feed """
    model.Session.delete(feed)
    model.Session.commit()

def edit_feed(feed, data_dict):
    """
    Edits the specified feed with the dictionary of data provided,
    validating both the data and the request URL (as with create_feed)
    """
    data, errors = df.validate(data_dict, fs.feed_schema())
    if errors:
        raise logic.ValidationError(errors, error_summary(errors))

    ok,format, content = util.validate_feed(data.get('url'))
    if not ok:
        raise feedmodels.FeedException(_("Unable to fetch feed"))

    # If URL is different use new content, but if using existing
    # content replace it if still empty
    if feed.url != data.get('url'):
        feed.content = content
    else:
        feed.content = data.get('content', None) or content

    feed.title = data.get('title')
    feed.url = data.get('url')
    feed.template = data.get('template')
    feed.format = format
    feed.updated = data.get('updated')
    feed.html_entries = data.get('html_entries')
    feed.save()

    return feed
