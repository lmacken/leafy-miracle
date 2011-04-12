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
        yumobj = yum.YumBase()
        yumobj.setCacheDir()
        for package in session.query(Package).all():
            deps = yumobj.pkgSack.searchNevra(name=package.name)[0]
            deps_d = pkg.findDeps([pkg])
            deps = [tup[0] for tup in deps_d[deps_d.keys()[0]].keys()]

            for dep in deps:
                dep_as_package = session.query(Package)\
                        .filter_by(name=dep).one()
                if dep_as_package not in package.dependencies:
                    package.dependencies.append(dep_as_package)



    session.commit()

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
