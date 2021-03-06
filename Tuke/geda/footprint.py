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

from Tuke.units import *
from Tuke import Element,Id
from Tuke.geometry import V,translate
from Tuke.pcb import Pin,Pad
import Tuke.pcb.footprint

import re

class Footprint(Tuke.pcb.footprint.Footprint):
    """Wrapper for gEDA/PCB footprints"""

    __required__ = ('file',)

    def _init(self):
        f = open(self.file,"r")

        for l in f:
            l = l.strip()

            tag = re.findall(r'^(ElementArc|ElementLine|Element|Pin|Pad)',l)

            if len(tag):

                v = re.findall(r'\[.*\]',l)

                # FIXME: add detection for mil units in () brackets
                source_units = CMIL 

                v = v[0][1:-1].split(' ')

                if tag[0] == 'Element':
                    (element_flags,description,pcb_name,value,mark_x,mark_y,text_x,text_y,text_direction,text_scale,text_flags) = v

                    mark_x = float(mark_x)
                    mark_y = float(mark_y)
                    text_x = float(text_x)
                    text_y = float(text_y)

                    mark_x *= source_units
                    mark_y *= source_units
                    text_x *= source_units
                    text_y *= source_units

                    # Base translation 
                    translate(self,V(mark_x,mark_y))

                elif tag[0] == 'Pin':
                    (x,y,thickness,clearance,mask,dia,name,pin_number,flags) = v
                    x = float(x) * source_units
                    y = float(y) * source_units
                    thickness = float(thickness) * source_units
                    clearance = float(clearance) * source_units
                    mask = float(mask) * source_units
                    dia = float(dia) * source_units

                    # Pin() defines pad thickness as the thickness of the
                    # metalization surrounding the hole. gEDA simply defines
                    # thickness as diameter of the metal, convert.
                    thickness = (thickness - dia) / 2

                    # gEDA defines clearance as the sum of both clearance
                    # thicknesses, Pin() defines it as a single thickness,
                    # convert
                    clearance = clearance / 2

                    pin_number = Id('_' + pin_number[1:-1]) # remove quotes

                    p = Pin(dia=dia,
                            thickness=thickness,
                            clearance=clearance,
                            mask=mask,
                            id=pin_number)
                    translate(p,V(x,y))

                    self.add(p)

                elif tag[0] == 'Pad':
                    (x1,y1,x2,y2,thickness,clearance,mask,name,pad_number,flags) = v

                    x1 = float(x1) * source_units
                    y1 = float(y1) * source_units
                    x2 = float(x2) * source_units
                    y2 = float(y2) * source_units
                    thickness = float(thickness) * source_units
                    clearance = float(clearance) * source_units
                    mask = float(mask) * source_units

                    # gEDA defines clearance as the sum of both clearance
                    # thicknesses, Pin() defines it as a single thickness,
                    # convert
                    clearance = clearance / 2

                    pad_number = Id('_' + pad_number[1:-1]) # remove quotes

                    p = Pad(a=(x1,y1),b=(x2,y2),
                            thickness=thickness,
                            clearance=clearance,
                            mask=mask,
                            id=pad_number)
                    self.add(p)
