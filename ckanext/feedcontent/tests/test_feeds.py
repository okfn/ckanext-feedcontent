import sys
import ckan
import ckan.model as model
import ckan.lib.helpers as h
import ckan.tests.functional.base as base

import nose.tools as tools

import ckanext.feedcontent.model as feedmodel

assert_equal = tools.assert_equal

class TestFeeds(base.FunctionalTestCase):

    controller_path = 'ckanext.feedcontent.controllers:FeedController'

    @classmethod
    def setup_class(cls):
        feedmodel.setup()

        ckan.model.repo.rebuild_db()
        ckan.tests.CreateTestData.create()

        cls.user = model.User.by_name(u'testsysadmin')
        cls.extra_environ = {'Authorization':str(cls.user.apikey)}


    def test_missing_view(self):
        offset = h.url_for(controller=TestFeeds.controller_path,
                           action='read',
                           id="test")
        res = self.app.get(offset, status=404, extra_environ=TestFeeds.extra_environ)
        #status=200, extra_environ=
        #assert '<dct:title>A Wonderful Story</dct:title>' in res, res

    def test_new_feed(self, name='test-new-feed'):

        offset = h.url_for(controller=TestFeeds.controller_path,
                           action='new')
        res = self.app.get(offset, status=200,
                           extra_environ={"REMOTE_USER": "testsysadmin"})
        assert 'URL' in res, "URL missing in response text"
        assert 'Title' in res, "Title missing in response text"

        data = {
            "title": name,
            "url": u"http://ckan.org/feed/",
            "template": u""
        }
        res = self.app.post(offset, params=data,
                            status=[200,302],
                            extra_environ={"REMOTE_USER": "testsysadmin"})

        offset = h.url_for(controller=TestFeeds.controller_path,
                           action='read',
                           id=name)
        res = self.app.get(offset, status=200, extra_environ={"REMOTE_USER": "testsysadmin"})


    def test_delete_fail(self):
        self.test_new_feed('test-delete-fail')
        offset = h.url_for(controller=TestFeeds.controller_path,
                           action='read',
                           id='test-delete-fail')
        res = self.app.get(offset, status=401, extra_environ={'REMOTE_USER': 'russianfan'})

    def test_delete_ok(self):
        self.test_new_feed('test-delete-ok')
        offset = h.url_for(controller=TestFeeds.controller_path,
                           action='delete',
                           id='test-delete-ok')
        res = self.app.get(offset, status=[200,302], extra_environ=self.extra_environ)

    def test_new_fail(self, name='test-new-feed'):
        offset = h.url_for(controller=TestFeeds.controller_path,
                           action='new')
        res = self.app.get(offset, status=401,
                           extra_environ={'REMOTE_USER': 'russianfan'})




