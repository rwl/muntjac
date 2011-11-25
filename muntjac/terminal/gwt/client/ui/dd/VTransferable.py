# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
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
