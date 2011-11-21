# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

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
