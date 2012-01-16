# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

import sys
import traceback

from unittest import TestCase
from muntjac.terminal.key_mapper import KeyMapper


class TestKeyMapper(TestCase):

    def testAdd(self):
        mapper = KeyMapper()
        o1 = object()
        o2 = object()
        o3 = object()

        # Create new ids
        key1 = mapper.key(o1)
        key2 = mapper.key(o2)
        key3 = mapper.key(o3)

        self.assertEquals(mapper.get(key1), o1)
        self.assertEquals(mapper.get(key2), o2)
        self.assertEquals(mapper.get(key3), o3)
        self.assertNotEquals(key1, key2)
        self.assertNotEquals(key1, key3)
        self.assertNotEquals(key2, key3)

        self.assertSize(mapper, 3)

        # Key should not add if there already is a mapping
        self.assertEquals(mapper.key(o3), key3)
        self.assertSize(mapper, 3)

        # Remove -> add should return a new key
        mapper.remove(o1)
        newkey1 = mapper.key(o1)
        self.assertNotEqual(key1, newkey1)


    def testRemoveAll(self):
        mapper = KeyMapper()
        o1 = object()
        o2 = object()
        o3 = object()

        # Create new ids
        mapper.key(o1)
        mapper.key(o2)
        mapper.key(o3)

        self.assertSize(mapper, 3)
        mapper.removeAll()
        self.assertSize(mapper, 0)


    def testRemove(self):
        mapper = KeyMapper()
        o1 = object()
        o2 = object()
        o3 = object()

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
            h1 = getattr(mapper, '_objectKeyMap')
            h2 = getattr(mapper, '_keyObjectMap')
            self.assertEquals(i, len(h1))
            self.assertEquals(i, len(h2))
        except Exception:
            traceback.print_exc(file=sys.stdout)
            self.fail()
