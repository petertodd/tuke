# vim: tabstop=4 expandtab shiftwidth=4 fileencoding=utf8
# ### BOILERPLATE ###
# Tuke - Electrical Design Automation toolset
# Copyright (C) 2008 Peter Todd <pete@petertodd.org>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ### BOILERPLATE ###

from Tuke import Element
from Tuke.geo import Geo,Hole,Polygon

class Pin(Element):
    """Defines a pin"""

    def __init__(self,id,dia,thickness,clearance,mask,square=False):
        """Create a pin

        
        """
        Element.__init__(self,id = id)

        self.dia = dia
        self.thickness = thickness
        self.clearance = clearance
        self.mask = mask
        self.square = square

    def gen_pad_shape(self,thick,square,id='../',layer=None):
        """Returns a pad shape, circle or square, with a given thickness.

        For makng pads or masks.
        """

        return Polygon(((-thick,-thick),(thick,-thick),(thick,thick),(-thick,thick)),id=id,layer=layer)

    def geo(self):
        """Generate geometry"""

        g = Geo() 

        g.add(Hole(self.dia,id=self.id))

        g.add(self.gen_pad_shape(self.thickness,self.square,id=self.id,layer='top.pad'))
        g.add(self.gen_pad_shape(self.mask,self.square,layer='top.mask'))
        g.add(self.gen_pad_shape(self.mask + (self.clearance * 2),self.square,layer='top.clearance'))

        return g