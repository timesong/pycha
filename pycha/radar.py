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

import math

import cairo

from pycha.chart import Chart, Option, Layout, Area, get_text_extents
from pycha.color import hex2rgb

class RadarChart(Chart):
    def __init__(self, surface=None, options={}, debug=False):
        super(RadarChart, self).__init__(surface, options, debug)
        self.start_angle = 0
        self.direction = "clockwise"
        self.number = 0
        self.slice = 5
        # self.frame = 'polygon' # 'circle'
        self.frame = 'circle'

    def _updateChart(self):
        for i, (name, store) in enumerate(self.datasets):
            self.number = max(len(store), self.number)

        w, h = self.getSurfaceSize()
        self.centerx = w * 0.5
        self.centery = h * 0.5

    def _renderLines(self, cx):
        """Aux function for _renderBackground"""
        radius = min(self.layout.chart.w * 0.5, self.layout.chart.h * 0.5)

        cx.save()
        cx.set_source_rgb(*hex2rgb(self.options.axis.lineColor))
        # cx.arc(self.centerx, self.centery, 5.0, 0, 2*math.pi)

        angle = self.start_angle * math.pi / 180
        direction = self.direction == "clockwise" and -1 or 1
        angle_between = direction*(2 * math.pi) / float(self.number)

        for i in xrange(self.number):
            car = math.cos(angle) * radius
            sar = math.sin(angle) * radius

            cx.move_to(self.centerx, self.centery)
            cx.line_to(self.centerx + car, self.centery + sar)
            cx.show_text(str(self.xticks[i][-1]))

            angle += angle_between
        
        cr = radius / float(self.slice)

        if self.frame == 'circle':
            for i in xrange(self.slice):
                cx.move_to(self.centerx, self.centery)
                cx.arc(self.centerx, self.centery, (i+1) * cr, 0, 2*math.pi)
                cx.move_to(self.centerx + (i+1) * cr, self.centery)
                cx.show_text(str(self.maxyval / self.slice * i))
        else:
            for i in xrange(self.slice):
                angle = self.start_angle * math.pi / 180

                for j in xrange(self.number):
                    x = self.centerx + math.cos(angle) * (i+1) * cr
                    y = self.centery + math.sin(angle) * (i+1) * cr

                    if j:
                        cx.line_to(x, y)
                    else:
                        cx.move_to(x, y)

                    angle += angle_between
                cx.close_path()
                
                cx.move_to(self.centerx + (i+1) * cr, self.centery)
                cx.show_text(str(self.maxyval / self.slice * i))

        cx.stroke()
        cx.restore()

    def _renderChart(self, cx):
        """Renders a pie chart"""
        cx.set_line_join(cairo.LINE_JOIN_ROUND)

        cx.save()
        cx.set_line_width(5)

        radius = min(self.layout.chart.w * 0.5, self.layout.chart.h * 0.5)

        for name, store in self.datasets:
            n = len(store)
            angle = self.start_angle * math.pi / 180
            direction = self.direction == "clockwise" and -1 or 1
            angle_between = direction * (2 * math.pi) / float(n)
            cx.set_source_rgb(*self.colorScheme[name])
            firstPoint = True

            for xval, yval in store:
                r = (yval / self.maxyval) * radius
                x = self.centerx + math.cos(angle) * r
                y = self.centery + math.sin(angle) * r

                if firstPoint == True:
                    cx.move_to(x, y)
                    firstPoint = False
                else:
                    cx.line_to(x, y)

                angle += angle_between
            cx.close_path()

        cx.stroke()

        cx.restore()

    def _renderAxis(self, cx):
        pass

if __name__ == '__main__':
    import sys
    import cairo

    lines = (
        ('bar.py', 319),
        ('chart.py', 875),
        ('color.py', 204),
        ('line.py', 130),
        ('pie.py', 352),
        ('scatter.py', 38),
        ('stackedbar.py', 121),
        ('radar.py', 184),
    )

    def MyRadarChart(output):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
        dataSet = (
            ('lines', [(i, l[1]) for i, l in enumerate(lines)]),
        )

        options = {
            'axis': {
                'x': {
                    'ticks': [dict(v=i, label=d[0]) for i, d in enumerate(lines)],
                }
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
        }
        chart = RadarChart(surface, options)

        chart.addDataset(dataSet)
        chart.render()

        surface.write_to_png(output)

    if len(sys.argv) > 1:
        output = sys.argv[1]
    else:
        output = 'radarchart.png'
    MyRadarChart(output)
