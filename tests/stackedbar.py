# Copyright (c) 2009-2010 by Yaco S.L. <lgs@yaco.es>
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

import pycha.stackedbar


class StackedBarTests(unittest.TestCase):

    def test_init(self):
        ch = pycha.stackedbar.StackedBarChart(None)
        self.assertEqual(ch.barWidth, 0.0)

    def test_updateXY(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ((0, 1), (1, 2))),
            ('dataset2', ((0, 3), (1, 1))),
        )
        ch = pycha.stackedbar.StackedBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()

        self.assertEqual(ch.yrange, 4.0)
        self.assertAlmostEqual(ch.yscale, 0.25)

    def test_updateChart(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ((0, 1), (1, 2))),
            ('dataset2', ((0, 3), (1, 1))),
        )
        ch = pycha.stackedbar.StackedBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()

        self.assertEqual(ch.minxdelta, 1)
        self.assertAlmostEqual(ch.barWidth, 0.375, 3)
        self.assertAlmostEqual(ch.barMargin, 0.0625, 4)


class StackedVerticalBarTests(unittest.TestCase):

    def test_updateChart(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, 3], [1, 4], [2, 2], [3, 5], [4, 3.5])),
            ('dataset2', ([0, 2], [1, 3], [2, 1], [3, 5], [4, 2.5])),
            )
        ch = pycha.stackedbar.StackedVerticalBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        self.assertEqual(ch.minxval, 0)
        self.assertEqual(ch.maxxval, 4)
        self.assertEqual(ch.xrange, 4)
        self.assertAlmostEqual(ch.xscale, 0.20, 4)
        self.assertEqual(ch.minyval, 0)
        self.assertEqual(ch.maxyval, 5)
        self.assertEqual(ch.yrange, 10)
        self.assertAlmostEqual(ch.yscale, 0.10, 4)
        self.assertEqual(ch.minxdelta, 1)
        self.assertAlmostEqual(ch.barWidth, 0.150, 4)
        self.assertAlmostEqual(ch.barMargin, 0.025, 4)

        R = pycha.bar.Rect
        bars = (
            R(0.025, 0.700, 0.150, 0.300, 0, 3, 'dataset1'),
            R(0.225, 0.600, 0.150, 0.400, 1, 4, 'dataset1'),
            R(0.425, 0.800, 0.150, 0.200, 2, 2, 'dataset1'),
            R(0.625, 0.500, 0.150, 0.500, 3, 5, 'dataset1'),
            R(0.825, 0.650, 0.150, 0.350, 4, 3.5, 'dataset1'),

            R(0.025, 0.500, 0.150, 0.200, 0, 2, 'dataset2'),
            R(0.225, 0.300, 0.150, 0.300, 1, 3, 'dataset2'),
            R(0.425, 0.700, 0.150, 0.100, 2, 1, 'dataset2'),
            R(0.625, 0.000, 0.150, 0.500, 3, 5, 'dataset2'),
            R(0.825, 0.400, 0.150, 0.250, 4, 2.5, 'dataset2'),
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
        ch = pycha.stackedbar.StackedVerticalBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        ch._updateTicks()
        xticks = [(0.125, 0), (0.375, 1), (0.625, 2)]
        for i in range(len(xticks)):
            self.assertAlmostEqual(ch.xticks[i][0], xticks[i][0], 4)
            self.assertAlmostEqual(ch.xticks[i][1], xticks[i][1], 4)

        yticks = [
            (1.0, 0.0), (0.9, 0.7), (0.8, 1.4), (0.7, 2.1), (0.6, 2.8),
            (0.5, 3.5), (0.4, 4.2), (0.3, 4.9), (0.2, 5.6),
            (0.1, 6.3), (0.0, 7.0),
            ]
        for i in range(len(yticks)):
            self.assertAlmostEqual(ch.yticks[i][0], yticks[i][0], 4)
            self.assertAlmostEqual(ch.yticks[i][1], yticks[i][1], 4)


class StackedHorizontalBarTests(unittest.TestCase):

    def test_updateChart(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, 1], [1, 1], [2, 3])),
            ('dataset2', ([0, 2], [1, 0], [2, 4])),
            )
        ch = pycha.stackedbar.StackedHorizontalBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        self.assertEqual(ch.xrange, 2)
        self.assertAlmostEqual(ch.xscale, 0.3333, 4)
        self.assertAlmostEqual(ch.yscale, 0.1429, 4)
        self.assertEqual(ch.minxdelta, 1)
        self.assertAlmostEqual(ch.barWidth, 0.25, 4)
        self.assertAlmostEqual(ch.barMargin, 0.0417, 4)

        bars = (
            pycha.bar.Rect(0, 0.0417, 0.1429, 0.25, 0, 1, 'dataset1'),
            pycha.bar.Rect(0, 0.3750, 0.1429, 0.25, 1, 1, 'dataset1'),
            pycha.bar.Rect(0, 0.7083, 0.4286, 0.25, 2, 3, 'dataset1'),

            pycha.bar.Rect(0.1429, 0.0417, 0.2857, 0.25, 0, 2, 'dataset2'),
            pycha.bar.Rect(0.1429, 0.3750, 0.0000, 0.25, 1, 0, 'dataset2'),
            pycha.bar.Rect(0.4286, 0.7083, 0.5714, 0.25, 2, 4, 'dataset2'),
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
            ('dataset2', ([0, 2], [1, 0], [2, 4])),
            )
        ch = pycha.stackedbar.StackedHorizontalBarChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        ch._updateTicks()

        xticks = [
            (0.0, 0.0), (0.1, 0.7), (0.2, 1.4), (0.3, 2.1),
            (0.4, 2.8), (0.5, 3.5), (0.6, 4.2), (0.7, 4.9),
            (0.8, 5.6), (0.9, 6.3), (1.0, 7.0),
            ]
        for i in range(len(xticks)):
            self.assertAlmostEqual(ch.xticks[i][0], xticks[i][0], 4)
            self.assertAlmostEqual(ch.xticks[i][1], xticks[i][1], 4)

        yticks = [(0.1667, 0), (0.5, 1), (0.8333, 2)]
        for i in range(len(yticks)):
            self.assertAlmostEqual(ch.yticks[i][0], yticks[i][0], 4)
            self.assertAlmostEqual(ch.yticks[i][1], yticks[i][1], 4)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(StackedBarTests),
        unittest.makeSuite(StackedVerticalBarTests),
        unittest.makeSuite(StackedHorizontalBarTests),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
