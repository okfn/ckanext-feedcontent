import urllib2

from pylons.i18n import _

import ckan.lib.navl.dictization_functions as df
import ckan.lib.helpers as h, json
import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model
import ckanext.feedcontent.model as feedmodels
import ckanext.feedcontent.logic as feedlogic
import ckanext.feedcontent.util as util
c = base.c

class FeedController(base.BaseController):

    controller_path = 'ckanext.feedcontent.controllers:FeedController'

    def index(self):
        self._check_auth("feed_list")

        c.feeds = feedlogic.get_feeds()
        return base.render("feeds/index.html")

    def read(self, id):
        self._check_auth("feed_get")

        c.feed = feedlogic.get_feed(id)
        if not c.feed:
            base.abort(404, _("Feed {name} does not exist".format(name=id)))

        return base.render("feeds/read.html")

    def new(self):
        self._check_auth("feed_create")
        data, errors, error_summary = {}, {}, {}

        if base.request.method == "POST":
            try:
                dd = logic.clean_dict(
                                df.unflatten(
                                    logic.tuplize_dict(
                                        logic.parse_params(base.request.params)
                                    )
                                )
                            )
                feed = feedlogic.create_feed(dd)
                h.redirect_to( controller=self.controller_path,
                               action='read',
                               id=feed.name)
            except feedmodels.FeedException:
                error = {'url': [u'Failed to load feed']}
                error_summary = {u'URL': u'Failed to load feed'}
                data = dd
            except df.DataError:
                base.abort(400, _(u'Integrity Error'))
            except logic.ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary

        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}
        c.action = 'create'
        c.form = base.render("feeds/edit_form.html", extra_vars=vars)
        return base.render("feeds/new.html")

    def update(self, id):
        self._check_auth("feed_update")

        feed = feedlogic.get_feed(id)
        if not feed:
            base.abort(404, _("Feed {name} does not exist".format(name=id)))

        feedlogic.update_feed(feed)
        h.redirect_to( controller=self.controller_path,
                       action='read',
                       id=feed.name)



    def edit(self, id):
        self._check_auth("feed_update")

        data, errors, error_summary = {}, {}, {}
        c.feed = feedlogic.get_feed(id)
        if not c.feed:
            base.abort(404, _("Feed {name} does not exist".format(name=id)))

        if base.request.method == "POST":
            try:
                data = logic.clean_dict(
                        df.unflatten(
                            logic.tuplize_dict(
                                logic.parse_params(base.request.params)
                        )))
                feed = feedlogic.edit_feed(c.feed, data)
                h.redirect_to( controller=self.controller_path,
                               action='read',
                               id=feed.name)
            except feedmodels.FeedException:
                error = {'url': [u'Failed to load feed']}
                error_summary = {u'URL': u'Failed to load feed'}
                data = c.feed.as_dict()
            except df.DataError:
                base.abort(400, _(u'Integrity Error'))
            except logic.ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
        else:
            data = c.feed.as_dict()

        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}
        c.action = 'edit'
        c.form = base.render("feeds/edit_form.html", extra_vars=vars)
        return base.render("feeds/edit.html")

    def delete(self, id):
        self._check_auth("feed_delete")
        feed = feedlogic.get_feed(id)
        if not feed:
            base.abort(404, _("Feed {name} does not exist".format(name=id)))
        feedlogic.delete_feed(feed)

        h.redirect_to( controller=self.controller_path,
                       action='index')

    def _check_auth(self, name):
        ctx = {"user": c.user, 'model':model, 'session': model.Session}
        try:
            logic.check_access(name, ctx)
        except logic.NotAuthorized, e:
            base.abort(401, _('Not authorized'))
