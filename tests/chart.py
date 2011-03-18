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

import pycha.chart


class FunctionsTests(unittest.TestCase):

    def test_uniqueIndices(self):
        arr = (range(10), range(5), range(20), range(30))
        self.assertEqual(pycha.chart.uniqueIndices(arr), range(30))

        arr = (range(30), range(20), range(5), range(10))
        self.assertEqual(pycha.chart.uniqueIndices(arr), range(30))

        arr = (range(4), )
        self.assertEqual(pycha.chart.uniqueIndices(arr), range(4))

        arr = (range(0), )
        self.assertEqual(pycha.chart.uniqueIndices(arr), [])


class AreaTests(unittest.TestCase):

    def test_area(self):
        area = pycha.chart.Area(10, 20, 100, 300)
        self.assertEqual(area.x, 10)
        self.assertEqual(area.y, 20)
        self.assertEqual(area.w, 100)
        self.assertEqual(area.h, 300)
        msg = "<pycha.chart.Area@(10.00, 20.00) 100.00 x 300.00>"
        self.assertEqual(str(area), msg)


class OptionTests(unittest.TestCase):

    def test_options(self):
        opt = pycha.chart.Option(a=1, b=2, c=3)
        self.assertEqual(opt.a, opt['a'])
        self.assertEqual(opt.b, 2)
        self.assertEqual(opt['c'], 3)

        opt = pycha.chart.Option({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(opt.a, opt['a'])
        self.assertEqual(opt.b, 2)
        self.assertEqual(opt['c'], 3)

    def test_merge(self):
        opt = pycha.chart.Option(a=1, b=2,
                                 c=pycha.chart.Option(d=4, e=5))
        self.assertEqual(opt.c.d, 4)
        opt.merge(dict(c=pycha.chart.Option(d=7, e=8, f=9)))
        self.assertEqual(opt.c.d, 7)
        # new attributes not present in original option are not merged
        self.assertRaises(AttributeError, getattr, opt.c, 'f')

        opt.merge(pycha.chart.Option(a=10, b=20))
        self.assertEqual(opt.a, 10)
        self.assertEqual(opt.b, 20)


class ChartTests(unittest.TestCase):

    def test_init(self):
        ch = pycha.chart.Chart(None)
        self.assertEqual(ch.resetFlag, False)
        self.assertEqual(ch.datasets, [])
        self.assertNotEqual(ch.layout, None)
        self.assertEqual(ch.minxval, None)
        self.assertEqual(ch.maxxval, None)
        self.assertEqual(ch.minyval, None)
        self.assertEqual(ch.maxyval, None)
        self.assertEqual(ch.xscale, 1.0)
        self.assertEqual(ch.yscale, 1.0)
        self.assertEqual(ch.xrange, None)
        self.assertEqual(ch.yrange, None)
        self.assertEqual(ch.xticks, [])
        self.assertEqual(ch.yticks, [])
        self.assertEqual(ch.options, pycha.chart.DEFAULT_OPTIONS)
        self.assertEqual(ch.origin, 0.0)

    def test_datasets(self):
        ch = pycha.chart.Chart(None)
        d1 = ('dataset1', ([0, 0], [1, 2], [2, 1.5]))
        d2 = ('dataset2', ([0, 1], [1, 2], [2, 2.4]))
        d3 = ('dataset3', ([0, 4], [1, 3], [2, 0.5]))
        ch.addDataset((d1, d2, d3))
        self.assertEqual(ch._getDatasetsKeys(),
                         ['dataset1', 'dataset2', 'dataset3'])
        self.assertEqual(ch._getDatasetsValues(),
                         [d1[1], d2[1], d3[1]])

    def test_options(self):
        ch = pycha.chart.Chart(None)
        opt = pycha.chart.Option(shouldFill=False)
        ch.setOptions(opt)
        self.assertEqual(ch.options.shouldFill, False)

        opt = {'pieRadius': 0.8}
        ch.setOptions(opt)
        self.assertEqual(ch.options.pieRadius, 0.8)

    def test_reset(self):
        ch = pycha.chart.Chart(None, options={'shouldFill': False})
        self.assertEqual(ch.resetFlag, False)
        self.assertEqual(ch.options.shouldFill, False)
        dataset = (('dataset1', ([0, 1], [1, 1])), )
        ch.addDataset(dataset)
        self.assertEqual(ch._getDatasetsKeys(), ['dataset1'])
        ch.reset()
        defaultFill = pycha.chart.DEFAULT_OPTIONS.shouldFill
        self.assertEqual(ch.options.shouldFill, defaultFill)
        self.assertEqual(ch.datasets, [])
        self.assertEqual(ch.resetFlag, True)

    def test_colorscheme(self):
        options = {'colorScheme': {'name': 'gradient',
                                   'args': {'initialColor': '#000000'}}}
        ch = pycha.chart.Chart(None, options)
        dataset = (('dataset1', ([0, 1], [1, 1])), )
        ch.addDataset(dataset)
        ch._setColorscheme()
        self.assert_(isinstance(ch.colorScheme, dict))
        self.assertEqual(ch.colorScheme, {'dataset1': (0.0, 0.0, 0.0)})

        options = {'colorScheme': {'name': 'foo'}}
        ch = pycha.chart.Chart(None, options)
        ch.addDataset(dataset)
        self.assertRaises(ValueError, ch._setColorscheme)

    def test_updateXY(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        opt = {'padding': dict(left=10, right=10, top=10, bottom=10)}
        dataset = (
            ('dataset1', ([0, 1], [1, 1], [2, 3])),
            ('dataset2', ([0, 2], [1, 0], [3, 4])),
            )
        ch = pycha.chart.Chart(surface, opt)
        ch.addDataset(dataset)
        ch._updateXY()
        self.assertEqual(ch.minxval, 0.0)
        self.assertEqual(ch.maxxval, 3)
        self.assertEqual(ch.xrange, 3)
        self.assertEqual(ch.xscale, 1/3.0)

        self.assertEqual(ch.minyval, 0)
        self.assertEqual(ch.maxyval, 4)
        self.assertEqual(ch.yrange, 4)
        self.assertEqual(ch.yscale, 1/4.0)
        # TODO: test with different options (axis.range, ...)

    def test_updateTicks(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        opt = {'padding': dict(left=10, right=10, top=10, bottom=10)}
        dataset = (
            ('dataset1', ([0, 1], [1, 1], [2, 3])),
            ('dataset2', ([0, 2], [1, 0], [3, 4])),
            )
        ch = pycha.chart.Chart(surface, opt)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateTicks()
        xticks = [(0.0, 0), (1/3.0, 1), (2/3.0, 2)]
        for i in range(len(xticks)):
            self.assertAlmostEqual(ch.xticks[i][0], xticks[i][0], 4)
            self.assertAlmostEqual(ch.xticks[i][1], xticks[i][1], 4)

        yticks = [(1 - 0.1 * i, 0.4*i)
                  for i in range(ch.options.axis.y.tickCount + 1)]
        self.assertEqual(len(ch.yticks), len(yticks))
        for i in range(len(yticks)):
            self.assertAlmostEqual(ch.yticks[i][0], yticks[i][0], 4)
            self.assertAlmostEqual(ch.yticks[i][1], yticks[i][1], 4)

    def test_updateExplicitTicks(self):
        """Test for bug #7"""
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        yticks = [dict(v=i, label=str(i)) for i in range(0, 3)]
        opt = {'axis': {'y': {'ticks': yticks}}}
        dataset = (
            ('dataset1', ([0, 1], [1, 1], [2, 3])),
            )
        ch = pycha.chart.Chart(surface, opt)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateTicks()
        self.assertAlmostEqual(ch.yticks[0][0], 1.0, 4)
        self.assertAlmostEqual(ch.yticks[1][0], 2/3.0, 4)
        self.assertAlmostEqual(ch.yticks[2][0], 1/3.0, 4)

    def test_updateTicksPrecission(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        opt = {'axis': {'y': {'tickCount': 10, 'tickPrecission': 1}}}
        dataset = (
            ('dataset1', ([0, 1], [1, 1], [2, 3])),
            ('dataset2', ([0, 2], [1, 0], [3, 4])),
            )
        ch = pycha.chart.Chart(surface, opt)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateTicks()
        xticks = [(0.0, 0), (1/3.0, 1), (2/3.0, 2)]
        for i in range(len(xticks)):
            self.assertAlmostEqual(ch.xticks[i][0], xticks[i][0], 4)
            self.assertAlmostEqual(ch.xticks[i][1], xticks[i][1], 4)

        yticks = ((1, 0), (0.9, 0.4), (0.8, 0.8), (0.7, 1.2), (0.6, 1.6),
                  (0.5, 2.0), (0.4, 2.4), (0.3, 2.8), (0.2, 3.2), (0.1, 3.6),
                  (0.0, 4.0))
        self.assertEqual(len(ch.yticks), len(yticks))
        for i in range(len(yticks)):
            self.assertAlmostEqual(ch.yticks[i][0], yticks[i][0], 1)
            self.assertAlmostEqual(ch.yticks[i][1], yticks[i][1], 1)

        # decrease precission to 0
        opt = {'axis': {'y': {'tickCount': 10, 'tickPrecision': 0}}}
        dataset = (
            ('dataset1', ([0, 1], [1, 1], [2, 3])),
            ('dataset2', ([0, 2], [1, 0], [3, 4])),
            )
        ch = pycha.chart.Chart(surface, opt)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateTicks()

        yticks = ((1, 0), (0.75, 1), (0.5, 2), (0.25, 3), (0.0, 4))
        self.assertEqual(len(ch.yticks), len(yticks))
        for i in range(len(yticks)):
            self.assertAlmostEqual(ch.yticks[i][0], yticks[i][0], 1, i)
            self.assertEqual(ch.yticks[i][1], yticks[i][1], i)

    def test_abstractChart(self):
        ch = pycha.chart.Chart(None)
        self.assertRaises(NotImplementedError, ch._updateChart)
        self.assertRaises(NotImplementedError, ch._renderChart, None)

    def test_range(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        opt = {'axis': {'x': {'range': (1, 10)}, 'y': {'range': (1.0, 10.0)}}}
        ch = pycha.chart.Chart(surface, opt)
        dataset = (
            ('dataset1', ([0, 1], [1, 1], [2, 3])),
            )
        ch.addDataset(dataset)
        ch._updateXY()
        self.assertAlmostEqual(ch.xrange, 9, 4)
        self.assertAlmostEqual(ch.yrange, 9, 4)
        self.assertAlmostEqual(ch.xscale, 0.1111, 4)
        self.assertAlmostEqual(ch.yscale, 0.1111, 4)

    def test_interval(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        opt = {'axis': {'y': {'interval': 2.5}}}
        ch = pycha.chart.Chart(surface, opt)
        dataset = (
            ('dataset1', ([0, 1], [1, 4], [2, 10])),
            )
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateTicks()
        yticks = ((0.75, 2.5), (0.5, 5.0),
                  (0.25, 7.5), (0.0, 10.0))

        self.assertEqual(len(yticks), len(ch.yticks))
        for i, (pos, label) in enumerate(yticks):
            tick = ch.yticks[i]
            self.assertAlmostEqual(tick[0], pos, 2)
            self.assertAlmostEqual(tick[1], label, 2)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(FunctionsTests),
        unittest.makeSuite(AreaTests),
        unittest.makeSuite(OptionTests),
        unittest.makeSuite(ChartTests),
    ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
