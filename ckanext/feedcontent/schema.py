from ckan.lib.navl.validators import ignore_missing, not_empty
from ckan.lib.navl.validators import empty, ignore, not_missing
from ckan.logic.schema import tag_string_convert

def feed_schema():
    return {
            'id': [ignore_missing, unicode],
            'title': [not_empty, unicode],
            'name': [ignore_missing, unicode],
            'url': [not_empty, unicode],
            'format': [ignore_missing, unicode],
            'created': [ignore_missing, unicode],
            'updated': [ignore_missing, unicode],
            'content': [ignore_missing, unicode],
        }

