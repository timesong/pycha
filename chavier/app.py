# Copyright(c) 2007-2010 by Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
#
# This file is part of Chavier.
#
# Chavier is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Chavier is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Chavier.  If not, see <http://www.gnu.org/licenses/>.

import cairo

from pycha.chart import DEFAULT_OPTIONS
from pycha.bar import HorizontalBarChart, VerticalBarChart
from pycha.line import LineChart
from pycha.pie import PieChart
from pycha.scatter import ScatterplotChart
from pycha.stackedbar import StackedVerticalBarChart, StackedHorizontalBarChart

from chavier.gui import GUI


class App(object):

    CHART_TYPES = (
        VerticalBarChart,
        HorizontalBarChart,
        LineChart,
        PieChart,
        ScatterplotChart,
        StackedVerticalBarChart,
        StackedHorizontalBarChart,
        )

    (VERTICAL_BAR_TYPE,
     HORIZONTAL_BAR_TYPE,
     LINE_TYPE,
     PIE_TYPE,
     SCATTER_TYPE,
     STACKED_VERTICAL_BAR_TYPE,
     STACKED_HORIZONTAL_BAR_TYPE) = range(len(CHART_TYPES))

    OPTIONS_TYPES = dict(
        axis=dict(
            lineWidth=float,
            lineColor=str,
            tickSize=float,
            labelColor=str,
            labelFont=str,
            labelFontSize=int,
            labelWidth=float,
            tickFont=str,
            tickFontSize=int,
            x=dict(
                hide=bool,
                ticks=list,
                tickCount=int,
                tickPrecision=int,
                range=list,
                rotate=float,
                label=unicode,
                interval=int,
                showLines=bool,
                ),
            y=dict(
                hide=bool,
                ticks=list,
                tickCount=int,
                tickPrecision=int,
                range=list,
                rotate=float,
                label=unicode,
                interval=int,
                showLines=bool,
                ),
            ),
        background=dict(
            hide=bool,
            baseColor=str,
            chartColor=str,
            lineColor=str,
            lineWidth=float,
            ),
        legend=dict(
            opacity=float,
            borderColor=str,
            borderWidth=int,
            hide=bool,
            position=dict(
                top=int,
                left=int,
                bottom=int,
                right=int,
                )
            ),
        padding=dict(
            left=int,
            right=int,
            top=int,
            bottom=int,
            ),
        stroke=dict(
            color=str,
            hide=bool,
            shadow=bool,
            width=int,
            ),
        yvals=dict(
            show=bool,
            inside=bool,
            fontSize=int,
            fontColor=str,
            skipSmallValues=bool,
            snapToOrigin=bool,
            renderer=str,
            ),
        fillOpacity=float,
        shouldFill=bool,
        barWidthFillFraction=float,
        pieRadius=float,
        colorScheme=dict(
            name=str,
            args=dict(
                initialColor=str,
                colors=list,
                ),
            ),
        title=unicode,
        titleColor=str,
        titleFont=str,
        titleFontSize=int,
        encoding=str,
        )

    def __init__(self):
        self.gui = GUI(self)

    def run(self):
        self.gui.run()

    def get_default_options(self):
        return DEFAULT_OPTIONS

    def get_chart(self, datasets, options, chart_type, width, height):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        chart_factory = self.CHART_TYPES[chart_type]
        chart = chart_factory(surface, options)
        chart.addDataset(datasets)
        chart.render()
        return chart


def main():
    app = App()
    app.run()
    return 0

if __name__ == '__main__':
    main()
