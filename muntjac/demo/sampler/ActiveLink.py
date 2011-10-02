# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
# from com.vaadin.terminal.PaintException import (PaintException,)
# from com.vaadin.terminal.PaintTarget import (PaintTarget,)
# from com.vaadin.terminal.Resource import (Resource,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.ClientWidget import (ClientWidget,)
# from com.vaadin.ui.Component import (Component,)
# from com.vaadin.ui.Link import (Link,)
# from java.io.Serializable import (Serializable,)
# from java.lang.reflect.Method import (Method,)
# from java.util.HashSet import (HashSet,)
# from java.util.Map import (Map,)


class ActiveLink(Link):
    _LINK_FOLLOWED_METHOD = None
    _listeners = set()

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(ActiveLink, self)()
        elif _1 == 2:
            caption, resource = _0
            super(ActiveLink, self)(caption, resource)
        elif _1 == 6:
            caption, resource, targetName, width, height, border = _0
            super(ActiveLink, self)(caption, resource, targetName, width, height, border)
        else:
            raise ARGERROR(0, 6)

    # This should never happen
    try:
        _LINK_FOLLOWED_METHOD = LinkActivatedListener.getDeclaredMethod('linkActivated', [LinkActivatedEvent])
    except java.lang.NoSuchMethodException, e:
        raise java.lang.RuntimeException('Internal error finding methods in ActiveLink')

    def addListener(self, listener):
        """Adds the link activated listener.

        @param listener
                   the Listener to be added.
        """
        self._listeners.add(listener)
        self.addListener(self.LinkActivatedEvent, listener, self._LINK_FOLLOWED_METHOD)
        if len(self._listeners) == 1:
            self.requestRepaint()

    def removeListener(self, listener):
        """Removes the link activated listener.

        @param listener
                   the Listener to be removed.
        """
        self._listeners.remove(listener)
        self.removeListener(ClickEvent, listener, self._LINK_FOLLOWED_METHOD)
        if len(self._listeners) == 0:
            self.requestRepaint()

    def fireClick(self, linkOpened):
        """Emits the options change event."""
        self.fireEvent(self.LinkActivatedEvent(self, linkOpened))

    def paintContent(self, target):
        super(ActiveLink, self).paintContent(target)
        if len(self._listeners) > 0:
            target.addVariable(self, 'activated', False)
            target.addVariable(self, 'opened', False)

    def changeVariables(self, source, variables):
        super(ActiveLink, self).changeVariables(source, variables)
        if not self.isReadOnly() and 'activated' in variables:
            activated = variables['activated']
            opened = variables['opened']
            if (
                activated is not None and activated.booleanValue() and not self.isReadOnly()
            ):
                self.fireClick(True if opened is not None and opened.booleanValue() else False)

    class LinkActivatedEvent(Component.Event):
        _linkOpened = None

        def __init__(self, source, linkOpened):
            """New instance of text change event.

            @param source
                       the Source of the event.
            """
            super(LinkActivatedEvent, self)(source)
            self._linkOpened = linkOpened

        def getActiveLink(self):
            """Gets the ActiveLink where the event occurred.

            @return the Source of the event.
            """
            return self.getSource()

        def isLinkOpened(self):
            """Indicates whether or not the link was opened on the client, i.e in a
            new window/tab. If the link was not opened, the listener should react
            to the event and "do something", otherwise the link does nothing.

            @return true if the link was opened on the client
            """
            return self._linkOpened

    class LinkActivatedListener(Serializable):
        """ActiveLink click listener"""

        def linkActivated(self, event):
            """ActiveLink has been activated.

            @param event
                       ActiveLink click event.
            """
            pass
