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
import os
from HTMLParser import HTMLParser

from pyquery import PyQuery as pq
import urllib
import urlparse
import urllib2
from urllib import urlretrieve

lang_codes = {'en':'en_US',
              'ml':'ml_IN',
              'kn':'kn_IN',
              'as':'as_IN',
              'gu':'gu_IN',
              'bn':'bn_IN',
              'hi':'hi_IN',
              'mr':'mr_IN',
              'or':'or_IN',
              'pa':'pa_IN',
              'ta':'ta_IN',
              'te':'te_IN'}

class Wikiparser(HTMLParser):
    def __init__(self, url, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."
        HTMLParser.__init__(self)
        self.hyperlinks = []
        self.url = url
        self.language = detect_language(url)
        self.pdf = PDFWriter(urllib.unquote(self.url.split("/")[-1]) + ".pdf", StandardPaper.A4)
        header = Header(text_align=pango.ALIGN_CENTER)
        #TODO Alignment not working.
        header.set_text(urllib.unquote(self.url))
        self.pdf.set_header(header) 
        self.pdf.move_context(0, 500)
        h1 = Text(urllib.unquote(self.url.split("/")[-1]), font="serif", font_size=32) 
        h1.color = StandardColors.Blue
        self.pdf.add_text(h1)
        h2 = Text(urllib.unquote(self.url), font="serif", font_size=16) 
        h2.color = StandardColors.Blue
        self.pdf.add_text(h2)
        footer = Footer(text_align=pango.ALIGN_CENTER)
        footer.set_text("wiki2pdf")
        self.pdf.set_footer(footer)
        self.pdf.page_break()
        
    def reset(self):                              
        HTMLParser.reset(self)
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
        self.table = False
        self.tr = False
        self.th = False
        self.td = False
        self.caption = False
        self.reference = False
	self.ref_counter = 0
        self.column_counter = 0
        self.current_counter = 0
        self.buffer = None
        self.sup = False
        
    def handle_data(self, data):
        if data.strip() == "": return
	if self.p or self.h1 or self.h2 or self.a or self.span or self.li or self.td or self.th or self.caption:
            if self.buffer != None:
                self.buffer += data
    def handle_starttag(self, tag, attrs):
        if tag == 'img'and not self.table:
            self.start_img(attrs)
        elif tag == 'h1':
            self.start_h1(attrs)
        elif tag == 'h2':
            self.start_h2(attrs)
        elif tag == 'li':
            self.start_li(attrs)
        elif tag == 'p':
            self.start_p(attrs)
        elif tag == 'a':
            self.start_a(attrs)
        elif tag == 'ul':
            self.start_ul(attrs)
        elif tag == 'ol':
            self.start_ol(attrs)
        elif tag == 'table':
            self.start_table(attrs)
        elif tag == 'tr' and self.table:
            self.start_tr(attrs)
        elif tag == 'td' and self.table:
            self.start_td(attrs)
        elif tag == 'th'and self.table:
            self.start_th(attrs)
        elif tag == 'caption' and self.table:
            self.start_caption(attrs)
        elif tag == 'span':
	    self.start_span(attrs)
        elif tag == 'sup' or tag == 'sub' or tag == 'b' or tag == 'i' or tag == 's' or tag == 'small' or tag == 'big' or tag == 'tt' or tag == 'u':
            if self.reference == False and self.table == False:
               if self.buffer != None:
                  self.buffer += "<"+tag+">"
                  self.sup = True


    def handle_endtag(self, tag):
        if tag == 'img' and not self.table:
            self.end_img()
        elif tag == 'h1':
            self.end_h1()
        elif tag == 'h2':
            self.end_h2()
        elif tag == 'li':
            self.end_li()
        elif tag == 'p':
            self.end_p()
        elif tag == 'a':
            self.end_a()
        elif tag == 'ul':
            self.end_ul()
        elif tag == 'ol':
            self.end_ol()
        elif tag == 'table':
            self.end_table()
        elif tag == 'tr' and self.table:
            self.end_tr()
        elif tag == 'td' and self.table:
            self.end_td()
        elif tag == 'th' and self.table:
            self.end_th()
        elif tag == 'caption' and self.table:
            self.end_caption()
        elif tag == 'span':
            self.end_span()
        elif tag == 'sup' or tag == 'sub' or tag == 'b' or tag == 'i' or tag == 's' or tag == 'small' or tag == 'big' or tag == 'tt' or tag == 'u':
            if self.sup and self.buffer != None:
                self.buffer += "</"+str(tag)+">"
        

    def start_img(self, attrs):         
        src = [value for key, value in attrs if key == 'src'] 
        if src:
            self.images.extend(src)
            
    def end_img(self):
        for wiki_image in self.images:
            image  = Image()  
            outpath = self.grab_image(wiki_image, "/tmp")
            image.set_image_file(outpath)
            self.pdf.add_image(image)
        self.images = []
        
    def start_h1(self, attrs):         
        self.h1 = True
        self.buffer = ""
        
    def end_h1(self):
        self.h1 = False
        h1 = Text(self.buffer, font="FreeSerif", font_size=16) 
        h1.color = StandardColors.Blue
        self.pdf.add_text(h1)
        self.buffer = None
        
    def start_h2(self, attrs):         
        self.h2 = True
        self.buffer = ""
        
    def end_h2(self):
        self.h2 = False
        if self.buffer and self.buffer.strip() > "":
            h2 = Text(self.buffer, font="FreeSerif", font_size=14) 
            h2.color = StandardColors.Blue
            self.pdf.add_text(h2)
        self.buffer = None
        
    def start_caption(self, attrs):         
        self.caption = True
        self.buffer = ""
        
    def end_caption(self):
        self.caption = False
        if self.buffer and self.buffer.strip() > "":
            caption = Text(self.buffer, font="FreeSerif", font_size=14) 
            caption.color = StandardColors.Blue
            self.pdf.add_text(caption)
        self.buffer = None

    def start_li(self, attrs):         
        self.li = True
        self.buffer = ""
        
    def end_li(self):
        self.li = False
#        print self.buffer
        if self.buffer and self.buffer.strip() > "":
            if self.ul:
                li = Text(markup = "• " + self.buffer,font="FreeSerif", font_size=10)
            elif self.ol:
                self.ref_counter+=1
                li = Text(markup = str(self.ref_counter) + ". "+ self.buffer.replace("↑",""), font = "FreeSerif", font_size=10)
            else:
                li = Text(markup = self.buffer,font="FreeSerif", font_size=10)     
            self.pdf.add_text(li)
        self.buffer = None
                
    def start_a(self, attrs):         
        self.a = True
        
    def end_a(self):
        self.a = False

    def start_table(self, attrs): 
        for tups in attrs:
	    if 'class' in tups:
		if tups[1] == 'wikitable':
                    self.table = True
                    self.wikitable = Table(border_width = 1)
                    self.wikitable.cell_padding = [2,2,2,2]
        
    def end_table(self):
        if self.table:
            self.table = False
            self.pdf.add_table(self.wikitable)

    def start_tr(self, attrs):         
        self.tr = True
        self.row = Row(height=25)
        self.current_counter = 0
        
    def end_tr(self):
        self.tr = False
        if self.current_counter == self.column_counter:
            self.wikitable.add_row(self.row)

    def start_td(self, attrs):         
        self.td = True
        self.buffer = ""
        
    def end_td(self):
        self.td = False
        print self.buffer
        cell_content = Text(self.buffer,font_size=10)
        cell_content.color = Color(0.0,0.0,0.0,1.0)
        cell = Cell(cell_content, font_size=8,width=100)
        self.row.add_cell(cell)
        self.current_counter+=1
        self.buffer = None

    def start_th(self, attrs):         
        self.th = True
        self.buffer = ""
        
    def end_th(self):
        self.th = False
        #print self.buffer
        cell_content = Text(self.buffer,font_size=10)
        cell_content.color = Color(0.0,0.0,0.0,1.0)
        cell = Cell(cell_content, font_size=8,width=100)
        self.row.add_cell(cell)
        self.column_counter+=1
        self.buffer = None
    
#    def start_sup(self, attrs):         
#        self.sup = True
#        self.buffer += "<sup>"
#        
#    def end_sup(self):
#        print "test"
#        self.buffer += "</sup>"

        
    def start_ol(self, attrs):
        self.ol = True
        for tups in attrs:
	    if 'class' in tups:
		if tups[1] == 'references':
                    self.reference = True

    def end_ol(self):
        self.ol = False
        self.ref_counter = 0
        if self.reference:
            self.reference= False
            #self.sup = False
        
    def start_ul(self, attrs):
        self.ul = True    
    def end_ul(self):
        self.ul = False
            
    def start_span(self, attrs):         
        self.span = True
        if self.buffer == None:
            self.buffer = ""  
        
    def end_span(self):
        self.buffer += " "
        self.span = False
            
    def start_p(self, attrs):
        self.p = True
        self.buffer = ""
        
    def end_p(self) :
        self.p = False
        if self.sup:
            para = Paragraph(markup=self.buffer,text = self.buffer, font="FreeSerif", font_size=10,)
            self.sup = False
        else:
            #print self.buffer
            para = Paragraph(text=self.buffer, font="FreeSerif", font_size=10,)
           
        para.set_justify(True)
        if self.language:
            para.language = self.language
        else:
            para.language = None
            
        para.set_hyphenate(True)
        self.pdf.add_paragraph(para) 
#        f= open("computer_para.txt","aw")
#        f.write(self.buffer)
#        f.write("\n")
#        f.close()  
        self.buffer = None
    def set_header(self, text):
        self.header = text

    def grab_image(self, imageurl, outputfolder):
        """
        Get the image from wiki
        """
        output_filename = None
        try:
            link= imageurl.strip()
            parts = link.split("/")
            filename = parts[len(parts)-1]
            output_filename = os.path.join(outputfolder , filename)
            #output_filename=urllib.unquote(output_filename)
            print("GET IMAGE " + link + " ==> " + output_filename)
            if os.path.isfile(output_filename):
                print("File " + output_filename + " already exists")
                return output_filename
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            infile = opener.open(link)
            page = infile.read()
            f= open(output_filename,"w")
            f.write(page)
            f.close()
        except KeyboardInterrupt:
            sys.exit()
        except urllib2.HTTPError:
            print("Error: Cound not download the image")
            pass
        return  output_filename
    def parse(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        infile = opener.open(self.url)
        page = infile.read()
        page = cleanup(page)
#        f= open("computer.txt","w")
#        f.write(page)
#        f.close()
#        f = open("computer.txt","r")
#        page=f.read()
#        f.close()
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
    unwanted_sections_list = """
    div#jump-to-nav, div.top, div#column-one, div#siteNotice, div#purl, div#head,div#footer, div#head-base, div#page-base, div#stub, div#noprint,
    div#disambig,div.NavFrame,#colophon,.editsection,.toctoggle,.tochidden,.catlinks,.navbox,.sisterproject,.ambox,
    .toccolours,.topicondiv#f-poweredbyico,div#f-copyrightico,div#featured-star,li#f-viewcount,
    li#f-about,li#f-disclaimer,li#f-privacy,.portal, #footer, #mw-head, #toc
    """
    unwanted_divs = unwanted_sections_list.split(",")
    for section in unwanted_divs:
        document.remove(section.strip())
    return document.wrap('<div></div>').html().encode("utf-8")

def detect_language(url):
    """
    
    Arguments:
    - `url`: Input url inform en.wikipedia.org
    return language code for the url
    """

    # Split on .
    # ml.wikipedia.org/ becomes
    # [ml,wikipedia,org/]

    if url.startswith("http://"):
        url = url.split("http://")[1]
        
    url_pieces = url.split(".")
    return lang_codes.get(url_pieces[0], None)
    

    
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = Wikiparser(sys.argv[1]) #"http://ml.wikipedia.org/wiki/Computer"
        parser.parse()    
    else:
        print("Usage: wiki2pdf url")    
        print("Example: wiki2pdf http://en.wikipedia.org/wiki/Computer")    
