# -*- coding: utf-8 -*-
# from com.vaadin.data.util.sqlcontainer.RowId import (RowId,)
# from org.junit.Assert import (Assert,)
# from org.junit.Test import (Test,)


class RowIdTest(object):

    def constructor_withArrayOfPrimaryKeyColumns_shouldSucceed(self):
        id = RowId(['id', 'name'])
        Assert.assertArrayEquals(['id', 'name'], id.getId())

    def constructor_withNullParameter_shouldFail(self):
        RowId(None)

    def hashCode_samePrimaryKeys_sameResult(self):
        id = RowId(['id', 'name'])
        id2 = RowId(['id', 'name'])
        Assert.assertEquals(id.hashCode(), id2.hashCode())

    def hashCode_differentPrimaryKeys_differentResult(self):
        id = RowId(['id', 'name'])
        id2 = RowId(['id'])
        Assert.assertFalse(id.hashCode() == id2.hashCode())

    def equals_samePrimaryKeys_returnsTrue(self):
        id = RowId(['id', 'name'])
        id2 = RowId(['id', 'name'])
        Assert.assertEquals(id, id2)

    def equals_differentPrimaryKeys_returnsFalse(self):
        id = RowId(['id', 'name'])
        id2 = RowId(['id'])
        Assert.assertFalse(id == id2.hashCode())

    def equals_differentDataType_returnsFalse(self):
        id = RowId(['id', 'name'])
        Assert.assertFalse(id == 'Tudiluu')
        Assert.assertFalse(id == int(1337))
