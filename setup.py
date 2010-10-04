import sys
import os
from setuptools import setup, find_packages

name='pypdflib'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description=(
        read('README')
        + '\n' 
        )

setup(
    name=name,
    version='1.0.0',
    url='http://github.com/santhoshtr/pypdflib',
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
    install_requires=['setuptools'],
    zip_safe = False,
    )
