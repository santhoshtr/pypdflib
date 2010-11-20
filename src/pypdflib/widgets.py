#!/usr/bin/python
#-*- coding:utf-8 -*-
# pypdflib/widgets.py

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
import StringIO
from PIL import Image as pil_image
from utils import Hyphenator
from utils import normalizer
from styles import *
class Widget(object):
    
    def __init__(self,style = None):
        self.style = style
        self.xoffset = 0.0
        self.yoffset = 0.0
        self.margin_top = 0.0
        self.margin_bottom = 0.0
        self.margin_left = 0.0   
        self.margin_right = 0.0
        self.hyphenate = False
        self.language = None
        self.justify = True
        self.color = StandardColors.Black
        
    def set_justify(self, justify):
        self.justify = justify
        
    def set_hyphenate(self, hyphenate):
        self.hyphenate = hyphenate
        
    def set_language(self, language):
        self.language = language
        
    def set_margin(self, left,top, right,bottom) :
        self.margin_top = top
        self.margin_bottom = bottom
        self.margin_left = left   
        self.margin_right = right
        
    def set_style(self, style):
        self.style = style

    def set_xoffset(self,xoffset):
        self.xoffset = xoffset
        
    def set_yoffset(self, yoffset):
        self.yoffset = yoffset    
        
    def __getattribute__(self,name):
        if name == 'text':
            text = normalizer.normalize(object.__getattribute__(self, 'text'))
            if(self.justify and self.language and self.hyphenate):
                text = Hyphenator().hyphenate(text,self.language)
            return text
        else:
            return object.__getattribute__(self, name)

       
        
class Paragraph(Widget):
    
    def __init__(self,  text = None, markup = None, font = None, text_align = None, font_size = None):
        super(Paragraph,self).__init__()
        if font:
            self.font = font
        else:
            self.font = "Sans"    
        if font_size:
            self.font_size = font_size
        else:
            self.font_size = 10   
        if text_align:
            self.text_align = text_align
        else:
            self.text_align = pango.ALIGN_LEFT    
        self.text = text
        self.markup = markup
   
        
    def set_text(self,text):
        self.text = text


    def set_markup(self, markup):
        self.markup = markup


class Header(Widget):
    
    def __init__(self,  text = None, markup = None, font = None, text_align = None, font_size = None):
        super(Header,self).__init__()
        if font:
            self.font = font
        else:
            self.font = "Sans"    
        if font_size:
            self.font_size = font_size
        else:
            self.font_size = 10    
        if text_align:
            self.text_align = text_align
        else:
            self.text_align = pango.ALIGN_LEFT    
        self.text = text
        self.markup = markup
        self.underline =  True
        self.underline_thickness = 1.0
        
    def set_text(self,text):
        self.text = text
        
    def set_markup(self, markup):
        self.markup = markup
    
    def set_underline(self, thickness=None):
        self.underline =  True
        if thickness:
            self.underline_thickness = thickness
            
class Text(Widget):
    
    def __init__(self,  text = None, markup = None, font = None, text_align = None, font_size = None, height = 0,width = 0):
        super(Text,self).__init__()
        if font:
            self.font = font
        else:
            self.font = "Sans"    
        if font_size:
            self.font_size = font_size
        else:
            self.font_size = 10   
        if text_align:
            self.text_align = text_align
        else:
            self.text_align = pango.ALIGN_LEFT    
        self.text = text
        self.markup = markup
        self.underline =  False
        self.underline_thickness = 0.0
        
    def set_text(self,text):
        self.text = text
        
    def set_markup(self, markup):
        self.markup = markup
    
    def set_underline(self, thickness = None):
        self.underline =  True
        if thickness:
            self.underline_thickness = thickness


class Footer(Widget):
    
    def __init__(self,  text = None, markup = None, font = None, text_align = None, font_size = None):
        super(Footer,self).__init__()
        if font:
            self.font = font
        else:
            self.font = "Sans"    
        if font_size:
            self.font_size = font_size
        else:
            self.font_size = 10    
        if text_align:
            self.text_align = text_align
        else:
            self.text_align = pango.ALIGN_LEFT    

        self.text = text
        self.markup = markup
        self.underline =  True
        self.underline_thickness = 1.0
        
    def set_text(self,text):
        self.text = text
        
        
    def set_markup(self, markup):
        self.markup = markup
    
    def set_underline(self, thickness=None):
        self.underline =  True
        if thickness:
            self.underline_thickness = thickness

    
class Line(Widget) :
    
    def __init__(self, x1, y1, x2, y2):
        self.x1=x1
        if x2:
            self.x2 = x2
        else:
            self.x2 = x1
        self.y1 = y1
        self.y2 = y2
        self.thickness = None
        
    def set_thickness(self,thickness):
        self.thickness = thickness

class Cell(Text):
    def __init__(self,  text = None, border_width = 0, height = 0, width = 0, cell_spacing = [0,0,0,0], **kw):
       Text.__init__ (self, **kw)
       self.height = height
       self.width = width
       self.cell_spacing = cell_spacing
       self.text = text 
    
class Row(Widget):
    def __init__(self, cells = None,  border_width = 0, height = 0):
        self.border_width = border_width
        self.cells = cells
        self.height = height
        
    def add_cell(self, cell) :
        if cell == None: return
        if self.cells == None:
            self.cells = []
        self.cells.append(cell) 

class Table(Widget) :
    def __init__(self, rows=None, border_width=0):
        self.rows = rows
        self.border_width = border_width
        self.header_row = None
        self.subtitle = None
        self.column_count = 0
        self.row_count = 0
        
    def add_row(self, row):
        if row == None:return
        if self.rows == None: self.rows = []
        if self.column_count != 0:
            if len(row.cells) != self.column_count:
                raise Error('Number of cells differs in this row') 
        self.column_count = len(row.cells)
        self.rows.append(row)
        self.row_count = len(self.rows)
        
    def set_header_row(self,row):
        self.header_row = row
   
    def set_subtitle(self, text):
        self.subtitle = text
    
      
class Image(Widget):
    
    def __init__(self, image_file = None, width = None, height = None, scale_x = None, scale_y = None,padding_bottom = 10):
        super(Image,self).__init__()
        self.image_file = image_file
        self.width = width
        self.height = height
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.padding_bottom = padding_bottom
        self.image_data = None
    def set_width(self, width):
        self.width = width
    
    def set_image_file(self, imagefile):
        self.image_file = imagefile
        image = pil_image.open(imagefile)
        self.image_data = StringIO.StringIO()
        image.save(self.image_data, format="PNG")
        self.image_data.seek(0) # rewind
        
    def set_height(self, height):
        self.height = height
        
    def set_size(self,width,height):
        self.width = width
        self.height = height
        
    def set_scale(self, scale_x, scale_y):
        self.scale_x = scale_x
        self.scale_y = scale_y

