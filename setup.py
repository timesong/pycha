# Copyright(c) 2007-2010 by Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
#
# This file is part of PyCha.
#
# PyCha is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyCha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PyCha.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup

from pycha import version

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="pycha",
    version=version,
    author="Lorenzo Gil Sanchez",
    author_email="lorenzo.gil.sanchez@gmail.com",
    description="A library for making charts with Python",
    long_description=(
        read('README.txt')
        + '\n\n' +
        read('CHANGES.txt')
    ),
    license="LGPL 3",
    keywords="chart cairo",
    packages=['pycha', 'chavier'],
    url='http://bitbucket.org/lgs/pycha/',
    # if would be nice if pycairo would have an egg (sigh)
#    install_requires = [
#        'pycairo',
#    ],
    zip_safe=True,
    entry_points={
        'gui_scripts': [
            'chavier = chavier.app:main',
        ]
    },
    test_suite="tests",
)
