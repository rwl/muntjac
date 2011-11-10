
from muntjac.api import Link
from muntjac.ui.button import ClickEvent
from muntjac.ui.component import Event


class ILinkActivatedListener(object):
    """ActiveLink click listener"""

    def linkActivated(self, event):
        """ActiveLink has been activated.

        @param event:
                   ActiveLink click event.
        """
        raise NotImplementedError


_LINK_FOLLOWED_METHOD = getattr(ILinkActivatedListener, 'linkActivated')


class ActiveLink(Link):

    CLIENT_WIDGET = None #ClientWidget(VActiveLink)

    def __init__(self, caption=None, resource=None, targetName=None,
                width=None, height=None, border=None):
        self._listeners = set()

        if caption is None:
            super(ActiveLink, self).__init__()
        elif targetName is None:
            super(ActiveLink, self).__init__(caption, resource)
        else:
            super(ActiveLink, self).__init__(caption, resource, targetName,
                    width, height, border)


    def addListener(self, listener, iface=None):
        """Adds the link activated listener.

        @param listener:
                   the Listener to be added.
        """
        if (isinstance(listener, ILinkActivatedListener) and
                (iface is None or issubclass(iface, ILinkActivatedListener))):
            self._listeners.add(listener)

            super(ActiveLink, self).registerListener(LinkActivatedEvent,
                    listener, _LINK_FOLLOWED_METHOD)

            if len(self._listeners) == 1:
                self.requestRepaint()

        super(ActiveLink, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, LinkActivatedEvent):
            self.registerCallback(LinkActivatedEvent, callback, None, *args)
        else:
            super(ActiveLink, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        """Removes the link activated listener.

        @param listener:
                   the Listener to be removed.
        """
        if (isinstance(listener, ILinkActivatedListener) and
                (iface is None or iface == ILinkActivatedListener)):
            self._listeners.remove(listener)

            super(ActiveLink, self).withdrawListener(ClickEvent, listener,
                    _LINK_FOLLOWED_METHOD)

            if len(self._listeners) == 0:
                self.requestRepaint()

        super(ActiveLink, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, LinkActivatedEvent):
            self._listeners.remove(callback)

            super(ActiveLink, self).withdrawListener(ClickEvent, callback,
                    None)

            if len(self._listeners) == 0:
                self.requestRepaint()
        else:
            super(ActiveLink, self).removeCallback(callback, eventType)


    def fireClick(self, linkOpened):
        """Emits the options change event."""
        event = LinkActivatedEvent(self, linkOpened)
        self.fireEvent(event)


    def paintContent(self, target):
        super(ActiveLink, self).paintContent(target)
        if len(self._listeners) > 0:
            target.addVariable(self, 'activated', False)
            target.addVariable(self, 'opened', False)


    def changeVariables(self, source, variables):
        super(ActiveLink, self).changeVariables(source, variables)
        if not self.isReadOnly() and ('activated' in variables):
            activated = variables.get('activated')
            opened = variables.get('opened')
            if (activated is not None and bool(activated)
                    and not self.isReadOnly()):
                if (opened is not None) and bool(opened):
                    self.fireClick(True)
                else:
                    self.fireClick(False)


class LinkActivatedEvent(Event):

    def __init__(self, source, linkOpened):
        """New instance of text change event.

        @param source:
                   the Source of the event.
        """
        super(LinkActivatedEvent, self).__init__(source)
        self._linkOpened = linkOpened


    def getActiveLink(self):
        """Gets the ActiveLink where the event occurred.

        @return: the Source of the event.
        """
        return self.getSource()


    def isLinkOpened(self):
        """Indicates whether or not the link was opened on the client, i.e in a
        new window/tab. If the link was not opened, the listener should react
        to the event and "do something", otherwise the link does nothing.

        @return: true if the link was opened on the client
        """
        return self._linkOpened
