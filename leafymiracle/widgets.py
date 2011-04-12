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

from tw2.jit import SQLARadialGraph
from tw2.core.resources import JSSymbol

from leafymiracle import models

class LeafyGraph(SQLARadialGraph):
    id = 'leafy_graph'
    entities = [models.Root, models.Category, models.Group, models.Package]
    base_url = '/data'
    width = '1000'
    height = '650'
    depth = 2
    levelDistance = 150
    backgroundcolor = '#444444'
    alphabetize_relations = 24
    alphabetize_minimal = True
    show_attributes = False
    imply_relations = True
    auto_labels = False
    excluded_columns = ['group']
    deep_linking = True
    #transition = JSSymbol(src='$jit.Trans.Back.easeInOut')
    duration = 200
