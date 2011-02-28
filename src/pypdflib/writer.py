#!/usr/bin/python
#-*- coding: utf-8 -*-
# pypdflib/writer.py

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

import cairo
import pango
import pangocairo
class PDFWriter():

    def __init__(self,filename, paper):
        self.width = paper.width
        self.height = paper.height
        surface = cairo.PDFSurface(filename, self.width, self.height, pointsize=1)
        self.context = cairo.Context(surface)
        self.context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        self.pc = pangocairo.CairoContext(self.context)
        self.position_x = 0
        self.position_y = 0
        self.left_margin = self.width*0.1
        self.right_margin = self.width*0.1
        self.top_margin = self.width*0.1
        self.bottom_margin = self.width*0.1
        self.line_width = 10
        self.font_size = 10
        self.para_break_width = 10
        self.page_num = 0
        self.ybottom = self.height - self.bottom_margin*2
        self.header = None
        self.footer = None
        
    def set_header(self, header):
        """
        Sets the header of the page
        """
        self.header = header 
        self.write_header(self.header)
        
    def set_footer(self, footer):
        """
        Sets the footer of the page
        """
        self.footer = footer
        
    def add_text(self, text):
        """
        Add text widget
        """

        text_font_description = pango.FontDescription()
        text_font_description.set_family(text.font)
        text_font_description.set_size((int)(text.font_size* pango.SCALE))
        text_layout = pangocairo.CairoContext(self.context).create_layout()
        text_layout.set_font_description(text_font_description)
        text_layout.set_width((int)((self.width - self.left_margin-self.right_margin) * pango.SCALE))
        text_layout.set_alignment(text.text_align)
        text_layout.set_text(str(text.text))
        ink_rect, logical_rect = text_layout.get_extents()
        if self.position_y == 0:
            self.position_y += self.top_margin 
        self.position_y += self.line_width
        self.assert_page_break()
        self.context.move_to(self.left_margin, self.position_y)
        self.context.set_source_rgba (text.color.red,text.color.green, text.color.blue,text.color.alpha)
        self.pc.show_layout(text_layout)
        self.position_y += logical_rect[3]/pango.SCALE+self.para_break_width
  
        
    def write_footer(self,footer):
        if footer == None: return 
        footer_font_description = pango.FontDescription()
        footer_font_description.set_family(footer.font)
        footer_font_description.set_size((int)(footer.font_size* pango.SCALE))
        footer_layout = pangocairo.CairoContext(self.context).create_layout()
        footer_layout.set_font_description(footer_font_description)
        if footer.markup:
            footer_layout.set_text(str(footer.markup))
        else:
            footer_layout.set_text(str(footer.text))
        ink_rect, logical_rect = footer_layout.get_extents()
        y_position= self.height - self.bottom_margin- logical_rect[3]/pango.SCALE
        self.context.move_to(self.width/2, y_position)
        self.context.set_source_rgba (footer.color.red,footer.color.green, footer.color.blue,footer.color.alpha)
        self.pc.show_layout(footer_layout)
        self.draw_line(y_position)
        self.ybottom = y_position-self.line_width
        
    def write_header(self, header):
        if header == None: return 
        header_font_description = pango.FontDescription()
        header_font_description.set_family(header.font)
        header_font_description.set_size((int)(header.font_size * pango.SCALE))
        header_layout = pangocairo.CairoContext(self.context).create_layout()
        header_layout.set_font_description(header_font_description)
        header_layout.set_alignment(header.text_align)
        if header.markup:
            header_layout.set_markup(str(header.markup))
        else:
            header_layout.set_text(str(header.text))
        ink_rect, logical_rect = header_layout.get_extents()
        self.context.move_to(self.left_margin, self.top_margin)
        self.context.set_source_rgba (header.color.red,header.color.green, header.color.blue,header.color.alpha)
        self.pc.show_layout(header_layout)
        y_position = self.top_margin+(logical_rect[3] / pango.SCALE)
        self.draw_line(y_position)
        self.position_y = y_position + self.line_width*2
        
    def draw_line(self, y_position=0):
        if y_position ==0 :
            y_position = self.position_y
        self.context.move_to(self.left_margin, y_position)
        self.context.set_source_rgba (0.0, 0.0, 0.0, 1.0)
        self.context.line_to(self.width-self.right_margin,  y_position)
        self.context.stroke()
        self.position_y+= self.line_width
        
    def add_paragraph(self, paragraph):
        self.position_y+=self.para_break_width
        self.assert_page_break();
        self.position = (self.left_margin, self.position_y)
        self.context.set_source_rgba (0.0, 0.0, 0.0, 1.0)
        paragraph_layout = pangocairo.CairoContext(self.context).create_layout()
        paragraph_font_description = pango.FontDescription()
        paragraph_font_description.set_family(paragraph.font)
        paragraph_font_description.set_size((int)(paragraph.font_size * pango.SCALE))
        paragraph_layout.set_font_description(paragraph_font_description)
        paragraph_layout.set_width((int)((self.width - self.left_margin-self.right_margin) * pango.SCALE))
        if(paragraph.justify):
            paragraph_layout.set_justify(True)
        paragraph_layout.set_text(paragraph.text+"\n")#fix it , adding new line to keep the looping correct?!
        self.context.move_to(*self.position)
        pango_layout_iter = paragraph_layout.get_iter();
        itr_has_next_line=True
        while not pango_layout_iter.at_last_line():
            first_line = True
            self.context.move_to(self.left_margin, self.position_y)
            while not pango_layout_iter.at_last_line() :
                ink_rect, logical_rect = pango_layout_iter.get_line_extents()
                line = pango_layout_iter.get_line_readonly()
                has_next_line=pango_layout_iter.next_line()
                # Decrease paragraph spacing
                if  ink_rect[2] == 0 : #It is para break
                    dy = self.font_size / 2
                    self.position_y += dy
                    if not first_line:
                        self.context.rel_move_to(0, dy)
                else:
                    xstart = 1.0 * logical_rect[0] / pango.SCALE
                    self.context.rel_move_to(xstart, 0)
                    self.context.set_source_rgba (paragraph.color.red,paragraph.color.green, paragraph.color.blue,paragraph.color.alpha)
                    self.pc.show_layout_line( line)
                    line_height = (int)(logical_rect[3] / pango.SCALE)
                    self.context.rel_move_to(-xstart, line_height )
                    self.position_y += line_height 
 
                if self.position_y > self.ybottom:
                    self.page_num= self.page_num+1
                    self.write_header(self.header)
                    if self.footer:
                        self.footer.set_text(str(self.page_num))
                    self.write_footer(self.footer)
                    self.context.show_page()
                    break
                    
            first_line = False

    def flush(self) :   
        """
        Flush the contents before finishing and closing the PDF.
        This must be called at the end of the program. Otherwise the footer at the
        last page will be missing.
        """
        self.page_num= self.page_num+1
        self.write_header(self.header)
        if self.footer:
            self.footer.set_text(str(self.page_num))
        self.write_footer(self.footer)
        self.context.show_page()
    
    def draw_table(self, table):
        if table.row_count == 0: 
            print("Table has no rows")
            return 
        self.context.identity_matrix()
        self.context.set_source_rgba (0.0, 0.0, 0.0, 1.0)
        x1 = self.left_margin
        y1 = self.top_margin
        width=height=0
        for row in range(table.row_count):
            for column in range(table.column_count):
                height = table.rows[row].height
                width  = table.rows[row].cells[column].width    
                self.context.set_line_width(table.border_width)
                self.context.rectangle(x1,y1,width,height)
                self.context.stroke()
                self.draw_cell(table.rows[row].cells[column],x1,y1,x1+width,y1+height)
                x1+=width
            y1+=height    
            x1= self.left_margin   
            self.position_y += height
                
    def draw_cell(self, cell, x1, y1, x2, y2):
        cell_font_description = pango.FontDescription()
        cell_font_description.set_family(cell.font)
        cell_font_description.set_size((int)(cell.font_size* pango.SCALE))
        cell_layout = pangocairo.CairoContext(self.context).create_layout()
        cell_layout.set_width(int(x2-x1)*pango.SCALE)
        cell_layout.set_justify(True)
        cell_layout.set_font_description(cell_font_description)
        cell_layout.set_text(str(cell.text))
        ink_rect, logical_rect = cell_layout.get_extents()
        self.context.move_to(x1,y1)
        self.pc.show_layout(cell_layout)
                
    def add_image(self, image):
        self.context.save ()
        self.context.move_to(self.left_margin, self.position_y)
        image_surface = cairo.ImageSurface.create_from_png (image.image_data)
        w = image_surface.get_width ()
        h = image_surface.get_height ()
        if (self.position_y + h*0.5) > self.ybottom:
            self.page_break()
        data =image_surface.get_data()
        stride = cairo.ImageSurface.format_stride_for_width (cairo.FORMAT_ARGB32, w)
        image_surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, w, h,stride)
        self.assert_page_break()
        self.context.scale(0.5, 0.5)
        self.context.set_source_surface (image_surface,self.left_margin/0.5, self.position_y/0.5)
        self.context.paint()
        self.context.restore ()        
        self.position_y+= h*0.5+ image.padding_bottom 
        
        
    def new_page(self):
        self.context.identity_matrix()
        self.context.set_source_rgba (1.0, 1.0, 1.0, 1.0)
        self.context.rectangle(0, self.position_y, self.width, self.height)
        self.context.fill()
        self.context.set_source_rgb (0.0, 0.0, 0.0)
        self.context.move_to(self.left_margin, self.top_margin)
        self.position_y=0    
        self.context.show_page()
        
    def blank_space(self, height):
        """
        Inserts vertical blank space 
        Color will be white.
        
        Arguments
        -height - The vertical measurement for the blank space.
        """
        self.context.identity_matrix()
        self.context.set_source_rgba (1.0, 1.0, 1.0, 1.0)
        self.context.rectangle(0, self.position_y, self.width, height)
        self.context.fill()
        self.context.set_source_rgb (0.0, 0.0, 0.0)
        self.context.move_to(self.left_margin, self.top_margin)
        self.position_y=0    
        
                    
    def page_break(self):
        """
        Insert a pagebreak.
        If the header and footer is set, they will be written to page.
        Page number will be incremented.
        """
        self.page_num= self.page_num+1
        self.write_header(self.header)
        if self.footer:
            self.footer.set_text(str(self.page_num))
            self.write_footer(self.footer)
        self.context.show_page()
        
    def assert_page_break(self):
        """
        Check if the current y position exceeds the page's height. 
        If so do the page break.
        """
        if  self.position_y > self.ybottom:
            self.page_break()

    def move_context(self, xoffset, yoffset):
        """
        Move the drawing context to given x,y offsets. 
        This is relative to the currect x,y drawing positions.
        
        Arguments:
    
        - xoffset: offset for the current x drawing postion 
        - yoffset: offset for the current y drawing postion 
        
        """
        self.position_x += xoffset
        self.position_y += yoffset
        
        
