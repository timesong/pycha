# Copyright(c) 2009 by Yaco S.L. <lgs@yaco.es>
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

from pycha.bar import BarChart, VerticalBarChart, HorizontalBarChart, Rect
from pycha.chart import uniqueIndices


class HistogramChart(BarChart):

    def __init__(self, surface=None, options={}, debug=False):
        super(HistogramChart, self).__init__(surface, options, debug)
        self.barWidth = 0.0

class HistogramVerticalBarChart(HistogramChart, VerticalBarChart):

    def _updateChart(self):
        """Evaluates measures for vertical bars"""
        super(HistogramVerticalBarChart, self)._updateChart()

        accumulated_heights = {}
        for i, (name, store) in enumerate(self.datasets):
            for item in store:
                xval, yval = item
                x = ((xval - self.minxval) * self.xscale) + self.barMargin
                w = self.barWidth
                h = abs(yval) * self.yscale
                if yval > 0:
                    y = (1.0 - h) - self.origin
                else:
                    y = 1 - self.origin

                accumulated_height = accumulated_heights.setdefault(xval, 0)
                y -= accumulated_height
                accumulated_heights[xval] += h

                rect = Rect(x, y, w, h, xval, yval, name)

                if (0.0 <= rect.x <= 1.0) and (0.0 <= rect.y <= 1.0):
                    self.bars.append(rect)


class HistogramHorizontalBarChart(HistogramChart, HorizontalBarChart):

    def _updateChart(self):
        """Evaluates measures for horizontal bars"""
        super(HistogramHorizontalBarChart, self)._updateChart()

        accumulated_widths = {}
        for i, (name, store) in enumerate(self.datasets):
            for item in store:
                xval, yval = item
                y = ((xval - self.minxval) * self.xscale) + self.barMargin
                h = self.barWidth
                w = abs(yval) * self.yscale
                if yval > 0:
                    x = self.origin
                else:
                    x = self.origin - w

                accumulated_width = accumulated_widths.setdefault(xval, 0)
                x += accumulated_width
                accumulated_widths[xval] += w

                rect = Rect(x, y, w, h, xval, yval, name)

                if (0.0 <= rect.x <= 1.0) and (0.0 <= rect.y <= 1.0):
                    self.bars.append(rect)
