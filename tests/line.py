# Copyright (c) 2007-2010 by Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
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

import pycha.line

class PointTests(unittest.TestCase):

    def test_point(self):
        point = pycha.line.Point(2, 3, 1.0, 2.0, "test")
        self.assertEqual(point.x, 2)
        self.assertEqual(point.y, 3)
        self.assertEqual(point.xval, 1.0)
        self.assertEqual(point.yval, 2.0)
        self.assertEqual(point.name, "test")

class LineTests(unittest.TestCase):

    def test_init(self):
        ch = pycha.line.LineChart(None)
        self.assertEqual(ch.points, [])

    def test_updateChart(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, 1], [1, 1], [2, 3])),
            ('dataset2', ([0, 2], [1, 0], [3, 4])),
            )
        ch = pycha.line.LineChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()

        self.assertEqual(ch.minxval, 0)
        self.assertEqual(ch.maxxval, 3)
        self.assertEqual(ch.xrange, 3)
        self.assertAlmostEqual(ch.xscale, 1/3.0, 4)
        self.assertEqual(ch.minyval, 0)
        self.assertEqual(ch.maxyval, 4)
        self.assertEqual(ch.yrange, 4)
        self.assertAlmostEqual(ch.yscale, 0.25, 4)

        points = (
            pycha.line.Point(0, 0.75, 0, 1, 'dataset1'),
            pycha.line.Point(1/3.0, 0.75, 1, 1, 'dataset1'),
            pycha.line.Point(2/3.0, 0.25, 2, 3, 'dataset1'),
            pycha.line.Point(0, 0.5, 0, 2, 'dataset2'),
            pycha.line.Point(1/3.0, 1, 1, 0, 'dataset2'),
            pycha.line.Point(1, 0, 3, 4, 'dataset2'),
        )
        for i, point in enumerate(points):
            p1, p2 = ch.points[i], point
            self.assertEqual(p1.x, p2.x)
            self.assertEqual(p1.y, p2.y)
            self.assertAlmostEqual(p1.xval, p2.xval, 4)
            self.assertAlmostEqual(p1.yval, p2.yval, 4)
            self.assertEqual(p1.name, p2.name)

    def test_updateChartWithNegatives(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, 1], [1, -2], [2, 3])),
            ('dataset2', ([0, 2], [1, 0], [3, -4])),
            )
        ch = pycha.line.LineChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        self.assertEqual(ch.minxval, 0)
        self.assertEqual(ch.maxxval, 3)
        self.assertEqual(ch.xrange, 3)
        self.assertAlmostEqual(ch.xscale, 1/3.0, 4)
        self.assertEqual(ch.minyval, -4)
        self.assertEqual(ch.maxyval, 3)
        self.assertEqual(ch.yrange, 7)
        self.assertAlmostEqual(ch.yscale, 1/7.0, 4)

        points = (
            pycha.line.Point(0, 0.2857, 0, 1, 'dataset1'),
            pycha.line.Point(1/3.0, 0.7143, 1, -2, 'dataset1'),
            pycha.line.Point(2/3.0, 0.0, 2, 3, 'dataset1'),
            pycha.line.Point(0, 0.1429, 0, 2, 'dataset2'),
            pycha.line.Point(1/3.0, 0.4286, 1, 0, 'dataset2'),
            pycha.line.Point(1, 1.0, 3, -4, 'dataset2'),
        )
        for i, point in enumerate(points):
            p1, p2 = ch.points[i], point
            self.assertAlmostEqual(p1.x, p2.x, 4)
            self.assertAlmostEqual(p1.y, p2.y, 4)
            self.assertAlmostEqual(p1.xval, p2.xval, 4)
            self.assertAlmostEqual(p1.yval, p2.yval, 4)
            self.assertEqual(p1.name, p2.name)

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(PointTests),
        unittest.makeSuite(LineTests),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

