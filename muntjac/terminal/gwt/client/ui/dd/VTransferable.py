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

# from java.util.Collection import (Collection,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)


class VTransferable(object):
    """Client side counterpart for Transferable in com.vaadin.event.Transferable"""
    _component = None
    _variables = dict()

    def getDragSource(self):
        """Returns the component from which the transferable is created (eg. a tree
        which node is dragged).

        @return the component
        """
        return self._component

    def setDragSource(self, component):
        """Sets the component currently being dragged or from which the transferable
        is created (eg. a tree which node is dragged).
        <p>
        The server side counterpart of the component may implement
        {@link DragSource} interface if it wants to translate or complement the
        server side instance of this Transferable.

        @param component
                   the component to set
        """
        self._component = component

    def getData(self, dataFlawor):
        return self._variables[dataFlawor]

    def setData(self, dataFlawor, value):
        self._variables.put(dataFlawor, value)

    def getDataFlavors(self):
        return self._variables.keys()

    def getVariableMap(self):
        """This helper method should only be called by {@link VDragAndDropManager}.

        @return data in this Transferable that needs to be moved to server.
        """
        return self._variables
