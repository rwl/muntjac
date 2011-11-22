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

"""Defines an interface implemented by all classes that can be painted."""

from muntjac.util import IEventListener, EventObject


class IPaintable(IEventListener):
    """Interface implemented by all classes that can be painted. Classes
    implementing this interface know how to output themselves to a UIDL
    stream and that way describing to the terminal how it should be displayed
    in the UI.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.1
    """

    def paint(self, target):
        """Paints the IPaintable into a UIDL stream. This method creates the
        UIDL sequence describing it and outputs it to the given UIDL stream.

        It is called when the contents of the component should be painted in
        response to the component first being shown or having been altered so
        that its visual representation is changed.

        @param target:
                   the target UIDL stream where the component should paint
                   itself to.
        @raise PaintException:
                    if the paint operation failed.
        """
        raise NotImplementedError


    def requestRepaint(self):
        """Requests that the paintable should be repainted as soon as
        possible."""
        raise NotImplementedError


    def setDebugId(self, idd):
        """Adds an unique id for component that get's transferred to terminal
        for testing purposes. Keeping identifiers unique throughout the
        Application instance is on programmers responsibility.

        Note, that with the current terminal implementation the identifier
        cannot be changed while the component is visible. This means that the
        identifier should be set before the component is painted for the first
        time and kept the same while visible in the client.

        @param idd:
                   A short (< 20 chars) alphanumeric id
        """
        raise NotImplementedError


    def getDebugId(self):
        """Get's currently set debug identifier

        @return: current debug id, null if not set
        """
        raise NotImplementedError


    def addListener(self, listener, iface=None):
        """Adds repaint request listener. In order to assure that no repaint
        requests are missed, the new repaint listener should paint the
        paintable right after adding itself as listener.

        @param listener:
                   the listener to be added.
        """
        if (isinstance(listener, IRepaintRequestListener) and
                (iface is None or iface == IRepaintRequestListener)):
            raise NotImplementedError


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if eventType == RepaintRequestEvent:
            raise NotImplementedError


    def removeListener(self, listener, iface):
        """Removes repaint request listener.

        @param listener:
                   the listener to be removed.
        """
        if iface == IRepaintRequestListener:
            raise NotImplementedError
        else:
            super(IPaintable, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if eventType == RepaintRequestEvent:
            raise NotImplementedError


    def requestRepaintRequests(self):
        """Request sending of repaint events on any further visible changes.
        Normally the paintable only send up to one repaint request for
        listeners after paint as the paintable as the paintable assumes that
        the listeners already know about the repaint need. This method resets
        the assumtion. Paint implicitly does the assumtion reset functionality
        implemented by this method.

        This method is normally used only by the terminals to note paintables
        about implicit repaints (painting the component without actually
        invoking paint method).
        """
        raise NotImplementedError


class RepaintRequestEvent(EventObject):
    """Repaint request event is thrown when the paintable needs to be
    repainted. This is typically done when the C{paint} method
    would return dissimilar UIDL from the previous call of the method.
    """

    def __init__(self, source):
        """Constructs a new event.

        @param source:
                   the paintable needing repaint.
        """
        super(RepaintRequestEvent, self).__init__(source)


    def getPaintable(self):
        """Gets the paintable needing repainting.

        @return: IPaintable for which the C{paint} method will return
                dissimilar UIDL from the previous call of the method.
        """
        return self.getSource()


class IRepaintRequestListener(object):
    """Listens repaint requests. The C{repaintRequested} method is
    called when the paintable needs to be repainted. This is typically done
    when the C{paint} method would return dissimilar UIDL from the
    previous call of the method.
    """

    def repaintRequested(self, event):
        """Receives repaint request events.

        @param event:
                   the repaint request event specifying the paintable source.
        """
        raise NotImplementedError
