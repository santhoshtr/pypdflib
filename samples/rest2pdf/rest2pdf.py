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

import sys
import codecs
from sgmllib import SGMLParser
from docutils.core import publish_parts
from docutils.writers.html4css1 import Writer
sys.path.append("../../src/")  #not good!
from pypdflib.writer import PDFWriter
from pypdflib.widgets import *
from pypdflib.styles import *

SETTINGS = {
    'cloak_email_addresses': True,
    'file_insertion_enabled': False,
    'raw_enabled': False,
    'strip_comments': True,
    'doctitle_xform': False,
    'report_level': 5,
}

class HTMLParser(SGMLParser):
    def __init__(self, verbose=0):

        "Initialise an object, passing 'verbose' to the superclass."

        SGMLParser.__init__(self, verbose)
        self.hyperlinks = []

        self.pdf = None
        
    def reset(self):                              
        SGMLParser.reset(self)
        self.images = []

        self.h1 = False
        self.h2 = False
        self.li = False
        self.p = False
        self.a = False
        self.ul = False
        self.ol = False
        self.span = False
        self.buffer = None
        
    def handle_data(self,data):
        if data.strip() == "": return
        if self.p or self.h1 or self.h2 or self.a or self.span:
            if self.buffer!=None:
                self.buffer+= data
            
                
    def start_img(self, attrs):         
        src = [value for key, value in attrs if key=='src'] 
        if src:
            self.images.extend(src)
            
    def start_h1(self, attrs):         
        self.h1=True
        self.buffer=""
        
    def end_h1(self):
        self.h1=False
        h1= Text(self.buffer,font="Serif",font_size=16) 
        self.pdf.add_text(h1)
        self.buffer = None
        
    def start_h2(self, attrs):         
        self.h2=True
        self.buffer=""
        
    def end_h2(self):
        self.h2=False
        if self.buffer and self.buffer.strip()>"":
            h2= Text(self.buffer,font="Serif",font_size=14) 
            self.pdf.add_text(h2)
        self.buffer = None
        
    def start_li(self, attrs):         
        self.li=True
        self.buffer=""
        
    def end_li(self):
        self.li=False
        if self.buffer and self.buffer.strip()>"":
            if self.ul:
                li= Text("• "+self.buffer,font_size=10) 
            else:
                li= Text(self.buffer,font_size=10)     
            self.pdf.add_text(li)
        self.buffer = None
                
    def start_a(self, attrs):         
        self.a = True
        
    def end_a(self):
        self.a = False
        
    def start_ol(self,attrs):
        self.ol=True    
    def end_ol(self):
        self.ol=False
        
    def start_ul(self,attrs):
        self.ul=True    
    def end_ul(self):
        self.ul=False
            
    def start_span(self, attrs):         
        self.span=True
        if self.buffer==None:
            self.buffer=""  
        
    def end_span(self):
        self.buffer+=" "
        self.span=False
            
    def start_p(self,attrs):
        self.p=True
        self.buffer=""
        
    def end_p(self) :
        self.p=False
        para = Paragraph(text=self.buffer, font="Serif",font_size=10,)
        para.set_justify(True)
        para.set_hyphenate(False)
        self.pdf.add_paragraph(para)   
        self.buffer = None

    def parse(self, filename, outputfile):
        try:
            text = codecs.open(filename, 'r', 'utf-8').read()
        except IOError: # given filename could not be found
            return ''
        parts = publish_parts(text, writer=Writer(), settings_overrides=SETTINGS)
        if 'html_body' in parts:
            html = parts['html_body']
        "Parse the given string 's'."
        self.pdf = PDFWriter(outputfile, StandardPaper.A4)
        footer = Footer()
        header = Header()
        self.pdf.set_footer(footer)
        self.pdf.set_header(header)
        self.feed(html)
        self.close()
        self.pdf.flush()


if __name__ == '__main__':
    parser = HTMLParser()
    parser.parse(sys.argv[1], sys.argv[2])
