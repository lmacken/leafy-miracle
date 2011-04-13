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
from tw2.jqplugins.ui import DialogWidget

from tw2.core.resources import JSSymbol

import docutils.examples

from leafymiracle import models

# Using mihmo's mathematically nice colors for fedora.
# http://mihmo.livejournal.com/37350.html
triads = ["#3c6eb4", "#b53c6e", "#6eb53c"]
triads_dark = ["#294172", "#732942", "#427329"]


class LeafyGraph(SQLARadialGraph):
    id = 'leafy_graph'
    entities = [models.Root, models.Category, models.Group, models.Package]
    base_url = '/data'
    width = '1000'
    height = '750'
    depth = 2
    levelDistance = 150
    alphabetize_relations = 24
    alphabetize_minimal = True
    show_attributes = False
    show_empty_relations = False
    imply_relations = True
    auto_labels = False
    deep_linking = True
    #transition = JSSymbol(src='$jit.Trans.Back.easeInOut')
    duration = 400

    backgroundcolor = '#FFFFFF'
    background = { 'CanvasStyles': { 'strokeStyle' : '#FFFFFF' } }
    Node = { 'color' : triads[1] }
    Edge = { 'color' : triads[2], 'lineWidth':1.5, }

    # Override the label style
    onPlaceLabel = JSSymbol(src="""
        (function(domElement, node){
            domElement.style.display = "none";
            domElement.innerHTML = node.name;
            domElement.style.display = "";
            var left = parseInt(domElement.style.left);
            domElement.style.width = '120px';
            domElement.style.height = '';
            var w = domElement.offsetWidth;
            domElement.style.left = (left - w /2) + 'px';

            domElement.style.cursor = 'pointer';
            if ( node._depth <= 1 )
                domElement.style.color = '%s';
            else
                domElement.style.color = '%s';
        })""" % (triads[0], triads_dark[0]))

def leafy_readme():
    """ Ridiculous """
    root = '/'.join(__file__.split('/')[:-2])
    fname = root + '/README.rst'
    with open(fname, 'r') as f:
        readme = f.read()
        return docutils.examples.html_body(unicode(readme))

class LeafyDialog(DialogWidget):
    id = 'leafy_dialog'
    options = {
        'title' : 'README.rst',
        'autoOpen' : False,
        'width' : 1000
    }
    value = leafy_readme()
