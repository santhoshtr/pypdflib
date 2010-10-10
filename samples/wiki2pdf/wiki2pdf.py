#!/usr/bin/python
#-*- coding: utf-8 -*-
# pypdflib/samples/wiki2pdf.py

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
sys.path.append("../")   #not good!
sys.path.append("../../src/")  #not good!
from pypdflib.writer import PDFWriter
from pypdflib.widgets import *
from pypdflib.styles import *
import pango
from sgmllib import SGMLParser
from pyquery import PyQuery as pq
import urllib
import urllib2

class Wikiparser(SGMLParser):
    def __init__(self, url, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."
        SGMLParser.__init__(self, verbose)
        self.hyperlinks = []
        self.url = url
        self.pdf = PDFWriter(self.url.split("/")[-1] +".pdf",595, 842)
        header = Header(text_align = pango.ALIGN_CENTER)
        #TODO Alignment not working.
        header.set_text(self.url)
        self.pdf.set_header(header)
        self.pdf.move_context(0,500)
        h1= Text(self.url.split("/")[-1],font="Dyuthi",font_size=32) 
        self.pdf.add_h1(h1)
        h2= Text(self.url,font="Rachana",font_size=16) 
        self.pdf.add_h2(h2)
        footer = Footer(text_align = pango.ALIGN_CENTER)
        footer.set_text("wiki2pdf")
        self.pdf.set_footer(footer)
        self.pdf.page_break()
        
    def reset(self):                              
        SGMLParser.reset(self)
        self.images = []
        #TODO Alignment not working.
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
        h1= Text(self.buffer,font="Dyuthi",font_size=16) 
        self.pdf.add_h1(h1)
        self.buffer = None
        
    def start_h2(self, attrs):         
        self.h2=True
        self.buffer=""
        
    def end_h2(self):
        self.h2=False
        if self.buffer and self.buffer.strip()>"":
            h2= Text(self.buffer,font="Rachana",font_size=14) 
            self.pdf.add_h2(h2)
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
            self.pdf.add_li(li)
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
        para = Paragraph(text=self.buffer, font="Rachana",font_size=10,)
        para.set_justify(True)
        para.language = "ml_IN"
        para.set_hyphenate(True)
        self.pdf.add_paragraph(para)   
        self.buffer = None
    def set_header(self,text):
        self.header = text
        
    def parse(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        infile = opener.open(self.url)
        page = infile.read()
        page = cleanup(page)
        "Parse the given string 's'."
        self.feed(page)
        self.close()
        self.pdf.flush()
        
def cleanup(page):
    """
    remove unwanted sections of the page.
    Uses pyquery.
    """
    document = pq(page)
    #If you want to remove any other section, just add the class or id of the section below with comma seperated
    unwanted_sections_list="""
    div#jump-to-nav, div.top, div#column-one, div#siteNotice, div#purl, div#head,div#footer, div#head-base, div#page-base, div#stub, div#noprint,
    div#disambig,div.NavFrame,#colophon,.editsection,.toctoggle,.tochidden,.catlinks,.navbox,.sisterproject,.ambox,
    .toccolours,.topicondiv#f-poweredbyico,div#f-copyrightico,div#featured-star,li#f-viewcount,
    li#f-about,li#f-disclaimer,li#f-privacy,.portal, #footer, #mw-head
    """
    unwanted_divs = unwanted_sections_list.split(",")
    for section in unwanted_divs:
        document.remove(section.strip())
    return document.wrap('<div></div>').html().encode("utf-8")
    
    
if __name__=="__main__":
    if len(sys.argv)>1:
        parser = Wikiparser(sys.argv[1]) #"http://ml.wikipedia.org/wiki/Computer"
        parser.parse()    
    else:
        print("Usage: wiki2pdf url")    
        print("Example: wiki2pdf http://en.wikipedia.org/wiki/Computer")    
