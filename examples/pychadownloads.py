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

import cairo

import pycha.stackedbar


def barChart(output):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 400)

    dataSet = (
        ('main release', [(0, 263), (1, 641), (2, 969), (3, 278), (4, 989)]),
        ('1st bug fix',  [(0, 0),   (1, 0),   (2, 0),   (3, 787), (4, 234)]),
        ('2nd bug fix',  [(0, 0),   (1, 0),   (2, 0),   (3, 309), (4, 1581)]),
        ('3nd bug fix',  [(0, 0),   (1, 0),   (2, 0),   (3, 0),   (4, 1824)]),
        )

    options = {
        'axis': {
            'x': {
                'ticks': [dict(v=0, label='0.1 (Oct 07)'),
                          dict(v=1, label='0.2 (Oct 07)'),
                          dict(v=2, label='0.3 (Mar 08)'),
                          dict(v=3, label='0.4 (Oct 08)'),
                          dict(v=4, label='0.5 (Mar 09)')],
                'label': 'Releases',
            },
            'y': {
                'label': 'Downloads',
            }
        },
        'background': {
            'chartColor': '#ffeeff',
            'baseColor': '#ffffff',
            'lineColor': '#444444'
        },
        'colorScheme': {
            'name': 'gradient',
            'args': {
                'initialColor': 'green',
            },
        },
        'legend': {
            'position': {
                'top': 20,
                'left': 80,
            }
        },
        'title': 'Pycha Downloads'
    }
    chart = pycha.stackedbar.StackedVerticalBarChart(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(output)

if __name__ == '__main__':
    barChart('pychadownloads.png')
