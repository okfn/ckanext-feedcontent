import logging
from datetime import datetime

import ckan.lib.munge as munge
import ckan.model as model
import ckan.model.meta  as meta
import ckan.model.types as types
import ckan.model.core  as core
import ckan.model.domain_object as domain_object

log = logging.getLogger(__name__)

remotefeed_table = None


class RemoteFeed(DomainObject):
    """
    This model represents a remote RSS/Atom feed
    """
    @classmethod
    def by_id(cls, id, autoflush=True):
        obj = Session.query(cls).autoflush(autoflush)\
              .filter_by(id=id).first()
        return obj


def setup():

    if remotefeed_table is None:
        define_apps_tables()
        log.debug('Apps tables defined in memory')

    if model.repo.are_tables_created():
        if not remotefeed_table.exists():
            remotefeed_table.create()
            log.debug('Apps tables created')
        else:
            log.debug('Apps tables already exist')
            # Check if existing tables need to be updated
            inspector = Inspector.from_engine(meta.engine)
            columns = inspector.get_columns('application_tag')
            if not 'id' in [column['name'] for column in columns]:
                log.debug('Apps tables need to be updated')
                migrate_v2()
    else:
        log.debug('Apps table creation deferred')

def _generate_name(cls, title):
    name = munge.munge_title_to_name(title).replace('_', '-')
    while '--' in name:
        name = name.replace('--', '-')
    like_q = u"%s%%" % name
    query = model.Session.query(cls).filter(cls.name.ilike(like_q)).limit(100)
    taken = [do.name for do in query]
    if name not in taken:
        return name
    else:
        counter = 1
        while counter < 101:
            if name+str(counter) not in taken:
                return name+str(counter)
            counter+=1


def define_apps_tables():
    global remotefeed_table

    remotefeed_table = Table('application', metadata,
        Column('id',   types.UnicodeText, primary_key=True, default=types.make_uuid),
        Column('title', types.UnicodeText, nullable=False, unique=True),
        Column('name', types.UnicodeText, nullable=False, unique=True),
        Column('url',  types.UnicodeText, nullable=False),
        Column('format',  types.UnicodeText,  default="atom"),
        Column('created', types.DateTime, default=datetime.now),
        Column('updated', types.DateTime, default=datetime.now, onupdate=datetime.now),
        Column('content', types.UnicodeTest, default=""),
    )

    mapper(RemoteFeed, remotefeed_table)
