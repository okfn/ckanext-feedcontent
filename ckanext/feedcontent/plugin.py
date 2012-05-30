import logging
import ckan.plugins as p
import ckan.lib.helpers as h
import auth

from ckanext.feedcontent.model import setup

log = logging.getLogger(__name__)


class FeedContent(p.SingletonPlugin):
    """
    This plugin configures a local controller to be used for the management
    of feeds within the system.

    By creating a new database model to hold this information, and accessing
    it via the FeedController it is possible to manage the feeds that the
    extension 'knows' about.  By providing template helpers to pull this data
    onto a particular template.
    """
    p.implements(p.IAuthFunctions)
    p.implements(p.IConfigurable)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IRoutes, inherit=True)

    default_snippet = None

    def before_map(self, map):
        """  Creates the routing for feed URLs to map to the FeedController """
        ctllr = 'ckanext.feedcontent.controllers:FeedController'
        map.connect('feed_index', '/feed', controller=ctllr, action='index')
        map.connect('feed_new', '/feed/new', controller=ctllr, action='new')
        map.connect('feed_edit', '/feed/edit/{id}', controller=ctllr, action='edit')
        map.connect('feed_delete', '/feed/{id}/delete', controller=ctllr, action='delete')
        map.connect('feed_update', '/feed/{id}/update', controller=ctllr, action='update')
        map.connect('feed_view', '/feed/{id}', controller=ctllr, action='read')
        return map


    def configure(self, config):
        """
        Called upon CKAN setup, and creates (or checks) the appropriate
        database tables are created.
        """
        setup()

        # If a default snippet is configured then we should use that
        # otherwise we will use a default.
        FeedContent.default_snippet = config.get('feeds.default.snippet',
                                                 'snippets/default.html')


    def update_config(self, config):
        """ Updates the configuration with the template folder """
        p.toolkit.add_template_directory(config, 'templates/main')

        # TODO: Only add example if we have a config option set to
        # use it.

    def get_auth_functions(self):
        """ Provides new authorisation functions specific to feed
        management """
        return {
            'feed_create' : auth.feed_create,
            'feed_update' : auth.feed_update,
            'feed_delete' : auth.feed_delete,
            'feed_list'   : auth.feed_list,
            'feed_get'    : auth.feed_get
        }


    @classmethod
    def feed_entry(cls, name, title):
        data = {"key": "value"}
        return p.toolkit.render_snippet(default_snippet, data)

    def get_helpers(self):
        return {'feed_entry' : self.feed_entry,}
