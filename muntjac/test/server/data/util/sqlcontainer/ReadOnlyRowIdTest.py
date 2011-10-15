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

# from com.vaadin.data.util.sqlcontainer.ReadOnlyRowId import (ReadOnlyRowId,)
# from junit.framework.Assert import (Assert,)
# from org.junit.Test import (Test,)


class ReadOnlyRowIdTest(object):

    def getRowNum_shouldReturnRowNumGivenInConstructor(self):
        rowNum = 1337
        rid = ReadOnlyRowId(rowNum)
        Assert.assertEquals(rowNum, rid.getRowNum())

    def hashCode_shouldBeEqualToHashCodeOfRowNum(self):
        rowNum = 1337
        rid = ReadOnlyRowId(rowNum)
        Assert.assertEquals(Integer.valueOf.valueOf(rowNum).hashCode(), rid.hashCode())

    def equals_compareWithNull_shouldBeFalse(self):
        rid = ReadOnlyRowId(1337)
        Assert.assertFalse(rid is None)

    def equals_compareWithSameInstance_shouldBeTrue(self):
        rid = ReadOnlyRowId(1337)
        rid2 = rid
        Assert.assertTrue(rid == rid2)

    def equals_compareWithOtherType_shouldBeFalse(self):
        rid = ReadOnlyRowId(1337)
        Assert.assertFalse(rid == self.Object())

    def equals_compareWithOtherRowId_shouldBeFalse(self):
        rid = ReadOnlyRowId(1337)
        rid2 = ReadOnlyRowId(42)
        Assert.assertFalse(rid == rid2)
