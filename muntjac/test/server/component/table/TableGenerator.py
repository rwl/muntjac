# -*- coding: utf-8 -*-
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
