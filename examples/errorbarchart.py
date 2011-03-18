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

import pycha.bar


def barChart(output, chartFactory):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 400)

    # note that this dataset is composed by triplets, where the
    # third item is the error
    dataSet = (
        ('data 1', [(0, 30, 5), (1, 40, 7), (2, 25, 3), (3, 50, 10)]),
        )

    options = {
        'background': {
            'chartColor': '#ffeeff',
            'baseColor': '#ffffff',
            'lineColor': '#444444',
        },
        'legend': {
            'hide': True,
        },
        'title': 'Error bars'
    }
    chart = chartFactory(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        output = sys.argv[1]
    else:
        output = 'errorbars.png'
    barChart('v' + output, pycha.bar.VerticalBarChart)
    barChart('h' + output, pycha.bar.HorizontalBarChart)
