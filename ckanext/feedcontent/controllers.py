import urllib2

from pylons.i18n import _

import ckan.lib.helpers as h, json
import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model

c = base.c

class FeedController(base.BaseController):

    def index(self):
        self._check_auth("feed_list")
        c.feed = None
        return base.render("feeds/admin.html")

    def read(self):

        self._check_auth("feed_view")
        return base.render("feeds/read.html")

    def new(self):

        self._check_auth("feed_create")
        c.form = base.render("feeds/edit_form.html")
        return base.render("feeds/new.html")

    def edit(self):

        self._check_auth("feed_update")
        c.form = base.render("feeds/edit_form.html")
        return base.render("feeds/edit.html")

    def delete(self):
        # get context
        self._check_auth("feed_delete")
        h.redirect_to("feed_admin")

    def _check_auth(self, name):
        ctx = {"user": c.user, 'model':model, 'session': model.Session}
        try:
            logic.check_access(name, ctx)
        except logic.NotAuthorized, e:
            base.abort(401, _('Not authorized'))
