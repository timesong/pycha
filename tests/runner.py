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

import bar
import chart
import color
import line
import pie
import utils

def test_suite():
    return unittest.TestSuite((
        bar.test_suite(),
        chart.test_suite(),
        color.test_suite(),
        line.test_suite(),
        pie.test_suite(),
        utils.test_suite(),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
