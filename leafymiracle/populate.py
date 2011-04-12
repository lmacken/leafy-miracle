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

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from kitchen.text.converters import to_unicode

from models import Root, Category, Group, Package, DBSession, initialize_sql

from yum import YumBase
yumobj = YumBase()
yumobj.setCacheDir()

def populate(comps='comps-f16', do_dependencies=True):
    from yum.comps import Comps

    session = DBSession()

    c = Comps()
    c.add('comps/%s.xml' % comps)

    for group in c.groups:
        g = Group(id=group.groupid, name=group.name, description=group.description)
        session.add(g)

        for package in group.packages:
            p = session.query(Package).filter_by(name=to_unicode(package)).first()
            if not p:
                p = Package(name=package)
                session.add(p)
            p.group = g

        session.flush()

    root = Root(name=u'Fedora')
    session.add(root)
    session.flush()

    for category in c.categories:
        c = Category(id=category.categoryid, name=category.name,
                     description=category.description)
        session.add(c)
        root.categories.append(c)
        for group in category.groups:
            g = session.query(Group).filter_by(group_id=to_unicode(group)).first()
            if not g:
                print "Cannot find group: %s" % group
            else:
                g.category = c

        session.flush()

    if do_dependencies:
        for package in session.query(Package).all():
            add_dependencies(package, session)

    session.commit()

def add_dependencies(package, session):
    try:
        pkg = yumobj.pkgSack.searchNevra(name=package.name)[0]
        deps_d = yumobj.findDeps([pkg])
        deps = [tup[0] for tup in deps_d[deps_d.keys()[0]].keys()]

        for dep in deps:
            base_query = session.query(Package).filter_by(name=dep)
            if base_query.count() == 0:
                _new_package = Package(name=dep)
                session.add(_new_package)
                session.flush()
                add_dependencies(_new_package, session)

            dep_as_package = base_query.one()

            if dep_as_package not in package.dependencies:
                package.dependencies.append(dep_as_package)

        print "package: %s has (%i/%i) deps" % (
            package.name, len(package.dependencies), len(deps))
        session.flush()
    except Exception as e:
        # TODO -- figure out why some stuff breaks here.
        pass

def build_comps():
    import subprocess
    subprocess.call('git clone git://git.fedorahosted.org/comps.git', shell=True)
    subprocess.call('make comps-f16.xml', cwd='comps', shell=True)


if __name__ == '__main__':
    print "Initializing LeafyMiracle..."
    engine = create_engine('sqlite:///leafymiracle.db')
    initialize_sql(engine)
    build_comps()
    try:
        populate()
        print "Complete!"
    except IntegrityError, e:
        DBSession.rollback()
