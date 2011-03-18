# -*- encoding: utf-8 -*-
# Copyright(c) 2007-2010 by Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
#              2010 by Yaco S.L. <lgs@yaco.es>
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

import pycha.utils


class UtilsTests(unittest.TestCase):

    def test_clamp(self):
        self.assertEqual(pycha.utils.clamp(0, 1, 2), 1)
        self.assertEqual(pycha.utils.clamp(0, 1, -1), 0)
        self.assertEqual(pycha.utils.clamp(0, 1, 0.5), 0.5)
        self.assertEqual(pycha.utils.clamp(0, 1, 1), 1)
        self.assertEqual(pycha.utils.clamp(0, 1, 0), 0)

    def test_safe_unicode(self):
        self.assertEqual(pycha.utils.safe_unicode(u'unicode'), u'unicode')
        self.assertEqual(pycha.utils.safe_unicode('ascii'), u'ascii')
        self.assertEqual(pycha.utils.safe_unicode('non ascii ñ', 'utf-8'),
                         u'non ascii ñ')


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(UtilsTests),
    ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
