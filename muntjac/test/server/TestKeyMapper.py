# -*- coding: utf-8 -*-
# from com.vaadin.terminal.KeyMapper import (KeyMapper,)
# from java.lang.reflect.Field import (Field,)
# from java.util.Hashtable import (Hashtable,)
# from junit.framework.TestCase import (TestCase,)


class TestKeyMapper(TestCase):

    def testAdd(self):
        mapper = KeyMapper()
        o1 = self.Object()
        o2 = self.Object()
        o3 = self.Object()
        # Create new ids
        key1 = mapper.key(o1)
        key2 = mapper.key(o2)
        key3 = mapper.key(o3)
        self.assertEquals(mapper.get(key1), o1)
        self.assertEquals(mapper.get(key2), o2)
        self.assertEquals(mapper.get(key3), o3)
        self.assertNotSame(key1, key2)
        self.assertNotSame(key1, key3)
        self.assertNotSame(key2, key3)
        self.assertSize(mapper, 3)
        # Key should not add if there already is a mapping
        self.assertEquals(mapper.key(o3), key3)
        self.assertSize(mapper, 3)
        # Remove -> add should return a new key
        mapper.remove(o1)
        newkey1 = mapper.key(o1)
        self.assertNotSame(key1, newkey1)

    def testRemoveAll(self):
        mapper = KeyMapper()
        o1 = self.Object()
        o2 = self.Object()
        o3 = self.Object()
        # Create new ids
        mapper.key(o1)
        mapper.key(o2)
        mapper.key(o3)
        self.assertSize(mapper, 3)
        mapper.removeAll()
        self.assertSize(mapper, 0)

    def testRemove(self):
        mapper = KeyMapper()
        o1 = self.Object()
        o2 = self.Object()
        o3 = self.Object()
        # Create new ids
        mapper.key(o1)
        mapper.key(o2)
        mapper.key(o3)
        self.assertSize(mapper, 3)
        mapper.remove(o1)
        self.assertSize(mapper, 2)
        mapper.key(o1)
        self.assertSize(mapper, 3)
        mapper.remove(o1)
        self.assertSize(mapper, 2)
        mapper.remove(o2)
        mapper.remove(o3)
        self.assertSize(mapper, 0)

    def assertSize(self, mapper, i):
        try:
            f1 = KeyMapper.getDeclaredField('objectKeyMap')
            f2 = KeyMapper.getDeclaredField('keyObjectMap')
            f1.setAccessible(True)
            f2.setAccessible(True)
            h1 = getattr(mapper, f1)
            h2 = getattr(mapper, f2)
            self.assertEquals(i, len(h1))
            self.assertEquals(i, len(h2))
        except BaseException, t:
            t.printStackTrace()
            self.fail()
