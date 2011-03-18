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

import pycha.line


def intervalExample():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 400)

    dataSet = (
        ('dataset 1', [(0, 10), (1, 20), (2, 45), (3, 33)]),
        ('dataset 2', [(0, 14), (1, 18), (2, 32), (3, 21)]),
        )

    options = {
        'axis': {
            'x': {
                'interval': 0.5,
                },
            'y': {
                'interval': 5,
                },
            },
        'legend': {
            'hide': True,
            },
        'title': 'Interval example',
        'background': {
            'baseColor': '#f0f0f0',
            },
        'shouldFill': False,
    }
    chart = pycha.line.LineChart(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png("interval.png")


if __name__ == '__main__':
    intervalExample()
