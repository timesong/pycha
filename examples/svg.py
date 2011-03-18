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

import pycha.bar

def testBar():
    surface = cairo.SVGSurface("testsvg.svg", 500, 300)

    options = {
        'legend': {
            'position': {
                'left': 330
                }
            },
        }

    chart = pycha.bar.VerticalBarChart(surface, options)

    dataSet = (
        ('myFirstDataset', [[0, 1], [1, 1], [2, 1.414], [3, 1.73]]),
        ('mySecondDataset', [[0, 0.3], [1, 2.67], [2, 1.34], [3, 1.73]]),
        ('myThirdDataset', [[0, 0.46], [1, 1.45], [2, 2.5], [3, 1.2]]),
        ('myFourthDataset', [[0, 0.86], [1, 0.83], [2, 3], [3, 1.73]]),
    )

    chart.addDataset(dataSet)
    chart.render()

    surface.flush()

if __name__ == '__main__':
    testBar()
