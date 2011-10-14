# -*- coding: utf-8 -*-
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
