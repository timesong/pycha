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
import math
import unittest

import cairo

import pycha.pie

class SliceTests(unittest.TestCase):

    def test_init(self):
        slice = pycha.pie.Slice('test', 3/5.0, 0, 4, 1/4.0)
        self.assertEqual(slice.name, 'test')
        self.assertEqual(slice.fraction, 3/5.0)
        self.assertEqual(slice.xval, 0)
        self.assertEqual(slice.yval, 4)
        self.assertEqual(slice.startAngle, math.pi / 2)
        self.assertEqual(slice.endAngle, 1.7 * math.pi)

    def test_isBigEnough(self):
        slice = pycha.pie.Slice('test 1', 3/5.0, 0, 4, 1/4.0)
        self.assertEqual(slice.isBigEnough(), True)

        slice = pycha.pie.Slice('test 2', 1/10000.0, 0, 4, 1/4.0)
        self.assertEqual(slice.isBigEnough(), False)

    def test_normalisedAngle(self):
        # First quadrant
        slice = pycha.pie.Slice('test 1', 1/6.0, 0, 4, 0)
        self.assertAlmostEqual(slice.getNormalisedAngle(), 1/6.0 * math.pi, 4)

        # Second quadrant
        slice = pycha.pie.Slice('test 1', 1/6.0, 0, 4, 1/4.0)
        self.assertAlmostEqual(slice.getNormalisedAngle(), 2/3.0 * math.pi, 4)

        # Third quadrant
        slice = pycha.pie.Slice('test 1', 1/6.0, 0, 4, 1/2.0)
        self.assertAlmostEqual(slice.getNormalisedAngle(), 7/6.0 * math.pi, 4)

        # Fouth quadrant
        slice = pycha.pie.Slice('test 1', 1/6.0, 0, 4, 3/4.0)
        self.assertAlmostEqual(slice.getNormalisedAngle(), 10/6.0 * math.pi, 4)

        # Bigger than a circle
        slice = pycha.pie.Slice('test 1', 2/3.0, 0, 4, 3/4.0)
        self.assertAlmostEqual(slice.getNormalisedAngle(), 1/6.0 * math.pi, 4)

        # Negative angle
        slice = pycha.pie.Slice('test 1', -1/6.0, 0, 4, 0)
        self.assertAlmostEqual(slice.getNormalisedAngle(), 11/6.0 * math.pi, 4)

class PieTests(unittest.TestCase):

    def test_init(self):
        ch = pycha.pie.PieChart(None)
        self.assertEqual(ch.slices, [])
        self.assertEqual(ch.centerx, 0)
        self.assertEqual(ch.centery, 0)

    def test_updateChart(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, 10],)),
            ('dataset2', ([0, 20],)),
            ('dataset3', ([0, 70],)),
            )
        opt = {'padding': {'left': 0, 'right': 0, 'top': 0, 'bottom': 0},
               'pieRadius': 0.5}
        ch = pycha.pie.PieChart(surface, opt)
        ch.addDataset(dataset)
        ch.render()
        self.assertEqual(ch.centerx, 250)
        self.assertEqual(ch.centery, 250)

        slices = (
            pycha.pie.Slice('dataset1', 0.1, 0, 10, 0),
            pycha.pie.Slice('dataset2', 0.2, 1, 20, 0.1),
            pycha.pie.Slice('dataset3', 0.7, 2, 70, 0.3),
            )

        for i, slice in enumerate(slices):
            s1, s2 = ch.slices[i], slice
            self.assertEqual(s1.name, s2.name)
            self.assertAlmostEqual(s1.fraction, s2.fraction, 4)
            self.assertAlmostEqual(s1.startAngle, s2.startAngle, 4)
            self.assertAlmostEqual(s1.endAngle, s2.endAngle, 4)
            self.assertEqual(s1.xval, s2.xval)
            self.assertEqual(s1.yval, s2.yval)

    def test_updateTicks(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, 10],)),
            ('dataset2', ([0, 20],)),
            ('dataset3', ([0, 70],)),
            )
        opt = {'padding': {'left': 0, 'right': 0, 'top': 0, 'bottom': 0},
               'pieRadius': 0.5}
        ch = pycha.pie.PieChart(surface, opt)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        ch._updateTicks()
        self.assertEqual(ch.xticks, [(0, 'dataset1 (10.0%)'),
                                     (1, 'dataset2 (20.0%)'),
                                     (2, 'dataset3 (70.0%)')])

        ticks = [{'v': 0, 'label': 'First dataset'},
                 {'v': 1, 'label': 'Second dataset'},
                 {'v': 2, 'label': 'Third dataset'}]
        opt = {'axis': {'x': {'ticks': ticks},},}
        ch = pycha.pie.PieChart(surface, opt)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        ch._updateTicks()
        self.assertEqual(ch.xticks, [(0, 'First dataset (10.0%)'),
                                     (1, 'Second dataset (20.0%)'),
                                     (2, 'Third dataset (70.0%)')])

    def test_issue5(self):
        """See http://bitbucket.org/lgs/pycha/issue/5/"""
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, 30],)),
            ('dataset2', ([0, 0],)), # Empty set!!
            ('dataset3', ([0, 70],)),
            )
        ch = pycha.pie.PieChart(surface, {})
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()

        # there is no slice for the empty set
        slices = (
            pycha.pie.Slice('dataset1', 0.3, 0, 30, 0),
            pycha.pie.Slice('dataset3', 0.7, 2, 70, 0.3),
            )

        for i, slice in enumerate(slices):
            s1, s2 = ch.slices[i], slice
            self.assertEqual(s1.name, s2.name)
            self.assertAlmostEqual(s1.fraction, s2.fraction, 4)
            self.assertAlmostEqual(s1.startAngle, s2.startAngle, 4)
            self.assertAlmostEqual(s1.endAngle, s2.endAngle, 4)
            self.assertEqual(s1.xval, s2.xval)
            self.assertEqual(s1.yval, s2.yval)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(SliceTests),
        unittest.makeSuite(PieTests),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

