import logging
import ckan.plugins as p
import ckan.lib.helpers as h

import pylons.i18n as i18n

import ckanext.feedcontent.auth as auth
import ckanext.feedcontent.model as feedmodel
import ckanext.feedcontent.logic as feedlogic
import ckanext.feedcontent.util as util

log = logging.getLogger(__name__)

_ = i18n._

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
    short_description_size = 200

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
        feedmodel.setup()

        # If a default snippet is configured then we should use that
        # otherwise we will use a default.
        FeedContent.default_snippet = config.get('ckan.feeds.default.snippet',
                                                 'snippets/default.html')
        FeedContent.short_description_size = \
                        config.get('ckan.feeds.short_description.size', 200)

    def update_config(self, config):
        """ Updates the configuration with the template folder """
        p.toolkit.add_template_directory(config, 'templates/main')
        if config.get('ckan.feed.demo', False):
            p.toolkit.add_template_directory(config, 'templates/example')

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
        """
        Template helper which when given the name of a feed and the title
        for a particular entry will render the entry into the snippet for
        that feed. If the feed has no snippet it will use the one from
        the config file, and failing that will use default default.

        The title supplied be a regular expression.  Note that because a
        regex check is done then 'This is a long title here' will match
        a title parameter of 'This is a long title' unless ^ and & are
        used to bind the title to start/end of line.
        """
        data = {'error':'', 'entry': '', 'html_entries': False}
        feed = feedlogic.get_feed(name)
        template = FeedContent.default_snippet
        if feed:
            data['html_entries'] = feed.html_entries
            template = feed.template or FeedContent.default_snippet
            try:
                data['entry'] = util.find_entry(feed.content,
                                                title,
                                                FeedContent.short_description_size)
            except feedmodel.FeedException as fe:
                data['error'] = str(fe)
        else:
            data['error'] = _("Feed {name} not found".format(name=name))
        return p.toolkit.render_snippet(template, data)

    def get_helpers(self):
        return {'feed_entry' : FeedContent.feed_entry}
