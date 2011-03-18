# Copyright(c) 2009-2010 by Yaco S.L. <lgs@yaco.es>
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

import pycha.stackedbar


def stackedBarChart(output, chartFactory):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 400)

    dataSet = (
        ('internal', [(0, 8), (1, 10), (2, 5), (3, 6)]),
        ('external', [(0, 5), (1, 2), (2, 4), (3, 8)]),
        )

    options = {
        'background': {
            'chartColor': '#ffeeff',
            'baseColor': '#ffffff',
            'lineColor': '#444444',
        },
        'colorScheme': {
            'name': 'gradient',
            'args': {
                'initialColor': 'red',
            },
        },
        'legend': {
            'hide': True,
        },
        'title': 'Sample Chart'
    }
    chart = chartFactory(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        output = sys.argv[1]
    else:
        output = 'stackedbarchart.png'
    stackedBarChart('v' + output, pycha.stackedbar.StackedVerticalBarChart)
    stackedBarChart('h' + output, pycha.stackedbar.StackedHorizontalBarChart)
