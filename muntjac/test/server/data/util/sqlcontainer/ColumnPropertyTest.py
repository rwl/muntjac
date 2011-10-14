# -*- coding: utf-8 -*-
# from com.vaadin.data.Property.ReadOnlyException import (ReadOnlyException,)
# from com.vaadin.data.util.sqlcontainer.ColumnProperty.NotNullableException import (NotNullableException,)
# from java.util.Arrays import (Arrays,)
# from org.easymock.EasyMock import (EasyMock,)
# from org.junit.Assert import (Assert,)
# from org.junit.Test import (Test,)


class ColumnPropertyTest(object):

    def constructor_legalParameters_shouldSucceed(self):
        cp = self.ColumnProperty('NAME', False, True, True, 'Ville', str)
        Assert.assertNotNull(cp)

    def constructor_missingPropertyId_shouldFail(self):
        self.ColumnProperty(None, False, True, True, 'Ville', str)

    def constructor_missingType_shouldFail(self):
        self.ColumnProperty('NAME', False, True, True, 'Ville', None)

    def getValue_defaultValue_returnsVille(self):
        cp = self.ColumnProperty('NAME', False, True, True, 'Ville', str)
        Assert.assertEquals('Ville', cp.getValue())

    def setValue_readWriteNullable_returnsKalle(self):
        cp = self.ColumnProperty('NAME', False, True, True, 'Ville', str)
        container = EasyMock.createMock(self.SQLContainer)
        owner = self.RowItem(container, self.RowId([1]), Arrays.asList(cp))
        container.itemChangeNotification(owner)
        EasyMock.replay(container)
        cp.setValue('Kalle')
        Assert.assertEquals('Kalle', cp.getValue())
        EasyMock.verify(container)

    def setValue_readOnlyNullable_shouldFail(self):
        cp = self.ColumnProperty('NAME', True, True, True, 'Ville', str)
        container = EasyMock.createMock(self.SQLContainer)
        self.RowItem(container, self.RowId([1]), Arrays.asList(cp))
        EasyMock.replay(container)
        cp.setValue('Kalle')
        EasyMock.verify(container)

    def setValue_readWriteNullable_nullShouldWork(self):
        cp = self.ColumnProperty('NAME', False, True, True, 'Ville', str)
        container = EasyMock.createMock(self.SQLContainer)
        owner = self.RowItem(container, self.RowId([1]), Arrays.asList(cp))
        container.itemChangeNotification(owner)
        EasyMock.replay(container)
        cp.setValue(None)
        Assert.assertNull(cp.getValue())
        EasyMock.verify(container)

    def setValue_readWriteNotNullable_nullShouldFail(self):
        cp = self.ColumnProperty('NAME', False, True, False, 'Ville', str)
        container = EasyMock.createMock(self.SQLContainer)
        owner = self.RowItem(container, self.RowId([1]), Arrays.asList(cp))
        container.itemChangeNotification(owner)
        EasyMock.replay(container)
        cp.setValue(None)
        Assert.assertNotNull(cp.getValue())
        EasyMock.verify(container)

    def getType_normal_returnsStringClass(self):
        cp = self.ColumnProperty('NAME', False, True, True, 'Ville', str)
        Assert.assertSame(str, cp.getType())

    def isReadOnly_readWriteNullable_returnsTrue(self):
        cp = self.ColumnProperty('NAME', False, True, True, 'Ville', str)
        Assert.assertFalse(cp.isReadOnly())

    def isReadOnly_readOnlyNullable_returnsTrue(self):
        cp = self.ColumnProperty('NAME', True, True, True, 'Ville', str)
        Assert.assertTrue(cp.isReadOnly())

    def setReadOnly_readOnlyChangeAllowed_shouldSucceed(self):
        cp = self.ColumnProperty('NAME', False, True, True, 'Ville', str)
        cp.setReadOnly(True)
        Assert.assertTrue(cp.isReadOnly())

    def setReadOnly_readOnlyChangeDisallowed_shouldFail(self):
        cp = self.ColumnProperty('NAME', False, False, True, 'Ville', str)
        cp.setReadOnly(True)
        Assert.assertFalse(cp.isReadOnly())

    def getPropertyId_normal_returnsNAME(self):
        cp = self.ColumnProperty('NAME', False, False, True, 'Ville', str)
        Assert.assertEquals('NAME', cp.getPropertyId())

    def isModified_valueModified_returnsTrue(self):
        cp = self.ColumnProperty('NAME', False, True, True, 'Ville', str)
        container = EasyMock.createMock(self.SQLContainer)
        owner = self.RowItem(container, self.RowId([1]), Arrays.asList(cp))
        container.itemChangeNotification(owner)
        EasyMock.replay(container)
        cp.setValue('Kalle')
        Assert.assertEquals('Kalle', cp.getValue())
        Assert.assertTrue(cp.isModified())
        EasyMock.verify(container)

    def isModified_valueNotModified_returnsFalse(self):
        cp = self.ColumnProperty('NAME', False, False, True, 'Ville', str)
        Assert.assertFalse(cp.isModified())

    def setValue_nullOnNullable_shouldWork(self):
        cp = self.ColumnProperty('NAME', False, True, True, 'asdf', str)
        container = EasyMock.createMock(self.SQLContainer)
        self.RowItem(container, self.RowId([1]), Arrays.asList(cp))
        cp.setValue(None)
        Assert.assertNull(cp.getValue())

    def setValue_resetTonullOnNullable_shouldWork(self):
        cp = self.ColumnProperty('NAME', False, True, True, None, str)
        container = EasyMock.createMock(self.SQLContainer)
        self.RowItem(container, self.RowId([1]), Arrays.asList(cp))
        cp.setValue('asdf')
        Assert.assertEquals('asdf', cp.getValue())
        cp.setValue(None)
        Assert.assertNull(cp.getValue())
