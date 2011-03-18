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

import unittest

import cairo

import pycha.bar


class RectTests(unittest.TestCase):

    def test_rect(self):
        r = pycha.bar.Rect(2, 3, 20, 40, 2.5, 3.4, 'test')
        self.assertEqual(r.x, 2)
        self.assertEqual(r.y, 3)
        self.assertEqual(r.w, 20)
        self.assertEqual(r.h, 40)
        self.assertEqual(r.xval, 2.5)
        self.assertEqual(r.yval, 3.4)
        self.assertEqual(r.name, 'test')


class BarTests(unittest.TestCase):

    def test_init(self):
        ch = pycha.bar.BarChart(None)
        self.assertEqual(ch.bars, [])
        self.assertEqual(ch.minxdelta, 0)

    def test_updateChart(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        # An evil dataset with just one point. See bug #9
        dataset = (
            ('dataset1', ([0, 0], )),
        )
        ch = pycha.bar.BarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()

        self.assertEqual(ch.xscale, 1.0)
        self.assertEqual(ch.minxval, 0)
        self.assertEqual(ch.minxdelta, 1.0)
        self.assertAlmostEqual(ch.barWidthForSet, 0.75, 4)
        self.assertAlmostEqual(ch.barMargin, 0.125, 4)

    def test_customRangeWithOnePoint(self):
        """Weird results with a custom range and just one point. See bug #20"""
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)

        dataset = (
            ('dataset1', ([0, 1], )),
        )
        options = {
            'axis': {
                'x': {
                    'range': (0.0, 4.0),
                    },
                },
            }
        ch = pycha.bar.BarChart(surface, options)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()

        self.assertEqual(ch.xscale, 0.2)
        self.assertEqual(ch.minxval, 0)
        self.assertEqual(ch.minxdelta, 1.0)
        self.assertAlmostEqual(ch.barWidthForSet, 0.15, 2)
        self.assertAlmostEqual(ch.barMargin, 0.025, 3)


