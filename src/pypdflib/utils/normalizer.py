#!/usr/bin/python
#-*- coding:utf-8 -*-
# pypdflib/utis/normalizer.py

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

import re
import unicodedata
def normalize(text):
    text = unicodedata.normalize('NFC', unicode(text))
    space_re = re.compile('\s+', re.UNICODE)
    text = space_re.sub(' ', text)
    text = normalize_ml (text)
    return text
    
def normalize_ml (text):
    
    zwnj_re =  re.compile(u'‍+', re.UNICODE) # remove muliple instances of zwnj
    zwj_re =  re.compile(u'‍+', re.UNICODE) # remove muliple instances of  zwj 
    text = zwj_re.sub(u'‍', text)
    text = zwnj_re.sub(u'‍', text)
    text = text.replace(u"ൺ" , u"ണ്‍")
    text = text.replace(u"ൻ", u"ന്‍")
    text = text.replace(u"ർ", u"ര്‍")
    text = text.replace(u"ൽ", u"ല്‍")
    text = text.replace(u"ൾ", u"ള്‍")
    text = text.replace(u"ൿ", u"ക്‍")
    text = text.replace(u"ന്‍റ", u"ന്റ")
    return text     

