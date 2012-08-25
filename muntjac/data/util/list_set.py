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

"""ListSet is an internal Muntjac class which implements a combination of
a list and a set."""


class ListSet(list):
    """ListSet is an internal Muntjac class which implements a combination of
    a List and a Set. The main purpose of this class is to provide a list with
    a fast L{contains} method. Each inserted object must by unique (as
    specified by L{equals}). The L{set} method allows duplicates because of
    the way L{sort} works.

    This class is subject to change and should not be used outside Muntjac
    core.
    """

    def __init__(self, *args):
        self._itemSet = None

        # Contains a map from an element to the number of duplicates it has.
        # Used to temporarily allow duplicates in the list.
        self._duplicates = dict()

        nargs = len(args)
        if nargs == 0:
            super(ListSet, self).__init__()
            self._itemSet = set()
        elif nargs == 1:
            if isinstance(args[0], int):
                initialCapacity, = args
                super(ListSet, self).__init__()#initialCapacity)
                self._itemSet = set()#initialCapacity)
            else:
                c, = args
                super(ListSet, self).__init__(c)
                self._itemSet = set()#len(c))
                self._itemSet = self._itemSet.union(c)
        else:
            raise ValueError, 'too many arguments'

    # Delegate contains operations to the set

    def contains(self, o):
        return o in self._itemSet


    def __contains__(self, item):
        return self.contains(item)


    def containsAll(self, c):
        for cc in c:
            if cc not in self._itemSet:
                return False
        else:
            return True


    def append(self, val):
        return self.add(val)


    def insert(self, idx, val):
        return self.add(idx, val)


    # Methods for updating the set when the list is updated.
    def add(self, *args):
        """Works as list.append or list.insert but returns
        immediately if the element is already in the ListSet.
        """
        nargs = len(args)
        if nargs == 1:
            e, = args
            if self.contains(e):
                # Duplicates are not allowed
                return False
            if not super(ListSet, self).__contains__(e):
                super(ListSet, self).append(e)
                self._itemSet.add(e)
                return True
            else:
                return False
        elif nargs == 2:
            index, element = args
            if self.contains(element):
                # Duplicates are not allowed
                return
            super(ListSet, self).insert(index, element)
            self._itemSet.add(element)
        else:
            raise ValueError, 'invalid number of arguments'


    def extend(self, iterable):
        return self.addAll(iterable)


    def addAll(self, *args):
        nargs = len(args)
        if nargs == 1:
            c, = args
            modified = False
            for e in c:
                if self.contains(e):
                    continue

                if self.add(e):
                    self._itemSet.add(e)
                    modified = True

            return modified
        elif nargs == 2:
            index, c = args
            #self.ensureCapacity(len(self) + len(c))
            modified = False
            for e in c:
                if self.contains(e):
                    continue
                self.add(index, e)
                index += 1
                self._itemSet.add(e)
                modified = True
            return modified
        else:
            raise ValueError, 'invalid number of arguments'


    def clear(self):
        del self[:]
        self._itemSet.clear()


    def index(self, val):
        return self.indexOf(val)


    def indexOf(self, o):
        if not self.contains(o):
            return -1
        return super(ListSet, self).index(o)


    def lastIndexOf(self, o):
        if not self.contains(o):
            return -1
        return self[::-1].index(o)


    def remove(self, o):
        if isinstance(o, int):
            index = o
            e = super(ListSet, self).pop(index)
            if e is not None:
                self._itemSet.remove(e)
            return e
        else:
            if super(ListSet, self).remove(o):
                self._itemSet.remove(o)
                return True
            else:
                return False


    def removeRange(self, fromIndex, toIndex):
        toRemove = set()
        for idx in range(fromIndex, toIndex):
            toRemove.add(self[idx])
        del self[fromIndex:toIndex]
        for r in toRemove:
            self._itemSet.remove(r)


    def set(self, index, element):  #@PydevCodeAnalysisIgnore
        if element in self:
            # Element already exist in the list
            if self[index] == element:
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

        old = self[index] = element
        self.removeFromSet(old)
        self._itemSet.add(element)

        return old


    def removeFromSet(self, e):
        """Removes "e" from the set if it no longer exists in the list.
        """
        dupl = self._duplicates.get(e)
        if dupl is not None:
            # A duplicate was present so we only decrement the duplicate count
            # and continue
            if dupl == 1:
                # This is what always should happen. A sort sets the items one
                # by one, temporarily breaking the uniqueness requirement.
                del self._duplicates[e]
            else:
                self._duplicates[e] = dupl - 1
        else:
            # The "old" value is no longer in the list.
            self._itemSet.remove(e)


    def addDuplicate(self, element):
        """Marks the "element" can be found more than once from the list.
        Allowed in L{set} to make sorting work.
        """
        nr = self._duplicates.get(element)
        if nr is None:
            nr = 1
        else:
            nr += 1

        # Store the number of duplicates of this element so we know later on if
        # we should remove an element from the set or if it was a duplicate (in
        # removeFromSet)
        self._duplicates[element] = nr


    def clone(self):
        v = ListSet(self[:])
        v._itemSet = set(self._itemSet)
        return v
