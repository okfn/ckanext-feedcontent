import logging

import ckan.plugins as p

log = logging.getLogger(__name__)


class FeedContent(p.SingletonPlugin):
    """
    Insert javascript fragments into package pages and the home page to
    allow users to view and create comments on any package.
    """
    p.implements(p.IConfigurable)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def configure(self, config):
        """
        Called upon CKAN setup, will pass current configuration dict
        to the plugin to read custom options.
        """
        pass

    def update_config(self, config):
        # add template directory to template path
        p.toolkit.add_template_directory(config, 'templates')

    @classmethod
    def disqus_recent(cls, num_comments=5):
        '''  Adds Disqus recent comments to the page. '''
        data = {'disqus_shortname': "X",
                'disqus_num_comments' : num_comments,}
        return p.toolkit.render_snippet('recent.html', data)

    def get_helpers(self):
        return {'recent' : self.disqus_recent,}
