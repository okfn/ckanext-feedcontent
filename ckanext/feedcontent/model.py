import logging
from datetime import datetime

import ckan.lib.munge as munge
import ckan.model as model
import ckan.model.meta  as meta
import ckan.model.types as types
import ckan.model.core  as core
import ckan.model.domain_object as domain_object
import sqlalchemy as sa
import sqlalchemy.engine.reflection as refl

log = logging.getLogger(__name__)

feed_table = None

class FeedException(Exception):
    pass

class Feed(domain_object.DomainObject):
    """
    This model represents a remote RSS/Atom feed
    """
    @classmethod
    def by_id(cls, id, autoflush=True):
        obj = Session.query(cls).autoflush(autoflush)\
              .filter_by(id=id).first()
        return obj


def setup():

    if feed_table is None:
        define_apps_tables()
        log.debug('Feed table defined in memory')

    if model.repo.are_tables_created():
        if not feed_table.exists():
            feed_table.create()
            log.debug('Feed table created')
        else:
            log.debug('Feed table already exists')
    else:
        log.debug('Feed table creation deferred')


feed_table = sa.Table('feed', meta.metadata,
    sa.Column('id',   sa.types.UnicodeText, primary_key=True, default=types.make_uuid),
    sa.Column('title', sa.types.UnicodeText, nullable=False),
    sa.Column('name', sa.types.UnicodeText, nullable=False, unique=True),
    sa.Column('url',  sa.types.UnicodeText, nullable=False),
    sa.Column('format',  sa.types.UnicodeText,  default=u"atom"),
    sa.Column('created', sa.types.DateTime, default=datetime.now),
    sa.Column('updated', sa.types.DateTime, default=datetime.now, onupdate=datetime.now),
    sa.Column('template', sa.types.UnicodeText, default=u""),
    sa.Column('html_entries', sa.types.Boolean, default=False),
    sa.Column('content', sa.types.UnicodeText, default=u""),
)

meta.mapper(Feed, feed_table)
