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

from __pyjamas__ import (ARGERROR, POSTINC,)


class ListSet(list):
    """ListSet is an internal Vaadin class which implements a combination of a List
    and a Set. The main purpose of this class is to provide a list with a fast
    {@link #contains(Object)} method. Each inserted object must by unique (as
    specified by {@link #equals(Object)}). The {@link #set(int, Object)} method
    allows duplicates because of the way {@link Collections#sort(java.util.List)}
    works.

    This class is subject to change and should not be used outside Vaadin core.
    """
    _itemSet = None
    # Contains a map from an element to the number of duplicates it has. Used
    # to temporarily allow duplicates in the list.

    _duplicates = dict()

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(ListSet, self)()
            self._itemSet = set()
        elif _1 == 1:
            if isinstance(_0[0], Collection):
                c, = _0
                super(ListSet, self)(c)
                self._itemSet = set(len(c))
                self._itemSet.addAll(c)
            else:
                initialCapacity, = _0
                super(ListSet, self)(initialCapacity)
                self._itemSet = set(initialCapacity)
        else:
            raise ARGERROR(0, 1)

    # Delegate contains operations to the set

    def contains(self, o):
        return o in self._itemSet

    def containsAll(self, c):
        # Methods for updating the set when the list is updated.
        return self._itemSet.containsAll(c)

    def add(self, *args):
        """None
        ---
        Works as java.util.ArrayList#add(int, java.lang.Object) but returns
        immediately if the element is already in the ListSet.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            e, = _0
            if self.contains(e):
                # Duplicates are not allowed
                return False
            if super(ListSet, self).add(e):
                self._itemSet.add(e)
                return True
            else:
                return False
        elif _1 == 2:
            index, element = _0
            if self.contains(element):
                # Duplicates are not allowed
                return
            super(ListSet, self).add(index, element)
            self._itemSet.add(element)
        else:
            raise ARGERROR(1, 2)

    def addAll(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            c, = _0
            modified = False
            i = c
            while i.hasNext():
                e = i.next()
                if self.contains(e):
                    continue
                if self.add(e):
                    self._itemSet.add(e)
                    modified = True
            return modified
        elif _1 == 2:
            index, c = _0
            self.ensureCapacity(len(self) + len(c))
            modified = False
            i = c
            while i.hasNext():
                e = i.next()
                if self.contains(e):
                    continue
                self.add(POSTINC(globals(), locals(), 'index'), e)
                self._itemSet.add(e)
                modified = True
            return modified
        else:
            raise ARGERROR(1, 2)

    def clear(self):
        super(ListSet, self).clear()
        self._itemSet.clear()

    def indexOf(self, o):
        if not self.contains(o):
            return -1
        return super(ListSet, self).index(o)

    def lastIndexOf(self, o):
        if not self.contains(o):
            return -1
        return super(ListSet, self).rindex(o)

    def remove(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Object):
                o, = _0
                if super(ListSet, self).remove(o):
                    self._itemSet.remove(o)
                    return True
                else:
                    return False
            else:
                index, = _0
                e = super(ListSet, self).remove(index)
                if e is not None:
                    self._itemSet.remove(e)
                return e
        else:
            raise ARGERROR(1, 1)

    def removeRange(self, fromIndex, toIndex):
        toRemove = set()
        _0 = True
        idx = fromIndex
        while True:
            if _0 is True:
                _0 = False
            else:
                idx += 1
            if not (idx < toIndex):
                break
            toRemove.add(self.get(idx))
        super(ListSet, self).removeRange(fromIndex, toIndex)
        self._itemSet.removeAll(toRemove)

    def set(self, index, element):
        if self.contains(element):
            # Element already exist in the list
            if self.get(index) == element:
                # At the same position, nothing to be done
                return element
            else:
                # Adding at another position. We assume this is a sort
                # operation and temporarily allow it.
                # We could just remove (null) the old element and keep the list
                # unique. This would require finding the index of the old
                # element (indexOf(element)) which is not a fast operation in a
                # list. So we instead allow duplicates temporarily.
                self.addDuplicate(element)
        old = super(ListSet, self).set(index, element)
        self.removeFromSet(old)
        self._itemSet.add(element)
        return old

    def removeFromSet(self, e):
        """Removes "e" from the set if it no longer exists in the list.

        @param e
        """
        dupl = self._duplicates[e]
        if dupl is not None:
            # A duplicate was present so we only decrement the duplicate count
            # and continue
            if dupl == 1:
                # This is what always should happen. A sort sets the items one
                # by one, temporarily breaking the uniqueness requirement.
                self._duplicates.remove(e)
            else:
                self._duplicates.put(e, dupl - 1)
        else:
            # The "old" value is no longer in the list.
            self._itemSet.remove(e)

    def addDuplicate(self, element):
        """Marks the "element" can be found more than once from the list. Allowed in
        {@link #set(int, Object)} to make sorting work.

        @param element
        """
        nr = self._duplicates[element]
        if nr is None:
            nr = 1
        else:
            nr += 1
        # Store the number of duplicates of this element so we know later on if
        # we should remove an element from the set or if it was a duplicate (in
        # removeFromSet)

        self._duplicates.put(element, nr)

    def clone(self):
        v = super(ListSet, self).clone()
        v.itemSet = set(self._itemSet)
        return v
