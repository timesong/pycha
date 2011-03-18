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

import random
import sys

import cairo

import pycha.scatter


def scatterplotChart(output):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 400)

    top = 50
    dataSet = (
        ('points 1', [(i, random.random() * float(top)) for i in range(top)]),
        ('points 2', [(i, random.random() * float(top)) for i in range(top)]),
        ('points 3', [(i, random.random() * float(top)) for i in range(top)]),
        ('points 4', [(i, random.random() * float(top)) for i in range(top)]),
        ('points 5', [(i, random.random() * float(top)) for i in range(top)]),
        )

    options = {
        'background': {
            'color': '#eeeeff',
            'lineColor': '#444444',
        },
        'colorScheme': {
            'name': 'rainbow',
            'args': {
                'initialColor': 'blue',
            },
        },
        'legend': {
            'hide': True,
        },
        'title': u'Scatter plot',
    }
    chart = pycha.scatter.ScatterplotChart(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        output = sys.argv[1]
    else:
        output = 'scatterchart.png'
    scatterplotChart(output)
