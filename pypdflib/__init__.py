#!/usr/bin/python
#-*- coding:utf8 -*-
import cairo
import pango
import pangocairo

class PDFWriter():
    def __init__(self,filename, width, height):
        self.width=width
        self.height=height
        surface = cairo.PDFSurface(filename, self.width, self.height)
        self.context = cairo.Context(surface)
        self.context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        self.pc = pangocairo.CairoContext(self.context)
        #self.layout = self.pc.create_layout()
        self.position_x=0
        self.position_y=0
        self.left_margin= self.width*0.1
        self.right_margin= self.width*0.1
        self.top_margin= self.width*0.1
        self.bottom_margin= self.width*0.1
        self.line_width= 10
        self.font_size= 10
        self.page_num=0
        self.ybottom = self.height - self.top_margin - self.bottom_margin;
        
    def write_h1(self, text):
        h1_font_description = pango.FontDescription()
        h1_font_description.set_family("Rachana")
        h1_font_description.set_size((int)(16 * pango.SCALE))
        h1_layout = pangocairo.CairoContext(self.context).create_layout()
        h1_layout.set_font_description(h1_font_description)
        h1_layout.set_text(str(text))
        ink_rect, logical_rect = h1_layout.get_extents()
        self.position_y+=+self.line_width*4
        self.context.move_to(self.left_margin, self.position_y)
        self.pc.show_layout(h1_layout)
        self.position_y+=+self.line_width*4
        
    def write_h2(self, text):
        h2_font_description = pango.FontDescription()
        h2_font_description.set_family("Rachana")
        h2_font_description.set_size((int)(14 * pango.SCALE))
        h2_layout = pangocairo.CairoContext(self.context).create_layout()
        h2_layout.set_font_description(h2_font_description)
        h2_layout.set_text(str(text))
        ink_rect, logical_rect = h2_layout.get_extents()
        self.position_y+=+self.line_width*3
        self.context.move_to(self.left_margin, self.position_y)
        self.pc.show_layout(h2_layout)
        self.position_y+=+self.line_width*3
        
        
        
    def write_h3(self, text):
        h3_font_description = pango.FontDescription()
        h3_font_description.set_family("Rachana")
        h3_font_description.set_size((int)(12 * pango.SCALE))
        h3_layout = pangocairo.CairoContext(self.context).create_layout()
        h3_layout.set_font_description(h1_font_description)
        h3_layout.set_text(str(text))
        ink_rect, logical_rect = h3_layout.get_extents()
        self.position_y+=+self.line_width*2
        self.context.move_to(self.left_margin, self.position_y)
        self.pc.show_layout(h3_layout)
        self.position_y+=+self.line_width*2    
        
    def write_pagenum(self,page_num):
        pagenum_font_description = pango.FontDescription()
        pagenum_font_description.set_family("Rachana")
        pagenum_font_description.set_size((int)(10 * pango.SCALE))
        pagenum_layout = pangocairo.CairoContext(self.context).create_layout()
        pagenum_layout.set_font_description(pagenum_font_description)
        pagenum_layout.set_text(str(page_num))
        ink_rect, logical_rect = pagenum_layout.get_extents()
        self.context.move_to(self.width/2, self.height - self.bottom_margin+self.line_width)
        self.pc.show_layout(pagenum_layout)
        print "Page: " , page_num
        self.context.move_to(self.left_margin, self.top_margin)
        
    def write_header(self, header):
        pagenum_font_description = pango.FontDescription()
        pagenum_font_description.set_family("Rachana")
        pagenum_font_description.set_size((int)(8 * pango.SCALE))
        pagenum_layout = pangocairo.CairoContext(self.context).create_layout()
        pagenum_layout.set_font_description(pagenum_font_description)
        pagenum_layout.set_text(str(header))
        ink_rect, logical_rect = pagenum_layout.get_extents()
        self.context.move_to(self.left_margin, self.line_width*2)
        self.pc.show_layout(pagenum_layout)
        self.context.move_to(self.left_margin, self.top_margin)
        self.position_y=self.line_width
        self.draw_line()
        
    def draw_line(self):
        self.position_y+= self.line_width*2
        self.context.move_to(self.left_margin, self.position_y)
        self.context.set_source_rgba (0.0, 0.0, 0.0, 1.0)
        self.context.line_to(self.width-self.right_margin, self.position_y)
        self.context.stroke()
        self.position_y+= self.line_width
        
    def write_paragraph(self, text):
        self.position = (self.left_margin, self.position_y+self.top_margin)
        paragraph_layout = pangocairo.CairoContext(self.context).create_layout()
        paragraph_layout.set_font_description(pango.FontDescription('Rachana Normal 10'))
        paragraph_layout.set_width((int)((self.width - self.left_margin-self.right_margin) * pango.SCALE))
        paragraph_layout.set_justify(True)
        paragraph_layout.set_text(text)
        self.context.move_to(*self.position)
        pango_layout_iter = paragraph_layout.get_iter();
        while not pango_layout_iter.at_last_line():
            first_line = True
            while not pango_layout_iter.at_last_line() :
                ink_rect, logical_rect = pango_layout_iter.get_line_extents()
                line = pango_layout_iter.get_line_readonly()
                pango_layout_iter.next_line()
                # Decrease paragraph spacing
                if  ink_rect[2] == 0 : #It is para break
                    dy = self.font_size / 2
                    self.position_y += dy
                    if not first_line:
                        self.context.rel_move_to(0, dy)
                else:
                    xstart = 1.0 * logical_rect[0] / pango.SCALE
                    self.context.rel_move_to(xstart, 0)
                    self.pc.show_layout_line( line)
                    line_height = (int)(logical_rect[3] / pango.SCALE)
                    self.context.rel_move_to(-xstart, line_height )
                    self.position_y += line_height 
 
                if self.position_y > self.ybottom:
                    self.page_num= self.page_num+1
                    self.write_header("രാമായണം - മലയാളം വിക്കിപീഡിയ")
                    self.write_pagenum(self.page_num)
                    self.context.show_page()
                    self.position_y=0
                    break
            first_line = False
        
    def draw_image(self, image_name):
        self.context.move_to(self.left_margin, self.position_y)
        image = cairo.ImageSurface.create_from_png (image_name)
        w = image.get_width ()
        h = image.get_height ()
        self.context.set_source_surface (image,self.left_margin,self.position_y)
        self.context.paint ()
        self.position_y+=h


    def save(self):
        self.context.save()
        
    def new_page(self):
        self.context.identity_matrix()
        self.context.set_source_rgba (1.0, 1.0, 1.0, 1.0)
        self.context.rectangle(0, self.position_y, self.width, self.height)
        self.context.fill()
        self.context.set_source_rgb (0.0, 0.0, 0.0)
        self.context.move_to(self.left_margin, self.top_margin)
        self.position_y=0    
        self.context.show_page()



