# Copyright (C) 2010 Abo Akademi University
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
# Note: This is a modified file from GAEContainer. For further information
#       please visit http://vaadin.com/directory#addon/gaecontainer.

from muntjac.data.item import IItem


class IVersionedGAEItem(IItem):
    """Interface for items that keeps track of their version (for optimistic
    locking).

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def commit(self):
        """Commits all the changes made to properties in this item.

        This method only makes sense if  L{VersionedGAEItem.isWriteThrough}
        is false.

        @raise ConcurrentModificationException:
        @raise NoSuchElementException
        """
        raise NotImplementedError


    def getVersion(self):
        """Gets the current version of this item as seen locally by the
        container.

        @return: version or -1 if not supported
        """
        raise NotImplementedError


    def isWriteThrough(self):
        """Is the properties of this item write trough or is a L{commit}
        required.

        @return: true if writeThrough
        """
        raise NotImplementedError
