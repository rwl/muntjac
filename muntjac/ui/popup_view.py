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

from warnings import warn

from muntjac.ui.abstract_component_container import AbstractComponentContainer
from muntjac.ui.component import Event as ComponentEvent
from muntjac.ui.abstract_component import AbstractComponent


class IPopupVisibilityListener(object):
    """Defines a listener that can receive a PopupVisibilityEvent when the
    visibility of the popup changes.
    """

    def popupVisibilityChange(self, event):
        """Pass to L{PopupView.PopupVisibilityEvent} to start listening
        for popup visibility changes.

        @param event: the event

        @see: L{PopupVisibilityEvent}
        @see: L{PopupView.addListener}
        """
        raise NotImplementedError


_POPUP_VISIBILITY_METHOD = getattr(IPopupVisibilityListener,
        'popupVisibilityChange')


class SingleComponentIterator(object):
    """Iterator for the visible components (zero or one components), used by
    L{PopupView.getComponentIterator}.
    """

    def __init__(self, component):
        self._component = component
        self._first = component is None


    def __iter__(self):
        return self


    def hasNext(self):
        return not self._first


    def next(self):  #@PydevCodeAnalysisIgnore
        if not self._first:
            self._first = True
            return self._component
        else:
            raise StopIteration


    def remove(self):
        raise NotImplementedError


