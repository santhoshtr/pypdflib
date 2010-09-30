#!/usr/bin/python
#-*- coding:utf8 -*-
import sys
sys.path.append("../")  
from pypdflib.writer import PDFWriter
from pypdflib.widgets import *
from pypdflib.styles import *
import pango

if __name__=="__main__":
    pdf = PDFWriter("output.pdf",595, 842)
    header = Header(text_align = pango.ALIGN_CENTER)
    #TODO Alignment not working.
    header.set_text("test header")
    pdf.set_header(header)
    footer = Footer(text_align = pango.ALIGN_CENTER)
    footer.set_text("test footer")
    #TODO Alignment not working.
    pdf.set_footer(footer)
    h1= Text("Samples",font_size=16) 
    pdf.add_h1(h1)
    h2= Text("Malayalam",font_size=14) 
    pdf.add_h2(h2)
    para_file_malayalam=open("malayalam.txt")
    #image = Image(image_file="Four_Sons_of_Dasaratha.png")
    #pdf.add_image(image)
    while True:
        para_content = para_file_malayalam.readline()
        if para_content ==None or para_content=="" : break 
        para = Paragraph(text=para_content, font="Rachana")
        pdf.add_paragraph(para)
    h2= Text("Hindi",font_size=14, font="Rachana") 
    pdf.add_h2(h2)
    para_file_hindi=open("hindi.txt")
    
    while True:
        para_content = para_file_hindi.readline()
        if para_content ==None or para_content=="" : break 
        para = Paragraph(text=para_content)
        pdf.add_paragraph(para)
        
    h2= Text("Bengali",font_size=14) 
    pdf.add_h2(h2)   
     
    para_file_bengali=open("bengali.txt")
    while True:
        para_content = para_file_bengali.readline()
        if para_content ==None or para_content=="" : break 
        para = Paragraph(text=para_content)
        pdf.add_paragraph(para)
    
    pdf.flush()
    table = Table(border_width=1)
    row = Row(height=50)
    for i in range(4):
        cell = Cell("SampleCell "+str(i),font_size=8,width=100)
        row.add_cell(cell)
    for i in range(4):
        table.add_row(row)
        
    pdf.draw_table(table)    
