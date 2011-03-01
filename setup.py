#!/usr/bin/python
#-*- coding:utf-8 -*-

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
import os
from setuptools import setup, find_packages

name='pypdflib'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description=(
        read('README.md')
        + '\n' 
        )

setup(
    name=name,
    version='0.1.a3',
    url='https://savannah.nongnu.org/projects/pypdflib',
    license='LGPL 3.0',
    description='PangoCairo based Python PDF Library',
    author='Santhosh Thottingal',
    author_email='santhosh.thottingal@gmail.com',
    long_description=long_description,
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    setup_requires = ['setuptools-git'],
    namespace_packages=['pypdflib'],
    include_package_data = True,
    install_requires=['setuptools','PIL'],
    zip_safe = False,
    )
