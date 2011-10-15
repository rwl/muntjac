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

# from org.junit.Test import (Test,)


class TableGenerator(object):

    @classmethod
    def createTableWithDefaultContainer(cls, properties, items):
        t = Table()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < properties):
                break
            t.addContainerProperty('Property ' + i, str, None)
        _1 = True
        j = 0
        while True:
            if _1 is True:
                _1 = False
            else:
                j += 1
            if not (j < items):
                break
            item = t.addItem('Item ' + j)
            _2 = True
            i = 0
            while True:
                if _2 is True:
                    _2 = False
                else:
                    i += 1
                if not (i < properties):
                    break
                item.getItemProperty('Property ' + i).setValue('Item ' + j + '/Property ' + i)
        return t

    def testTableGenerator(self):
        t = self.createTableWithDefaultContainer(1, 1)
        self.junit.framework.Assert.assertEquals(len(t), 1)
        self.junit.framework.Assert.assertEquals(len(t.getContainerPropertyIds()), 1)
        t = self.createTableWithDefaultContainer(100, 50)
        self.junit.framework.Assert.assertEquals(len(t), 50)
        self.junit.framework.Assert.assertEquals(len(t.getContainerPropertyIds()), 100)
