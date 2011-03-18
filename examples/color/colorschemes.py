# Copyright(c) 2007-2010 by Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
#              2009 by Yaco S.L. <lgs@yaco.es>
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

import pycha.pie


def pieChart(colorScheme):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 400)

    options = {
        'background': {
            'hide': True,
        },
        'colorScheme': colorScheme,
        'title': colorScheme['name'],
    }
    chart = pycha.pie.PieChart(surface, options)

    dataSet = (
        ('dataset 1', ((0, 10), )),
        ('dataset 2', ((0, 15), )),
        ('dataset 3', ((0, 20), )),
        ('dataset 4', ((0, 25), )),
        ('dataset 5', ((0, 30), )),
        ('dataset 6', ((0, 20), )),
        ('dataset 7', ((0, 40), )),
        )

    chart.addDataset(dataSet)
    chart.render()

    output = colorScheme['name'] + '.png'
    surface.write_to_png(output)

if __name__ == '__main__':
    pieChart({'name': 'gradient', 'args': {'initialColor': 'red'}})

    colors = ('#ff0000', '#00ff00', '#0000ff',
              '#00ffff', '#000000', '#ff00ff',
              '#ffff00')
    pieChart({'name': 'fixed', 'args': {'colors': colors}})

    pieChart({'name': 'rainbow', 'args': {'initialColor': 'red'}})