class VerticalBarTests(unittest.TestCase):

    def test_updateChart(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, 3], [1, 4], [2, 2], [3, 5], [4, 3.5])),
            ('dataset2', ([0, 2], [1, 3], [2, 1], [3, 5], [4, 2.5])),
            )
        ch = pycha.bar.VerticalBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        self.assertEqual(ch.minxval, 0)
        self.assertEqual(ch.maxxval, 4)
        self.assertEqual(ch.xrange, 4)
        self.assertAlmostEqual(ch.xscale, 0.20, 4)
        self.assertEqual(ch.minyval, 0)
        self.assertEqual(ch.maxyval, 5)
        self.assertEqual(ch.yrange, 5)
        self.assertAlmostEqual(ch.yscale, 0.20, 4)
        self.assertEqual(ch.minxdelta, 1)
        self.assertAlmostEqual(ch.barWidthForSet, 0.075, 4)
        self.assertAlmostEqual(ch.barMargin, 0.025, 4)

        R = pycha.bar.Rect
        bars = (
            R(0.025, 0.400, 0.075, 0.600, 0, 3, 'dataset1'),
            R(0.225, 0.200, 0.075, 0.800, 1, 4, 'dataset1'),
            R(0.425, 0.600, 0.075, 0.400, 2, 2, 'dataset1'),
            R(0.625, 0.000, 0.075, 1.000, 3, 5, 'dataset1'),
            R(0.825, 0.300, 0.075, 0.700, 4, 3.5, 'dataset1'),

            R(0.100, 0.600, 0.075, 0.400, 0, 2, 'dataset2'),
            R(0.300, 0.400, 0.075, 0.600, 1, 3, 'dataset2'),
            R(0.500, 0.800, 0.075, 0.200, 2, 1, 'dataset2'),
            R(0.700, 0.000, 0.075, 1.000, 3, 5, 'dataset2'),
            R(0.900, 0.500, 0.075, 0.500, 4, 2.5, 'dataset2'),
            )

        for i, bar in enumerate(bars):
            b1, b2 = ch.bars[i], bar
            self.assertAlmostEqual(b1.x, b2.x, 4)
            self.assertAlmostEqual(b1.y, b2.y, 4)
            self.assertAlmostEqual(b1.w, b2.w, 4)
            self.assertAlmostEqual(b1.h, b2.h, 4)
            self.assertEqual(b1.xval, b2.xval)
            self.assertEqual(b1.yval, b2.yval)
            self.assertEqual(b1.name, b2.name)

    def test_updateChartWithNegatives(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, -3], [1, -1], [2, 3], [3, 5])),
            )
        ch = pycha.bar.VerticalBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        self.assertEqual(ch.minxval, 0)
        self.assertEqual(ch.maxxval, 3)
        self.assertEqual(ch.xrange, 3)
        self.assertAlmostEqual(ch.xscale, 0.25, 4)
        self.assertEqual(ch.minyval, -3)
        self.assertEqual(ch.maxyval, 5)
        self.assertEqual(ch.yrange, 8)
        self.assertAlmostEqual(ch.yscale, 0.125, 4)
        self.assertAlmostEqual(ch.origin, 0.375)
        self.assertEqual(ch.minxdelta, 1)
        self.assertAlmostEqual(ch.barWidthForSet, 0.1875, 4)
        self.assertAlmostEqual(ch.barMargin, 0.03125, 4)

        R = pycha.bar.Rect
        bars = (
            R(0.03125, 0.625, 0.1875, 0.375, 0, -3, 'dataset1'),
            R(0.28125, 0.625, 0.1875, 0.125, 1, -1, 'dataset1'),
            R(0.53125, 0.250, 0.1875, 0.375, 2, 3, 'dataset1'),
            R(0.78125, 0.000, 0.1875, 0.625, 3, 5, 'dataset1'),
            )

        for i, bar in enumerate(bars):
            b1, b2 = ch.bars[i], bar
            self.assertAlmostEqual(b1.x, b2.x, 4)
            self.assertAlmostEqual(b1.y, b2.y, 4)
            self.assertAlmostEqual(b1.w, b2.w, 4)
            self.assertAlmostEqual(b1.h, b2.h, 4)
            self.assertEqual(b1.xval, b2.xval)
            self.assertEqual(b1.yval, b2.yval)
            self.assertEqual(b1.name, b2.name)

    def test_updateTicks(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, 1], [1, 1], [2, 3])),
            ('dataset2', ([0, 2], [1, 0], [3, 4])),
            )
        ch = pycha.bar.VerticalBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        ch._updateTicks()
        xticks = [(0.125, 0), (0.375, 1), (0.625, 2)]
        for i in range(len(xticks)):
            self.assertAlmostEqual(ch.xticks[i][0], xticks[i][0], 4)
            self.assertAlmostEqual(ch.xticks[i][1], xticks[i][1], 4)

        yticks = [
            (1.0, 0.0), (0.9, 0.4), (0.8, 0.8), (0.7, 1.2), (0.6, 1.6),
            (0.5, 2.0), (0.4, 2.4), (0.3, 2.8), (0.2, 3.2), (0.1, 3.6),
            (0.0, 4.0),
            ]
        for i in range(len(yticks)):
            self.assertAlmostEqual(ch.yticks[i][0], yticks[i][0], 4)
            self.assertAlmostEqual(ch.yticks[i][1], yticks[i][1], 4)

    def test_udpateTicksWithNegatives(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, -2], [1, 1], [2, 3])),
            )
        ch = pycha.bar.VerticalBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        ch._updateTicks()
        xticks = [(0.1667, 0), (0.5000, 1), (0.8333, 2)]
        for i in range(len(xticks)):
            self.assertAlmostEqual(ch.xticks[i][0], xticks[i][0], 4)
            self.assertAlmostEqual(ch.xticks[i][1], xticks[i][1], 4)

        yticks = [
            (1.0, -2.0), (0.9, -1.5), (0.8, -1.0), (0.7, -0.5), (0.6, 0.0),
            (0.5, 0.5), (0.4, 1.0), (0.3, 1.5), (0.2, 2.0), (0.1, 2.5),
            (0.0, 3.0),
            ]
        for i in range(len(yticks)):
            self.assertAlmostEqual(ch.yticks[i][0], yticks[i][0], 4)
            self.assertAlmostEqual(ch.yticks[i][1], yticks[i][1], 4)

    def test_shadowRectangle(self):
        ch = pycha.bar.VerticalBarChart(None)
        shadow = ch._getShadowRectangle(10, 20, 400, 300)
        self.assertEqual(shadow, (8, 18, 404, 302))


