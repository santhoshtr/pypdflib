#!/usr/bin/python
#-*- coding: utf-8 -*-
# test.py

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
sys.path.append("../src/")  #not good!
from pypdflib.writer import PDFWriter
from pypdflib.widgets import *
from pypdflib.styles import *
import pango

if __name__=="__main__":
    pdf = PDFWriter("tables.pdf",StandardPaper.A4)
    header = Header(text_align = pango.ALIGN_CENTER)
    #TODO Alignment not working.
    header.set_text("test header")
    pdf.set_header(header)
    footer = Footer(text_align = pango.ALIGN_CENTER)
    footer.set_text("test footer")
    #TODO Alignment not working.
    pdf.set_footer(footer)
    table = Table(border_width=1)
    table.cell_padding = [2, 2, 2, 2]
    row = Row(height=50)
    for i in range(4):
        cell_content = Text("SampleCell "+str(i),font_size=14)
        cell_content.color = Color(0.0,0.0,0.8,1.0)
        cell = Cell(cell_content, font_size=8,width=100)
        row.add_cell(cell)
    for i in range(4):
        table.add_row(row)
    pdf.add_table(table)
    pdf.flush()
