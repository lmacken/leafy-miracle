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

from sqlalchemy import Integer, Column, Unicode, UnicodeText, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

from kitchen.text.converters import to_unicode

DBSession = scoped_session(sessionmaker())
Base = declarative_base()
Base.query = DBSession.query_property()

# Icon Hack. Throw these in a config file.
icons = ['admin-tools', 'apps', 'authoring-and-publishing', 'base-system', 'base-x', 'clustering', 'content', 'core', 'desktops', 'development', 'development-tools', 'dial-up', 'directory-server', 'eclipse', 'editors', 'education', 'electronic-lab', 'engineering-and-scientific', 'font-design', 'fonts', 'games', 'gnome-desktop', 'gnome-software-development', 'graphical-internet', 'graphics', 'hardware-support', 'haskell', 'input-methods', 'java-development', 'java', 'kde-desktop', 'kde-software-development', 'language-support', 'legacy-fonts', 'legacy-network-server', 'lxde-desktop', 'mail-server', 'mysql', 'office', 'printing', 'ruby', 'server-cfg', 'servers', 'sound-and-video', 'sql-server', 'sugar-desktop', 'system-tools', 'text-internet', 'uncategorized', 'virtualization', 'window-managers', 'xfce-desktop', 'xfce-software-development', 'x-software-development']
icon_link = '<img src="http://lmacken.fedorapeople.org/comps-extras/%s.png"/ style="vertical-align:middle;"> %s'


class Root(Base):
    __tablename__ = 'root'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)

    categories = relationship("Category", backref="root")

    def __init__(self, name):
        self.name = to_unicode(name)

    def __unicode__(self):
        return icon_link % (self.name.lower(), self.name)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    category_id = Column(Unicode(255), unique=True)
    name = Column(Unicode(255), unique=True)
    description = Column(UnicodeText)
    root_id = Column(Integer, ForeignKey('root.id'))

    groups = relationship("Group", backref="category")

    def __init__(self, id, name, description):
        self.category_id = to_unicode(id)
        self.name = to_unicode(name)
        self.description = to_unicode(description)

    def __unicode__(self):
        if self.category_id in icons:
            return icon_link % (self.category_id, self.name)
        return self.name


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    group_id = Column(Unicode(255), unique=True)
    name = Column(Unicode(255), unique=True)
    description = Column(UnicodeText)
    category_id = Column(Integer, ForeignKey('categories.id'))

    packages = relationship("Package", backref="group")

    def __init__(self, id, name, description):
        self.group_id = to_unicode(id)
        self.name = to_unicode(name)
        self.description = to_unicode(description)

    def __unicode__(self):
        if self.group_id in icons:
            return icon_link % (self.group_id, self.name)
        return self.name


class Package(Base):
    __tablename__ = 'packages'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)

    group_id = Column(Integer, ForeignKey('groups.id'))

    def __init__(self, name):
        self.name = to_unicode(name)

    def __unicode__(self):
        return self.name

    def __jit_data__(self):
        return {
            'hover_html' : """
            <h2>{name}</h2>
            <li><img src="https://admin.fedoraproject.org/community/images/16_pkgdb.png"/><a href="https://admin.fedoraproject.org/community/?package={name}#package_maintenance/details/downloads" target="_blank">Downloads</a></li>
            <li><img src="https://admin.fedoraproject.org/community/images/16_koji.png"/><a href="http://koji.fedoraproject.org/koji/search?terms={name}&type=package&match=exact" target="_blank">Builds</a></li>
            <li><img src="https://admin.fedoraproject.org/community/images/16_bodhi.png"/><a href="https://admin.fedoraproject.org/updates/{name}" target="_blank">Updates</a></li>
            <li><img src="https://admin.fedoraproject.org/community/images/16_bugs.png"/><a href="https://admin.fedoraproject.org/pkgdb/acls/bugs/{name}" target="_blank">Bugs</a></li>
            <li><img src="https://admin.fedoraproject.org/community/images/16_sources.png"/><a href="http://pkgs.fedoraproject.org/gitweb/?p={name}.git" target="_blank">Source</a></li>
            <li><img src="https://admin.fedoraproject.org/community/images/16_pkgdb.png"/><a href="https://admin.fedoraproject.org/pkgdb/acls/name/{name}" target="_blank">Package Info</a></li>
            </ul>
            """.format(**self.__dict__)
        }

dependencies_mapping = Table(
    'packages_dependencies_mapping', Base.metadata,
    Column('depender_id', Integer,
           ForeignKey('packages.id'), primary_key=True),
    Column('dependee_id', Integer,
           ForeignKey('packages.id'), primary_key=True))

Package.__mapper__.add_property('dependencies', relationship(
    Package,
    primaryjoin=Package.id==dependencies_mapping.c.dependee_id,
    secondaryjoin=dependencies_mapping.c.depender_id==Package.id,
    secondary=dependencies_mapping,
    doc="List of this packages' dependencies!",
))



def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
