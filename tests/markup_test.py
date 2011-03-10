#!/usr/bin/python
#-*- coding: utf-8 -*-
# markup_test.py

# pypdflib is a pango/cairo framework for generating reports.
# Copyright © 2011  Jinesh K J <jinesh@jinsbond.in>

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
sys.path.append("../src/")  #not good!
from pypdflib.writer import PDFWriter
from pypdflib.widgets import *
from pypdflib.styles import *
import pango

if __name__=="__main__":
    pdf = PDFWriter("markup.pdf",StandardPaper.A4)
    header = Header(text_align = pango.ALIGN_CENTER)
    #TODO Alignment not working.
    header.set_text("test header")
    pdf.set_header(header)
    footer = Footer(text_align = pango.ALIGN_CENTER)
    footer.set_text("test footer")
    #TODO Alignment not working.
    pdf.set_footer(footer)
    h1= Text("Samples",font_size=16) 
    pdf.add_text(h1)
    h2= Text("Malayalam",font_size=14) 
    h2.color = StandardColors.Blue
    pdf.add_text(h2)
    
    para_file_malayalam=open("markup.txt")
    #image = Image(image_file="Four_Sons_of_Dasaratha.png")
    #pdf.add_image(image)
    while True:
        para_content = para_file_malayalam.readline()
        if para_content ==None or para_content=="" : break 
        para = Paragraph(markup=para_content,text = para_content font="Serif")
        para.language = "ml_IN"
        print para_content
        pdf.add_paragraph(para)
    pdf.flush()
    """
    table = Table(border_width=1)
    row = Row(height=50)
    for i in range(4):
        cell = Cell("SampleCell "+str(i),font_size=8,width=100)
        row.add_cell(cell)
    for i in range(4):
        table.add_row(row)
        
    pdf.draw_table(table)
    pdf.flush()
    """
