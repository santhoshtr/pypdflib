# -*- coding: utf-8 -*-
# pypdflib/styles.py

# pypdflib is a pango/cairo framework for generating reports.
# Copyright © 2010  Santhosh Thottingal <santhosh.thottingal@gmail.com>

# This file is part of pypdflib.
#
# pypdflib is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.  
#
# pypdflib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pypdflib.  If not, see <http://www.gnu.org/licenses/>.

import pango

ALIGN_LEFT = 0
ALIGN_CENTER = 1
ALIGN_RIGHT = 2
ALIGN_TOP = 0
ALIGN_MIDDLE = 1
ALIGN_BOTTOM = 2

ATTRS = ('font', 'font_size', 'border', 'margin', 'padding', 'align', 'valign', 'text_align')

def rgba_to_cairo (r, g, b, a):
    return (r/65535.0, g/65535.0, b/65535.0, a/65535.0)

class BorderSide (object):
    def __init__ (self, width=0, color=None, dash=None, round=0):
        self.width = width
        if not color:
            self.color = (0, 0, 0, 1)
        else:
            self.color = color
        if not dash:
            self.dash = []
        else:
            self.dash = dash
        self.round = round

class Border (object):
    def __init__ (self, width=0, color=None, dash=None, round=0):
        self.left = BorderSide (width, color, dash, round)
        self.top = BorderSide (width, color, dash, round)
        self.right = BorderSide (width, color, dash, round)
        self.bottom = BorderSide (width, color, dash, round)

class Dimension (object):
    def __init__ (self, width=0, height=0):
        self.width = width
        self.height = height

    def valid (self):
        return self.width > 0 and self.height > 0

    def maximize (self, d):
        self.width = max (self.width, d.width)
        self.height = max (self.height, d.height)

    def max_width (self, width):
        return max (self.width, width)

    def max_height (self, height):
        return max (self.height, height)

    def min_width (self, width):
        if self.valid ():
            return min (self.width, width)
        else:
            return width

    def min_height (self, height):
        if self.valid ():
            return min (self.height, height)
        else:
            return height

    def __add__ (self, d):
        return Dimension (self.width + d.width, self.height + d.height)

    def __str__ (self):
        return "Dimension (%d, %d)" % (self.width, self.height)

class Rectangle (Dimension):
    def __init__ (self, x=0, y=0, width=0, height=0, page=1):
        Dimension.__init__ (self, width, height)
        self.x = x
        self.y = y
        self.page = page
        self.no_paging = False

    def __add__ (self, d):
        return Rectangle (self.x, self.y, self.width + d.width, self.height + d.height)

    def __str__ (self):
        return "Rectangle (%d, %d, %d, %d)" % (self.x, self.y, self.width, self.height)

class Spacing (object):
    def __init__ (self, left=0, top=0, right=0, bottom=0):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def __str__ (self):
        return "Spacing (%d, %d, %d, %d)" % (self.left, self.top, self.right, self.bottom)

class Style (object):
    def __init__ (self, name=""):
        self.name = name

    def inherit (self, style):
        for attr in ATTRS:
            if not hasattr (self, attr) or getattr (self, attr) is None:
                setattr (self, attr, getattr (style, attr))

    def copy (self):
        s = Style (self.name)
        s.inherit (self)
        return s

    def __str__ (self):
        return "Style (%s)" % self.name

class Stylesheet (dict):
    def __init__ (self):
        s = self['widget'] = Style ('widget')
        s.font = 'Sans 12'
        s.font_size = 12
        s.border = Border ()
        s.margin = Spacing ()
        s.padding = Spacing ()
        s.align = ALIGN_LEFT
        s.valign = ALIGN_TOP
        s.text_align = pango.ALIGN_LEFT
        s = self['paragraph'] = Style ('paragraph')
        s.inherit (self['widget'])

default_stylesheet = Stylesheet ()

__all__ = ['default_stylesheet', 'Style', 'Dimension', 'Spacing', 'Rectangle', 'Border', 'BorderSide']
