# Copyright (C) 2010 IT Mill Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# from com.vaadin.data.util.sqlcontainer.SQLUtil import (SQLUtil,)
# from junit.framework.Assert import (Assert,)
# from org.junit.Test import (Test,)


class UtilTest(object):

    def escapeSQL_noQuotes_returnsSameString(self):
        Assert.assertEquals('asdf', SQLUtil.escapeSQL('asdf'))

    def escapeSQL_singleQuotes_returnsEscapedString(self):
        Assert.assertEquals('O\'\'Brien', SQLUtil.escapeSQL('O\'Brien'))

    def escapeSQL_severalQuotes_returnsEscapedString(self):
        Assert.assertEquals('asdf\'\'ghjk\'\'qwerty', SQLUtil.escapeSQL('asdf\'ghjk\'qwerty'))

    def escapeSQL_doubleQuotes_returnsEscapedString(self):
        Assert.assertEquals('asdf\\\"foo', SQLUtil.escapeSQL('asdf\"foo'))

    def escapeSQL_multipleDoubleQuotes_returnsEscapedString(self):
        Assert.assertEquals('asdf\\\"foo\\\"bar', SQLUtil.escapeSQL('asdf\"foo\"bar'))

    def escapeSQL_backslashes_returnsEscapedString(self):
        Assert.assertEquals('foo\\\\nbar\\\\r', SQLUtil.escapeSQL('foo\\nbar\\r'))

    def escapeSQL_x00_removesX00(self):
        Assert.assertEquals('foobar', SQLUtil.escapeSQL('foo\\x00bar'))

    def escapeSQL_x1a_removesX1a(self):
        Assert.assertEquals('foobar', SQLUtil.escapeSQL('foo\\x1abar'))
