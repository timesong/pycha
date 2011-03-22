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
    def __init__(self, surface=None, options={}, frame='circle', debug=False):
        """ frame equal 'polygon' or 'circle' """
        super(RadarChart, self).__init__(surface, options, debug)
        self.slice = self.options.axis.y.tickCount
        self.frame = frame
        self.layout = RadarLayout()

    def _updateChart(self):
        pass

    def _renderLines(self, cx):
        """Aux function for _renderBackground"""
        centerx = self.layout.chart.x + self.layout.chart.w * 0.5
        centery = self.layout.chart.y + self.layout.chart.h * 0.5

        cx.set_line_width(self.options.background.lineWidth)
        cx.set_source_rgb(*hex2rgb(self.options.background.lineColor))

        for angle in self.layout.angles:
            car = math.cos(angle) * self.layout.radius
            sar = math.sin(angle) * self.layout.radius

            cx.move_to(centerx, centery)
            cx.line_to(centerx + car, centery + sar)

        cx.stroke()

    def _renderChart(self, cx):
        """Renders a radar chart"""
        cx.set_line_join(cairo.LINE_JOIN_ROUND)

        cx.save()
        cx.set_line_width(self.options.stroke.width)

        centerx = self.layout.chart.x + self.layout.chart.w * 0.5
        centery = self.layout.chart.y + self.layout.chart.h * 0.5

        for name, store in self.datasets:
            cx.set_source_rgb(*self.colorScheme[name])
            firstPoint = True
            angels = self.layout.angles
            angels.reverse()

            for i, angle in enumerate(angels[:-1]):
                xval, yval = store[i]
                r = (yval / self.maxyval) * self.layout.radius
                x = centerx + math.cos(angle) * r
                y = centery + math.sin(angle) * r

                if firstPoint == True:
                    cx.move_to(x, y)
                    firstPoint = False
                else:
                    cx.line_to(x, y)
                    
                # cx.show_text(str(yval))

            cx.close_path()

        cx.stroke()

        cx.restore()

    def _renderAxis(self, cx):
        """Renders the axis for radar charts"""
        if self.options.axis.x.hide or not self.xticks:
            return

        self.xlabels = []

        if self.debug:
            px = max(cx.device_to_user_distance(1, 1))
            cx.set_source_rgba(0, 0, 1, 0.5)
            for x, y, w, h in self.layout.ticks:
                cx.rectangle(x, y, w, h)
                cx.stroke()
                cx.arc(x + w / 2.0, y + h / 2.0, 5 * px, 0, 2 * math.pi)
                cx.fill()
                cx.arc(x, y, 2 * px, 0, 2 * math.pi)
                cx.fill()

        cx.select_font_face(self.options.axis.labelFont,
                            cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_NORMAL)
        cx.set_font_size(self.options.axis.labelFontSize)

        cx.set_source_rgb(*hex2rgb(self.options.axis.labelColor))

        for i, tick in enumerate(self.xticks):
            label = tick[1]
            x, y, w, h = self.layout.ticks[i]

            xb, yb, width, height, xa, ya = cx.text_extents(label)

            # draw label with text tick[1]
            cx.move_to(x - xb, y - yb)
            cx.show_text(label)
            self.xlabels.append(label)
            
        # Draw y-axis

        centerx = self.layout.chart.x + self.layout.chart.w * 0.5
        centery = self.layout.chart.y + self.layout.chart.h * 0.5

        cr = self.layout.radius / float(self.slice)
        
        cx.set_line_width(self.options.axis.lineWidth)
        cx.set_source_rgb(*hex2rgb(self.options.axis.lineColor))

        if self.frame == 'circle':
            for i in xrange(self.slice):
                cx.move_to(centerx, centery)
                cx.arc(centerx, centery, (i+1) * cr, 0, 2*math.pi)
        else:
            for i in xrange(self.slice):
                for j, angle in enumerate(self.layout.angles):
                    x = centerx + math.cos(angle) * (i+1) * cr
                    y = centery + math.sin(angle) * (i+1) * cr

                    if j:
                        cx.line_to(x, y)
                    else:
                        cx.move_to(x, y)

                cx.close_path()

        cx.stroke()

        cx.select_font_face(self.options.axis.tickFont,
                            cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_NORMAL)
        cx.set_font_size(self.options.axis.tickFontSize)
        cx.set_source_rgb(*hex2rgb(self.options.axis.labelColor))

        for i in xrange(self.slice):
            yval = "%.1f" % (self.maxyval / self.slice * (i+1))
            tw, th = get_text_extents(cx, yval, self.options.axis.tickFont, self.options.axis.tickFontSize, self.options.encoding)
            tx = centerx + (i+1) * cr - tw

            cx.move_to(tx, centery+th)
            cx.show_text(yval)

