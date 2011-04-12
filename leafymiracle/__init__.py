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

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from leafymiracle.resources import appmaker
from leafymiracle.widgets import LeafyGraph

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    print settings
    engine = engine_from_config(settings, 'sqlalchemy.')
    get_root = appmaker(engine)
    config = Configurator(settings=settings, root_factory=get_root)
    config.add_view('leafymiracle.views.view_root', 
                    context='leafymiracle.resources.MyApp', 
                    renderer="templates/root.pt")
    config.add_view('leafymiracle.views.view_model',
                    context='leafymiracle.models.Root',
                    renderer="templates/model.pt")
    config.add_static_view(name='static', path='static')

    # Create the data view for our tw2.jit.SQLARadialGraph
    jit_view = lambda context, request: LeafyGraph.request(request)
    config.add_route('data', '/data', view=jit_view, xhr=True)

    return config.make_wsgi_app()
