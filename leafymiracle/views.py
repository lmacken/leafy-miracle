# Copyright (C) 2011 Luke Macken <lmacken@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pyramid.httpexceptions import HTTPFound
from tw2.jqplugins.ui.base import set_ui_theme_name
from widgets import LeafyGraph
from widgets import LeafyDialog
from widgets import LeafySearchbar

import leafymiracle.models
import sqlalchemy
import simplejson
import webob

def view_root(context, request):
    return HTTPFound(location='/1')

def view_model(context, request):
    # TODO -- we need a fedora jquery-ui theme sitting around.
    set_ui_theme_name('hot-sneaks')
    return {'item':context, 'project':'leafymiracle',
            'jitwidget': LeafyGraph(rootObject=context),
            'dialogwidget': LeafyDialog,
            'searchbarwidget': LeafySearchbar,
           }


def search(context, request):
    """ NOTE :: this is *not* the `pyramid` way of doing things.

    DB stuff should not happen in the 'view' but should instead happen..
    elsewhere?   Quick hack to make this work before submission.

    --Ralph
    """

    term = request.params['term']
    cats = request.params.get('cats', 'Category,Group,Package')

    # Don't do any search if the term is too short
    if len(term) < 2:
        return {'data':[]}

    attrs = {
        'Category' : {
            'search_on' : ['name', 'description'],
        },
        'Group' : {
            'search_on' : ['name', 'description'],
        },
        'Package' : {
            'search_on' : ['name'],
        }
    }
    srch = '%%%s%%' % term
    cats = cats.split(',')
    results = []

    for cat in cats:
        if not cat in attrs.keys():
            raise ValueError, "'%s' is a disallowed category." % cat
        cls = getattr(leafymiracle.models, cat)
        entries = cls.query.filter(sqlalchemy.or_(
            *[getattr(cls, srch_attr).like(srch)
              for srch_attr in attrs[cat]['search_on']]
        ))
        results += [[unicode(e), e.id, cat] for e in entries]

    data = {
        'data' : [
            {
                'label' : label,
                'value' : value,
                'category' : category }
            for label, value, category in results
        ]
    }
    resp = webob.Response(request=request, content_type="application/json")
    resp.body = simplejson.dumps(data)
    return resp
