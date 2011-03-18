# Copyright(c) 2007-2010 by Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
#              2009 by Yaco S.L. <lgs@yaco.es>
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

import pycha.color


class SimpleColorScheme(pycha.color.ColorScheme):
    pass


class ColorTests(unittest.TestCase):

    def test_hex2rgb(self):
        color = pycha.color.hex2rgb('#ff0000')
        self.assert_(isinstance(color, tuple))
        self.assertAlmostEqual(1, color[0])
        self.assertAlmostEqual(0, color[1])
        self.assertAlmostEqual(0, color[2])

        color2 = pycha.color.hex2rgb(color)
        self.assertEqual(color, color2)

        color = pycha.color.hex2rgb('#000fff000', digits=3)
        self.assert_(isinstance(color, tuple))
        self.assertEqual(0, color[0])
        self.assertEqual(1, color[1])
        self.assertEqual(0, color[2])

        color = pycha.color.hex2rgb('#00000000ffff', digits=4)
        self.assert_(isinstance(color, tuple))
        self.assertEqual(0, color[0])
        self.assertEqual(0, color[1])
        self.assertEqual(1, color[2])

    def test_rgb2hsv_and_hsv2rgb(self):
        for rgb, hsv in (((1.0, 0.0, 0.0), (0.0, 1.0, 1.0)),
                         ((1.0, 0.5, 0.0), (30.0, 1.0, 1.0)),
                         ((1.0, 1.0, 0.0), (60.0, 1.0, 1.0)),
                         ((0.5, 1.0, 0.0), (90.0, 1.0, 1.0)),
                         ((0.0, 1.0, 0.0), (120.0, 1.0, 1.0)),
                         ((0.0, 1.0, 0.5), (150.0, 1.0, 1.0)),
                         ((0.0, 1.0, 1.0), (180.0, 1.0, 1.0)),
                         ((0.0, 0.5, 1.0), (210.0, 1.0, 1.0)),
                         ((0.0, 0.0, 1.0), (240.0, 1.0, 1.0)),
                         ((0.5, 0.0, 1.0), (270.0, 1.0, 1.0)),
                         ((1.0, 0.0, 1.0), (300.0, 1.0, 1.0)),
                         ((1.0, 0.0, 0.5), (330.0, 1.0, 1.0)),
                         ((0.375, 0.5, 0.25), (90.0, 0.5, 0.5)),
                         ((0.21875, 0.25, 0.1875), (90.0, 0.25, 0.25))):
            self._assertColors(pycha.color.rgb2hsv(*rgb), hsv, 5)
            self._assertColors(pycha.color.hsv2rgb(*hsv), rgb, 5)

    def test_lighten(self):
        r, g, b = (1.0, 1.0, 0.0)
        r2, g2, b2 = pycha.color.lighten(r, g, b, 0.1)
        self.assertEqual((r2, g2, b2), (1.0, 1.0, 0.1))

        r3, g3, b3 = pycha.color.lighten(r2, g2, b2, 0.5)
        self.assertEqual((r3, g3, b3), (1.0, 1.0, 0.6))

    def _assertColors(self, c1, c2, precission):
        for i in range(3):
            self.assertAlmostEqual(c1[i], c2[i], precission)

    def test_basicColors(self):
        colors = ('red', 'green', 'blue', 'grey', 'black', 'darkcyan')
        for color in colors:
            self.assert_(color in pycha.color.basicColors)

    def test_ColorSchemeRegistry(self):
        self.assertEquals(SimpleColorScheme,
                          pycha.color.ColorScheme.getColorScheme('simple'))
        self.assertEquals(None,
                          pycha.color.ColorScheme.getColorScheme('foo'))

    def test_FixedColorScheme(self):
        keys = range(3)
        colors = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
        scheme = pycha.color.FixedColorScheme(keys, colors)
        self._assertColors(scheme[0], (1.0, 0.0, 0.0), 1)
        self._assertColors(scheme[1], (0.0, 1.0, 0.0), 3)
        self._assertColors(scheme[2], (0.0, 0.0, 1.0), 3)

    def test_GradientColorScheme(self):
        keys = range(5)
        scheme = pycha.color.GradientColorScheme(keys, "#000000")
        self._assertColors(scheme[0], (0.0, 0.0, 0.0), 3)
        self._assertColors(scheme[1], (0.1, 0.1, 0.1), 3)
        self._assertColors(scheme[2], (0.2, 0.2, 0.2), 3)
        self._assertColors(scheme[3], (0.3, 0.3, 0.3), 3)
        self._assertColors(scheme[4], (0.4, 0.4, 0.4), 3)

    def test_autoLighting(self):
        """This test ensures that the colors don't get to white too fast.

        See bug #8.
        """
        # we have a lot of keys
        n = 50
        keys = range(n)
        color = '#ff0000'
        scheme = pycha.color.GradientColorScheme(keys, color)

        # ensure that the last color is not completely white
        color = scheme[n-1]

        # the red component was already 1
        self.assertAlmostEqual(color[0], 1.0, 4)
        self.assertNotAlmostEqual(color[1], 1.0, 4)
        self.assertNotAlmostEqual(color[2], 1.0, 4)

    def test_RainbowColorScheme(self):
        keys = range(5)
        scheme = pycha.color.GradientColorScheme(keys, "#ff0000")
        self._assertColors(scheme[0], (1.0, 0.0, 0.0), 3)
        self._assertColors(scheme[1], (1.0, 0.1, 0.1), 3)
        self._assertColors(scheme[2], (1.0, 0.2, 0.2), 3)
        self._assertColors(scheme[3], (1.0, 0.3, 0.3), 3)
        self._assertColors(scheme[4], (1.0, 0.4, 0.4), 3)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ColorTests),
    ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