class RadarLayout(Layout):
    """Set of chart areas for radar charts"""

    def __init__(self):
        self.title = Area()
        self.chart = Area()

        self.ticks = []
        self.radius = 0
        self.angles = []

        self._areas = (
            (self.title, (1, 126 / 255.0, 0)),  # orange
            (self.chart, (75 / 255.0, 75 / 255.0, 1.0)),  # blue
            )

        self._lines = []

    def update(self, cx, options, width, height, xticks, yticks):
        self.title.x = options.padding.left
        self.title.y = options.padding.top
        self.title.w = width - (options.padding.left + options.padding.right)
        self.title.h = get_text_extents(cx,
                                        options.title,
                                        options.titleFont,
                                        options.titleFontSize,
                                        options.encoding)[1]

        self.chart.x = self.title.x
        self.chart.y = self.title.y + self.title.h
        self.chart.w = self.title.w
        self.chart.h = height - self.title.h - (options.padding.top
                                                + options.padding.bottom)

        centerx = self.chart.x + self.chart.w * 0.5
        centery = self.chart.y + self.chart.h * 0.5

        angle = 0
        angle_between =(2 * math.pi) / len(xticks)
        self.angles = [angle]
        self.radius = min(self.chart.w / 2.0, self.chart.h / 2.0)

        for tick in xticks:
            width, height = get_text_extents(cx, tick[1],
                                             options.axis.tickFont,
                                             options.axis.tickFontSize,
                                             options.encoding)
            radius = self._get_min_radius(angle, centerx, centery,
                                          width, height)
            self.radius = min(self.radius, radius)
            angle += angle_between
            self.angles.append(angle)

        # Now that we now the radius we move the ticks as close as we can
        # to the circle
        for i, tick in enumerate(xticks):
            self.ticks[i] = self._get_tick_position(self.radius, self.angles[i],
                                                    self.ticks[i],
                                                    centerx, centery)

    def _get_min_radius(self, angle, centerx, centery, width, height):
        min_radius = None

        # precompute some common values
        tan = math.tan(angle)
        half_width = width / 2.0
        half_height = height / 2.0
        offset_x = half_width * tan
        offset_y = tan

        def intersect_horizontal_line(y):
            return centerx + (centery - y) / tan

        def intersect_vertical_line(x):
            return centery - tan * (x - centerx)

        # computes the intersection between the rect that has
        # that angle with the X axis and the bounding chart box
        if 0.25 * math.pi <= angle < 0.75 * math.pi:
            # intersects with the top rect
            y = self.chart.y
            x = intersect_horizontal_line(y)
            self._lines.append((x, y))

            x1 = x - half_width - offset_y
            self.ticks.append((x1, self.chart.y, width, height))

            min_radius = abs((y + height) - centery)
        elif 0.75 * math.pi <= angle < 1.25 * math.pi:
            # intersects with the left rect
            x = self.chart.x
            y = intersect_vertical_line(x)
            self._lines.append((x, y))

            y1 = y - half_height - offset_x
            self.ticks.append((x, y1, width, height))

            min_radius = abs(centerx - (x + width))
        elif 1.25 * math.pi <= angle < 1.75 * math.pi:
            # intersects with the bottom rect
            y = self.chart.y + self.chart.h
            x = intersect_horizontal_line(y)
            self._lines.append((x, y))

            x1 = x - half_width + offset_y
            self.ticks.append((x1, y - height, width, height))

            min_radius = abs((y - height) - centery)
        else:
            # intersects with the right rect
            x = self.chart.x + self.chart.w
            y = intersect_vertical_line(x)
            self._lines.append((x, y))

            y1 = y - half_height + offset_x
            self.ticks.append((x - width, y1, width, height))

            min_radius = abs((x - width) - centerx)

        return min_radius

    def _get_tick_position(self, radius, angle, tick, centerx, centery):
        text_width, text_height = tick[2:4]
        half_width = text_width / 2.0
        half_height = text_height / 2.0

        if 0 <= angle < 0.5 * math.pi:
            # first quadrant
            k1 = j1 = k2 = 1
            j2 = -1
        elif 0.5 * math.pi <= angle < math.pi:
            # second quadrant
            k1 = k2 = -1
            j1 = j2 = 1
        elif math.pi <= angle < 1.5 * math.pi:
            # third quadrant
            k1 = j1 = k2 = -1
            j2 = 1
        elif 1.5 * math.pi <= angle <= 2 * math.pi:
            # fourth quadrant
            k1 = k2 = 1
            j1 = j2 = -1

        cx = radius * math.cos(angle) + k1 * half_width
        cy = radius * math.sin(angle) + j1 * half_height

        radius2 = math.sqrt(cx * cx + cy * cy)

        tan = math.tan(angle)
        x = math.sqrt((radius2 * radius2) / (1 + tan * tan))
        y = tan * x

        x = centerx + k2 * x
        y = centery + j2 * y

        return x - half_width, y - half_height, text_width, text_height