
import ckan.logic as logic
import ckan.lib.navl.dictization_functions as df
import ckan.lib.base as base
import ckan.model as model
import ckan.lib.munge as m
import ckan.logic.action as action

from ckanext.feedcontent.schema import feed_schema
from ckanext.feedcontent.model import Feed

def _generate_name(title):
    name = m.munge_title_to_name(title).replace('_', '-')
    while '--' in name:
        name = name.replace('--', '-')
    like_q = u"%s%%" % name
    query = model.Session.query(Feed).filter(Feed.name.ilike(like_q)).limit(100)
    taken = [do.name for do in query]
    if name not in taken:
        return name
    else:
        counter = 1
        while counter < 101:
            if name+str(counter) not in taken:
                return name+str(counter)
            counter+=1

def get_feed(id):
    return model.Session.query(Feed).filter(Feed.name==id).first()

def get_feeds():
    """ Fetches all of the current Feeds """
    return model.Session.query(Feed).order_by(Feed.updated.desc()).all()


def create_feed(data_dict):
    data, errors = df.validate(data_dict, feed_schema())
    if errors:
        raise logic.ValidationError(errors, action.error_summary(errors))

    feed = Feed(
            name=_generate_name(data.get('title')),
            title=data.get('title'),
            url=data.get('url'),
            format=data.get('format'),
            updated=data.get('updated'),
            content=data.get('content')
        )
    feed.save()

    return feed


def edit_feed(feed, data_dict):
    data, errors = df.validate(data_dict, feed_schema())
    if errors:
        raise logic.ValidationError(errors, error_summary(errors))

    feed.title=data.get('title')
    feed.url=data.get('url')
    feed.format=data.get('format')
    feed.updated=data.get('updated')
    feed.content=data.get('content')
    feed.save()

    return feed
