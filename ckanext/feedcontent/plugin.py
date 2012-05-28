import logging
import ckan.plugins as p
import ckan.lib.helpers as h
import auth

log = logging.getLogger(__name__)


class FeedContent(p.SingletonPlugin):
    """
    Insert fragments into pages and the home page to
    allow users to add content from data feeds.
    """
    p.implements(p.IAuthFunctions)
    p.implements(p.IConfigurable)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IRoutes, inherit=True)

    def before_map(self, map):
        print "configuring map"
        ctllr = 'ckanext.feedcontent.controllers:FeedController'
        map.connect('feed_index', '/feeds', controller=ctllr, action='index')
        map.connect('feed_new', '/feeds/new', controller=ctllr, action='new')
        map.connect('feed_edit', '/feeds/edit/{id}', controller=ctllr, action='edit')
        map.connect('feed_delete', '/feeds/delete', controller=ctllr, action='delete')
        map.connect('feed_view', '/feeds/{id}', action='read')

        print h.url_for('feed_new')
        return map


    def configure(self, config):
        """
        Called upon CKAN setup, will pass current configuration dict
        to the plugin to read custom options.
        """
        pass

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')

    def get_auth_functions(self):
        return {
            'feed_create' : auth.feed_create,
            'feed_update' : auth.feed_update,
            'feed_delete' : auth.feed_delete,
            'feed_list'   : auth.feed_list,
        }


    @classmethod
    def feed_entry(cls):
        '''  Adds Disqus recent comments to the page. '''
        data = {"key": "value"}
        return p.toolkit.render_snippet('template.html', data)

    def get_helpers(self):
        return {'feed_entry' : self.feed_entry,}
