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

from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.component import Event as ComponentEvent


class IFragmentChangedListener(object):
    """Listener that listens changes in URI fragment."""

    def fragmentChanged(self, source):
        raise NotImplementedError


_FRAGMENT_CHANGED_METHOD = getattr(IFragmentChangedListener, 'fragmentChanged')


class UriFragmentUtility(AbstractComponent):
    """Experimental web browser dependent component for URI fragment (part
    after hash mark "#") reading and writing.

    Component can be used to workaround common ajax web applications pitfalls:
    bookmarking a program state and back button.
    """

    CLIENT_WIDGET = None #ClientWidget(VUriFragmentUtility, LoadStyle.EAGER)


    def addListener(self, listener, iface=None):
        if (isinstance(listener, IFragmentChangedListener) and
                (iface is None or issubclass(iface, IFragmentChangedListener))):
            self.registerListener(FragmentChangedEvent,
                    listener, _FRAGMENT_CHANGED_METHOD)

        super(UriFragmentUtility, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, FragmentChangedEvent):
            self.registerCallback(FragmentChangedEvent, callback, None, *args)
        else:
            super(UriFragmentUtility, self).addCallback(callback,
                    eventType, *args)


    def removeListener(self, listener, iface=None):
        if (isinstance(listener, IFragmentChangedListener) and
                (iface is None or issubclass(iface, IFragmentChangedListener))):
            self.withdrawListener(FragmentChangedEvent,
                    listener, _FRAGMENT_CHANGED_METHOD)

        super(UriFragmentUtility, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, FragmentChangedEvent):
            self.withdrawCallback(FragmentChangedEvent, callback)
        else:
            super(UriFragmentUtility, self).removeCallback(callback, eventType)


    def __init__(self):
        super(UriFragmentUtility, self).__init__()

        self._fragment = None

        # immediate by default
        self.setImmediate(True)


    def paintContent(self, target):
        super(UriFragmentUtility, self).paintContent(target)
        value = self._fragment if self._fragment is not None else ''
        target.addVariable(self, 'fragment', value)


    def changeVariables(self, source, variables):
        super(UriFragmentUtility, self).changeVariables(source, variables)
        self._fragment = variables.get('fragment')
        self.fireEvent( FragmentChangedEvent(self) )


    def getFragment(self):
        """Gets currently set URI fragment.

        To listen changes in fragment, hook a L{IFragmentChangedListener}.

        Note that initial URI fragment that user used to enter the application
        will be read after application init. It fires FragmentChangedEvent
        only if it is not the same as on server side.

        @return: the current fragment in browser uri or null if not known
        """
        return self._fragment


    def setFragment(self, newFragment, fireEvent=True):
        """Sets URI fragment. Optionally fires a L{FragmentChangedEvent}

        @param newFragment:
                   id of the new fragment
        @param fireEvent:
                   true to fire event
        @see: L{FragmentChangedEvent}
        @see: L{IFragmentChangedListener}
        """
        if ((newFragment is None and self._fragment is not None)
                or (newFragment is not None
                        and newFragment != self._fragment)):
                self._fragment = newFragment
                if fireEvent:
                    fireEvent( FragmentChangedEvent(self) )

                self.requestRepaint()


class FragmentChangedEvent(ComponentEvent):
    """Event fired when uri fragment changes."""

    def __init__(self, source):
        """Creates a new instance of UriFragmentReader change event.

        @param source:
                   the Source of the event.
        """
        super(FragmentChangedEvent, self).__init__(source)


    def getUriFragmentUtility(self):
        """Gets the UriFragmentReader where the event occurred.

        @return: the Source of the event.
        """
        return self.getSource()
