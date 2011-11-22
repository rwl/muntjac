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

"""Simple two-way map."""


class KeyMapper(object):
    """C{KeyMapper} is the simple two-way map for generating textual keys
    for objects and retrieving the objects later with the key.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.1
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
