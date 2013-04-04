# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

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
