# Copyright (C) 2011 Vaadin Ltd
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

from __pyjamas__ import (PREINC,)
# from java.io.Serializable import (Serializable,)
# from java.util.Hashtable import (Hashtable,)


class KeyMapper(Serializable):
    """<code>KeyMapper</code> is the simple two-way map for generating textual keys
    for objects and retrieving the objects later with the key.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    _lastKey = 0
    _objectKeyMap = dict()
    _keyObjectMap = dict()

    def key(self, o):
        """Gets key for an object.

        @param o
                   the object.
        """
        if o is None:
            return 'null'
        # If the object is already mapped, use existing key
        key = self._objectKeyMap[o]
        if key is not None:
            return key
        # If the object is not yet mapped, map it
        key = String.valueOf.valueOf(PREINC(globals(), locals(), 'self._lastKey'))
        self._objectKeyMap.put(o, key)
        self._keyObjectMap.put(key, o)
        return key

    def get(self, key):
        """Retrieves object with the key.

        @param key
                   the name with the desired value.
        @return the object with the key.
        """
        return self._keyObjectMap[key]

    def remove(self, removeobj):
        """Removes object from the mapper.

        @param removeobj
                   the object to be removed.
        """
        key = self._objectKeyMap[removeobj]
        if key is not None:
            self._objectKeyMap.remove(removeobj)
            self._keyObjectMap.remove(key)

    def removeAll(self):
        """Removes all objects from the mapper."""
        self._objectKeyMap.clear()
        self._keyObjectMap.clear()
