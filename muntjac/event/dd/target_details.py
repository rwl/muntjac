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

"""wraps drop target related information about DragAndDropEvent."""


class ITargetDetails(object):
    """ITargetDetails wraps drop target related information about
    L{DragAndDropEvent}.

    When a ITargetDetails object is used in L{DropHandler} it is often
    preferable to cast the ITargetDetails to an implementation provided by
    DropTarget like L{TreeTargetDetails}. They often provide a better typed,
    drop target specific API.
    """

    def getData(self, key):
        """Gets target data associated with the given string key

        @return: The data associated with the key
        """
        raise NotImplementedError


    def getTarget(self):
        """@return: the drop target on which the L{DragAndDropEvent}
        happened."""
        raise NotImplementedError