class HorizontalBarTests(unittest.TestCase):

    def test_updateChart(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, 1], [1, 1], [2, 3])),
            ('dataset2', ([0, 2], [1, 0], [3, 4])),
            )
        ch = pycha.bar.HorizontalBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        self.assertEqual(ch.xrange, 3)
        self.assertAlmostEqual(ch.xscale, 0.25, 4)
        self.assertAlmostEqual(ch.yscale, 0.25, 4)
        self.assertEqual(ch.minxdelta, 1)
        self.assertAlmostEqual(ch.barWidthForSet, 0.09375, 4)
        self.assertAlmostEqual(ch.barMargin, 0.03125, 4)

        bars = (
            pycha.bar.Rect(0, 0.03125, 0.25, 0.09375, 0, 1, 'dataset1'),
            pycha.bar.Rect(0, 0.28125, 0.25, 0.09375, 1, 1, 'dataset1'),
            pycha.bar.Rect(0, 0.53125, 0.75, 0.09375, 2, 3, 'dataset1'),

            pycha.bar.Rect(0, 0.125, 0.5, 0.09375, 0, 2, 'dataset2'),
            pycha.bar.Rect(0, 0.375, 0.0, 0.09375, 1, 0, 'dataset2'),
            pycha.bar.Rect(0, 0.875, 1.0, 0.09375, 3, 4, 'dataset2'),
            )

        for i, bar in enumerate(bars):
            b1, b2 = ch.bars[i], bar
            self.assertAlmostEqual(b1.x, b2.x, 4)
            self.assertAlmostEqual(b1.y, b2.y, 4)
            self.assertAlmostEqual(b1.w, b2.w, 4)
            self.assertAlmostEqual(b1.h, b2.h, 4)
            self.assertEqual(b1.xval, b2.xval)
            self.assertEqual(b1.yval, b2.yval)
            self.assertEqual(b1.name, b2.name)

    def test_updateChartWithNegatives(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, -3], [1, -1], [2, 3], [3, 5])),
            )

        ch = pycha.bar.HorizontalBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        self.assertEqual(ch.minxval, 0)
        self.assertEqual(ch.maxxval, 3)
        self.assertEqual(ch.xrange, 3)
        self.assertAlmostEqual(ch.xscale, 0.25, 4)
        self.assertEqual(ch.minyval, -3)
        self.assertEqual(ch.maxyval, 5)
        self.assertEqual(ch.yrange, 8)
        self.assertAlmostEqual(ch.yscale, 0.125, 4)
        self.assertAlmostEqual(ch.origin, 0.375)
        self.assertEqual(ch.minxdelta, 1)
        self.assertAlmostEqual(ch.barWidthForSet, 0.1875, 4)
        self.assertAlmostEqual(ch.barMargin, 0.03125, 4)

        R = pycha.bar.Rect
        bars = (
            R(0.000, 0.03125, 0.375, 0.1875, 0, -3, 'dataset1'),
            R(0.250, 0.28125, 0.125, 0.1875, 1, -1, 'dataset1'),
            R(0.375, 0.53125, 0.375, 0.1875, 2, 3, 'dataset1'),
            R(0.375, 0.78125, 0.625, 0.1875, 3, 5, 'dataset1'),
            )

        for i, bar in enumerate(bars):
            b1, b2 = ch.bars[i], bar
            self.assertAlmostEqual(b1.x, b2.x, 4)
            self.assertAlmostEqual(b1.y, b2.y, 4)
            self.assertAlmostEqual(b1.w, b2.w, 4)
            self.assertAlmostEqual(b1.h, b2.h, 4)
            self.assertEqual(b1.xval, b2.xval)
            self.assertEqual(b1.yval, b2.yval)
            self.assertEqual(b1.name, b2.name)

    def test_updateTicks(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, 1], [1, 1], [2, 3])),
            ('dataset2', ([0, 2], [1, 0], [3, 4])),
            )
        ch = pycha.bar.HorizontalBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        ch._updateTicks()

        xticks = [
            (0.0, 0.0), (0.1, 0.4), (0.2, 0.8), (0.3, 1.2), (0.4, 1.6),
            (0.5, 2.0), (0.6, 2.4), (0.7, 2.8), (0.8, 3.2), (0.9, 3.6),
            (1.0, 4.0),
            ]
        for i in range(len(xticks)):
            self.assertAlmostEqual(ch.xticks[i][0], xticks[i][0], 4)
            self.assertAlmostEqual(ch.xticks[i][1], xticks[i][1], 4)

        yticks = [(0.125, 0), (0.375, 1), (0.625, 2)]
        for i in range(len(yticks)):
            self.assertAlmostEqual(ch.yticks[i][0], yticks[i][0], 4)
            self.assertAlmostEqual(ch.yticks[i][1], yticks[i][1], 4)

    def test_udpateTicksWithNegatives(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, -2], [1, 1], [2, 3])),
            )
        ch = pycha.bar.HorizontalBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        ch._updateTicks()
        xticks = [
            (0.0, -2.0), (0.1, -1.5), (0.2, -1.0), (0.3, -0.5), (0.4, 0.0),
            (0.5, 0.5), (0.6, 1.0), (0.7, 1.5), (0.8, 2.0), (0.9, 2.5),
            (1.0, 3.0),
            ]
        for i in range(len(xticks)):
            self.assertAlmostEqual(ch.xticks[i][0], xticks[i][0], 4)
            self.assertAlmostEqual(ch.xticks[i][1], xticks[i][1], 4)

        yticks = [(0.1667, 0), (0.5000, 1), (0.8333, 2)]
        for i in range(len(yticks)):
            self.assertAlmostEqual(ch.yticks[i][0], yticks[i][0], 4)
            self.assertAlmostEqual(ch.yticks[i][1], yticks[i][1], 4)

    def test_shadowRectangle(self):
        ch = pycha.bar.HorizontalBarChart(None)
        shadow = ch._getShadowRectangle(10, 20, 400, 300)
        self.assertEqual(shadow, (10, 18, 402, 304))


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(RectTests),
        unittest.makeSuite(BarTests),
        unittest.makeSuite(VerticalBarTests),
        unittest.makeSuite(HorizontalBarTests),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