class PopupView(AbstractComponentContainer):
    """A component for displaying a two different views to data. The minimized
    view is normally used to render the component, and when it is clicked the
    full view is displayed on a popup. The class L{popup_view.IContent} is
    used to deliver contents to this component.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    """

    CLIENT_WIDGET = None #ClientWidget(VPopupView, LoadStyle.EAGER)

    def __init__(self, *args):
        """A simple way to create a PopupPanel. Note that the minimal
        representation may not be dynamically updated.

        Alternatively, creates a PopupView through the IContent interface.
        This allows the creator to dynamically change the contents of the
        PopupView.

        @param args: tuple of the form
            - (small, large)
              1. the minimal textual representation as HTML
              2. the full, Component-type representation
            - (content)
              1. the IContent that contains the information for this
        """
        self._content = None
        self._hideOnMouseOut = None
        self._visibleComponent = None

        nargs = len(args)
        if nargs == 1:
            content, = args
            super(PopupView, self).__init__()
            self._hideOnMouseOut = True
            self.setContent(content)
        elif nargs == 2:
            small, large = args

            c = InnerContent(small, large)
            PopupView.__init__(self, c)
        else:
            raise ValueError, 'invalid number of arguments'


    def setContent(self, newContent):
        """This method will replace the current content of the panel with
        a new one.

        @param newContent:
                   IContent object containing new information
                   for the PopupView
        @raise ValueError:
                    if the method is passed a null value, or if one of
                    the content methods returns null
        """
        if newContent is None:
            raise ValueError, 'IContent must not be null'
        self._content = newContent
        self.requestRepaint()


    def getContent(self):
        """Returns the content-package for this PopupView.

        @return: the IContent for this object or null
        """
        return self._content


    def setPopupVisibility(self, visible):
        """@deprecated: Use L{setPopupVisible} instead."""
        warn('use setPopupVisible() instead', DeprecationWarning)
        self.setPopupVisible(visible)

    def getPopupVisibility(self):
        """@deprecated: Use L{isPopupVisible} instead."""
        warn('use isPopupVisible() instead', DeprecationWarning)
        return self.isPopupVisible()


    def setPopupVisible(self, visible):
        """Set the visibility of the popup. Does not hide the minimal
        representation.
        """
        if self.isPopupVisible() != visible:
            if visible:
                self._visibleComponent = self._content.getPopupComponent()
                if self._visibleComponent is None:
                    raise ValueError, ('PopupView.IContent did not return '
                            'Component to set visible')
                super(PopupView, self).addComponent(self._visibleComponent)
            else:
                super(PopupView, self).removeComponent(self._visibleComponent)
                self._visibleComponent = None
            self.fireEvent( PopupVisibilityEvent(self) )
            self.requestRepaint()


    def isPopupVisible(self):
        """Return whether the popup is visible.

        @return: true if the popup is showing
        """
        return self._visibleComponent is not None


    def isHideOnMouseOut(self):
        """Check if this popup will be hidden when the user takes the mouse
        cursor out of the popup area.

        @return: true if the popup is hidden on mouse out, false otherwise
        """
        return self._hideOnMouseOut

    # Methods inherited from AbstractComponentContainer. These are unnecessary
    # (but mandatory). Most of them are not supported in this implementation.

    def setHideOnMouseOut(self, hideOnMouseOut):
        """Should the popup automatically hide when the user takes the mouse
        cursor out of the popup area? If this is false, the user must click
        outside the popup to close it. The default is true.
        """
        self._hideOnMouseOut = hideOnMouseOut


    def getComponentIterator(self):
        """This class only contains other components when the popup is
        showing.

        @see: L{ComponentContainer.getComponentIterator}
        """
        return SingleComponentIterator(self._visibleComponent)


    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the
        iterator returned by L{getComponentIterator}.

        @return: the number of contained components (zero or one)
        """
        return 1 if self._visibleComponent is not None else 0


    def removeAllComponents(self):
        """Not supported in this implementation.

        @see: L{AbstractComponentContainer.removeAllComponents}
        @raise NotImplementedError:
        """
        raise NotImplementedError


    def moveComponentsFrom(self, source):
        """Not supported in this implementation.

        @see: L{AbstractComponentContainer.moveComponentsFrom}
        @raise NotImplementedError:
        """
        raise NotImplementedError


    def addComponent(self, c):
        """Not supported in this implementation.

        @see: L{AbstractComponentContainer.addComponent}
        @raise NotImplementedError:
        """
        raise NotImplementedError


    def replaceComponent(self, oldComponent, newComponent):
        """Not supported in this implementation.

        @see: L{ComponentContainer.replaceComponent}
        @raise NotImplementedError:
        """
        raise NotImplementedError


    def removeComponent(self, c):
        """Not supported in this implementation

        @see: L{AbstractComponentContainer.removeComponent}
        """
        raise NotImplementedError

    # Methods for server-client communications.

    def paintContent(self, target):
        """Paint (serialize) the component for the client.

        @see: L{AbstractComponent.paintContent}
        """
        # Superclass writes any common attributes in the paint target.
        super(PopupView, self).paintContent(target)

        html = self._content.getMinimizedValueAsHTML()
        if html is None:
            html = ''

        target.addAttribute('html', html)
        target.addAttribute('hideOnMouseOut', self._hideOnMouseOut)

        # Only paint component to client if we know that the popup is showing
        if self.isPopupVisible():
            target.startTag('popupComponent')
            self._visibleComponent.paint(target)
            target.endTag('popupComponent')

        target.addVariable(self, 'popupVisibility', self.isPopupVisible())


    def changeVariables(self, source, variables):
        """Deserialize changes received from client.

        @see: L{AbstractComponent.changeVariables}
        """
        if 'popupVisibility' in variables:
            self.setPopupVisible( bool(variables.get('popupVisibility')) )


    def addListener(self, listener, iface=None):
        """Add a listener that is called whenever the visibility of the
        popup is changed.

        @param listener: the listener to add
        @see: L{IPopupVisibilityListener}
        @see: L{PopupVisibilityEvent}
        @see: L{removeListener}
        """
        if (isinstance(listener, IPopupVisibilityListener) and
                (iface is None or issubclass(iface, IPopupVisibilityListener))):
            self.registerListener(PopupVisibilityEvent,
                    listener, _POPUP_VISIBILITY_METHOD)

        super(PopupView, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, PopupVisibilityEvent):
            self.registerCallback(ClickEvent, callback, None, *args)
        else:
            super(PopupView, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        """Removes a previously added listener, so that it no longer receives
        events when the visibility of the popup changes.

        @param listener: the listener to remove
        @see: L{IPopupVisibilityListener}
        @see: L{addListener}
        """
        if (isinstance(listener, IPopupVisibilityListener) and
                (iface is None or issubclass(iface, IPopupVisibilityListener))):
            self.withdrawListener(PopupVisibilityEvent, listener,
                    _POPUP_VISIBILITY_METHOD)

        super(PopupView, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, PopupVisibilityEvent):
            self.withdrawCallback(PopupVisibilityEvent, callback)
        else:
            super(PopupView, self).removeCallback(callback, eventType)


class PopupVisibilityEvent(ComponentEvent):
    """This event is received by the PopupVisibilityListeners when the
    visibility of the popup changes. You can get the new visibility directly
    with L{isPopupVisible}, or get the PopupView that produced the event with
    L{getPopupView}.
    """

    def __init__(self, source):
        super(PopupVisibilityEvent, self).__init__(source)


    def getPopupView(self):
        """Get the PopupView instance that is the source of this event.

        @return: the source PopupView
        """
        return self.getSource()


    def isPopupVisible(self):
        """Returns the current visibility of the popup.

        @return: true if the popup is visible
        """
        return self.getPopupView().isPopupVisible()


class IContent(object):
    """Used to deliver customized content-packages to the PopupView. These
    are dynamically loaded when they are redrawn. The user must take care
    that neither of these methods ever return null.
    """

    def getMinimizedValueAsHTML(self):
        """This should return a small view of the full data.

        @return: value in HTML format
        """
        raise NotImplementedError


    def getPopupComponent(self):
        """This should return the full Component representing the data

        @return: a Component for the value
        """
        raise NotImplementedError


class InnerContent(IContent):

    def __init__(self, small, large):
        self._small = small
        self._large = large


    def getMinimizedValueAsHTML(self):
        return self._small


    def getPopupComponent(self):
        return self._large
