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

import sys

import cairo

import pycha.radar

from lines import lines

def radarChart(output):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
    dataSet = (
        ('lines', [(i, l[1]) for i, l in enumerate(lines)]),
    )

    options = {
        'axis': {
            'x': {
                'ticks': [dict(v=i, label=d[0]) for i, d in enumerate(lines)],
            },
            'y': {
                'tickCount': 5,
            },
            'tickFontSize': 10,
            'labelFont': 'MS ゴシンック',
            'labelFontSize': 16,
            'lineColor': '#ff0000',
        },
        'legend': {
            'hide': True,
        },
        'title': 'レーダーチャート',
        'titleFont': 'MS ゴシンック',
        'titleFontSize': 16,
        'colorScheme': {
            'name':'fixed',
            'args': {
                'colors': ['#0000ff'],
            },
        },
        'padding' : {
            'left': 10,
            'right': 10,
            'top': 10,
            'bottom': 10,
        },
        'background': {
            'lineColor': '#00aa00',
        },
        'stroke': {
            'width': 3,
        }
    }
    chart = pycha.radar.RadarChart(surface, options, frame='polygon')

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        output = sys.argv[1]
    else:
        output = 'radarchart.png'
    radarChart(output)
