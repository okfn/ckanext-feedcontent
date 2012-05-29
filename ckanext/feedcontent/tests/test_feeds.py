import nose.tools as tools
import ckan.lib.helpers as h
import ckan.tests.functional.base as base

assert_equal = tools.assert_equal

class TestFeeds(base.FunctionalTestCase):

    @classmethod
    def setup_class(cls):
        pass

    def test_missing_view(self):
        offset = h.url_for(controller='ckanext.feedcontent.controllers:FeedController', action='read', id="test")
        res = self.app.get(offset, status=404)
        #status=200, extra_environ={'REMOTE_USER': 'russianfan'}
        #assert '<dct:title>A Wonderful Story</dct:title>' in res, res


