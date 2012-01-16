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

"""Simple two-way map."""


class KeyMapper(object):
    """C{KeyMapper} is the simple two-way map for generating textual keys
    for objects and retrieving the objects later with the key.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self):
        self._lastKey = 0
        self._objectKeyMap = dict()
        self._keyObjectMap = dict()


    def key(self, o):
        """Gets key for an object.

        @param o: the object.
        """
        if o is None:
            return 'null'

        # If the object is already mapped, use existing key
        key = self._objectKeyMap.get(o)
        if key is not None:
            return key

        # If the object is not yet mapped, map it
        self._lastKey += 1
        key = str(self._lastKey)
        self._objectKeyMap[o] = key
        self._keyObjectMap[key] = o
        return key


    def get(self, key):
        """Retrieves object with the key.

        @param key:
                   the name with the desired value.
        @return: the object with the key.
        """
        return self._keyObjectMap.get(key)


    def remove(self, removeobj):
        """Removes object from the mapper.

        @param removeobj:
                   the object to be removed.
        """
        key = self._objectKeyMap.get(removeobj)
        if key is not None:
            del self._objectKeyMap[removeobj]
            if key in self._keyObjectMap:
                del self._keyObjectMap[key]


    def removeAll(self):
        """Removes all objects from the mapper."""
        self._objectKeyMap.clear()
        self._keyObjectMap.clear()
