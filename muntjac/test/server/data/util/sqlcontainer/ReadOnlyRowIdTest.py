# -*- coding: utf-8 -*-
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
