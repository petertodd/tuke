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

from Tuke import Netlist,Element,Id

from Tuke.sch import Component,Pin
from Tuke.pcb import Footprint

class Symbol(Component):
    """Defines a Symbol.
   
    A Symbol is a Component with a Footprint.
    """

    def __init__(self,pins=(),footprint=None,id=Id()):
        """Create a symbol.

        pins - Pin list. Order is important, each pin will be linked to it's
               corresponding footprint pin, starting at 1.
        footprint - Footprint element to use.
        id - Id name
        """

        Component.__init__(self,id=id)

        assert isinstance(footprint,Footprint)
        self.add(footprint)

        for p in pins:
            if not isinstance(p,Pin):
                p = Pin(p)
            self.add(p)

        self.link_pins_to_footprint(pins)

    def link_pins_to_footprint(self,pins):
        """Link pins to footprint.

        Links pins to sequential footprint id numbers.

        Seperated out from __init__ for the use of multi-slot symbols.
        """

        for i,p in enumerate(pins):
            self.link(p,Id('%s/%d' % (self.footprint.id,i)))