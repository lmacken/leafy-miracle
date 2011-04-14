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

from sqlalchemy.orm.exc import NoResultFound
from models import DBSession, Root, initialize_sql

import models
import sqlalchemy

class SearchHandler(object):
    def search(self, term, cats):
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
            cls = getattr(models, cat)
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
        return data

class MyApp(object):
    __name__ = None
    __parent__ = None

    def __getitem__(self, key):
        session = DBSession()
        if key == 'search':
            handler = SearchHandler()
            handler.__name__ = key
            handler.__parent__ = self
            return handler

        try:
            id = int(key)
        except (ValueError, TypeError):
            raise KeyError(key)

        query = session.query(Root).filter_by(id=id)

        try:
            item = query.one()
            item.__parent__ = self
            item.__name__ = key
            return item
        except NoResultFound:
            raise KeyError(key)

    def get(self, key, default=None):
        try:
            item = self.__getitem__(key)
        except KeyError:
            item = default
        return item

    def __iter__(self):
        session= DBSession()
        query = session.query(Root)
        return iter(query)

root = MyApp()

def default_get_root(request):
    return root

def appmaker(engine):
    initialize_sql(engine)
    return default_get_root
