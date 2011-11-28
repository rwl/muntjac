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

from pyjamas import DOM
from pyjamas.ui import RootPanel

from muntjac.terminal.gwt.client.ui.v_window import VWindow
from muntjac.terminal.gwt.client.ui.v_view import VView
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.ui.sub_part_aware import SubPartAware


class ComponentLocator(object):
    """ComponentLocator provides methods for generating a String locator for a
    given DOM element and for locating a DOM element using a String locator.
    """

    #: Separator used in the String locator between a parent and a child widget.
    _PARENTCHILD_SEPARATOR = '/'

    #: Separator used in the String locator between the part identifying the
    #  containing widget and the part identifying the target element within the
    #  widget.
    _SUBPART_SEPARATOR = '#'

    #: String that identifies the root panel when appearing first in the String
    #  locator.
    _ROOT_ID = 'Root'


    def __init__(self, client):
        """Construct a ComponentLocator for the given ApplicationConnection.

        @param client:
                   ApplicationConnection instance for the application.
        """
        #: Reference to ApplicationConnection instance.
        self._client = client


    def getPathForElement(self, targetElement):
        """Generates a String locator which uniquely identifies the target
        element. The L{getElementByPath} method can be used for the inverse
        operation, i.e. locating an element based on the return value from this
        method.

        Note that getElementByPath(getPathForElement(element)) == element is
        not always true as L{getPathForElement} can return a path to
        another element if the widget determines an action on the other element
        will give the same result as the action on the target element.

        @param targetElement:
                   The element to generate a path for.
        @return: A String locator that identifies the target element or null
                 if a String locator could not be created.
        """
        pid = None

        e = targetElement

        while True:
            pid = self._client.getPid(e)
            if pid is not None:
                break

            e = DOM.getParent(e)
            if e is None:
                break

        w = None
        if pid is not None:
            # If we found a Paintable then we use that as reference. We should
            # find the Paintable for all but very special cases (like
            # overlays).
            w = self._client.getPaintable(pid)

            # Still if the Paintable contains a widget that implements
            # SubPartAware, we want to use that as a reference
            targetParent = self.findParentWidget(targetElement, w)
            while targetParent != w and targetParent is not None:
                if isinstance(targetParent, SubPartAware):
                    # The targetParent widget is a child of the Paintable and
                    # the first parent (of the targetElement) that implements
                    # SubPartAware
                    w = targetParent
                    break

                targetParent = targetParent.getParent()

        if w is None:
            # Check if the element is part of a widget that is attached
            # directly to the root panel
            rootPanel = RootPanel.get()
            rootWidgetCount = rootPanel.getWidgetCount()
            for i in range(rootWidgetCount):
                rootWidget = rootPanel.getWidget(i)
                if rootWidget.getElement().isOrHasChild(targetElement):
                    # The target element is contained by this root widget
                    w = self.findParentWidget(targetElement, rootWidget)
                    break

            if w is not None:
                # We found a widget but we should still see if we find a
                # SubPartAware implementor (we cannot find the Paintable as
                # there is no link from VOverlay to its paintable/owner).
                subPartAwareWidget = self.findSubPartAwareParentWidget(w)
                if subPartAwareWidget is not None:
                    w = subPartAwareWidget

        if w is None:
            # Containing widget not found
            return None

        # Determine the path for the target widget
        path = self.getPathForWidget(w)
        if path is None:
            # No path could be determined for the target widget. Cannot create
            # a locator string.
            return None

        if w.getElement() == targetElement:
            # We are done if the target element is the root of the target
            # widget.
            return path
        elif isinstance(w, SubPartAware):
            # If the widget can provide an identifier for the targetElement we
            # let it do that
            elementLocator = w.getSubPartName(targetElement)
            if elementLocator is not None:
                return path + self._SUBPART_SEPARATOR + elementLocator

        # If everything else fails we use the DOM path to identify the target
        # element
        return path + self.getDOMPathForElement(targetElement, w.getElement())


    def findSubPartAwareParentWidget(self, w):
        """Finds the first widget in the hierarchy (moving upwards) that
        implements SubPartAware. Returns the SubPartAware implementor or
        null if none is found.

        @param w:
                   The widget to start from. This is returned if it implements
                   SubPartAware.
        @return: The first widget (upwards in hierarchy) that implements
                 SubPartAware or null
        """
        while w is not None:
            if isinstance(w, SubPartAware):
                return w

            w = w.getParent()

        return None


    def findParentWidget(self, targetElement, ancestorWidget):
        """Returns the first widget found when going from C{targetElement}
        upwards in the DOM hierarchy, assuming that C{ancestorWidget} is a
        parent of C{targetElement}.

        @return: The widget whose root element is a parent of C{targetElement}.
        """
        # As we cannot resolve Widgets from the element we start from the
        # widget and move downwards to the correct child widget, as long as we
        # find one.
        if isinstance(ancestorWidget, HasWidgets):
            for w in ancestorWidget:
                if w.getElement().isOrHasChild(targetElement):
                    return self.findParentWidget(targetElement, w)

        # No children found, this is it
        return ancestorWidget


    def getElementByDOMPath(self, baseElement, path):
        """Locates an element based on a DOM path and a base element.

        @param baseElement:
                   The base element which the path is relative to
        @param path:
                   String locator (consisting of domChild[x] parts) that
                   identifies the element
        @return: The element identified by path, relative to baseElement
                 or null if the element could not be found.
        """
        parts = path.split(self._PARENTCHILD_SEPARATOR)
        element = baseElement

        for part in parts:
            if part.startswith('domChild['):
                childIndexString = part[len('domChild['):-1]
                try:
                    childIndex = int(childIndexString)
                    element = DOM.getChild(element, childIndex)
                except Exception:
                    return None

        return element


    def getDOMPathForElement(self, element, baseElement):
        """Generates a String locator using domChild[x] parts for the element
        relative to the baseElement.

        @param element:
                   The target element
        @param baseElement:
                   The starting point for the locator. The generated path is
                   relative to this element.
        @return: A String locator that can be used to locate the target element
                 using L{getElementByDOMPath} or null if the locator String
                 cannot be created.
        """
        e = element
        path = ''
        while True:
            parent = DOM.getParent(e)
            if parent is None:
                return None

            childIndex = -1

            childCount = DOM.getChildCount(parent)
            for i in range(childCount):
                if e == DOM.getChild(parent, i):
                    childIndex = i
                    break

            if childIndex == -1:
                return None

            path = (self._PARENTCHILD_SEPARATOR + 'domChild[' + childIndex
                    + ']' + path)

            if parent == baseElement:
                break

            e = parent

        return path


    def getElementByPath(self, path):
        """Locates an element using a String locator (path) which identifies a
        DOM element. The L{getPathForElement} method can be used for the
        inverse operation, i.e. generating a string expression for a DOM
        element.

        @param path:
                   The String locater which identifies the target element.
        @return: The DOM element identified by {@code path} or null if the
                 element could not be located.
        """
        # Path is of type "targetWidgetPath#componentPart" or
        # "targetWidgetPath".
        parts = path.split(self._SUBPART_SEPARATOR, 2)
        widgetPath = parts[0]
        w = self.getWidgetFromPath(widgetPath)
        if (w is None) or (not Util.isAttachedAndDisplayed(w)):
            return None

        if len(parts) == 1:
            pos = widgetPath.find('domChild')
            if pos == -1:
                return w.getElement()

            # Contains dom reference to a sub element of the widget
            subPath = widgetPath[pos:]
            return self.getElementByDOMPath(w.getElement(), subPath)
        elif len(parts) == 2:
            if isinstance(w, SubPartAware):
                return w.getSubPartElement(parts[1])

        return None


    def getPathForWidget(self, w):
        """Creates a locator String for the given widget. The path can be used
        to locate the widget using L{getWidgetFromPath}.

        Returns null if no path can be determined for the widget or if the
        widget is null.

        @param w:
                   The target widget
        @return: A String locator for the widget
        """
        if w is None:
            return None

        pid = self._client.getPid(w.getElement())
        if self.isStaticPid(pid):
            return pid

        if isinstance(w, VView):
            return ''
        elif isinstance(w, VWindow):
            win = w
            subWindowList = self._client.getView().getSubWindowList()
            indexOfSubWindow = subWindowList.index(win)
            return (self._PARENTCHILD_SEPARATOR + 'VWindow['
                    + indexOfSubWindow + ']')
        elif isinstance(w, RootPanel):
            return self._ROOT_ID

        parent = w.getParent()

        basePath = self.getPathForWidget(parent)
        if basePath is None:
            return None

        simpleName = Util.getSimpleName(w)

        # Check if the parent implements Iterable. At least VPopupView does not
        # implement HasWdgets so we cannot check for that.
        if not hasattr(parent, '__iter__'):
            # Parent does not implement Iterable so we cannot find out which
            # child this is
            return None

        pos = 0
        for child in parent:
            if child == w:
                return (basePath + self._PARENTCHILD_SEPARATOR + simpleName
                        + '[' + pos + ']')

            simpleName2 = Util.getSimpleName(child)
            if simpleName == simpleName2:
                pos += 1

        return None


    def getWidgetFromPath(self, path):
        """Locates the widget based on a String locator.

        @param path:
                   The String locator that identifies the widget.
        @return: The Widget identified by the String locator or null if the
                 widget could not be identified.
        """
        w = None
        parts = path.split(self._PARENTCHILD_SEPARATOR)

        for part in parts:
            if part == self._ROOT_ID:
                w = RootPanel.get()
            elif part == '':
                w = self._client.getView()
            elif w is None:
                # Must be static pid (PID_S*)
                w = self._client.getPaintable(part)
            elif part.startswith('domChild['):
                # The target widget has been found and the rest identifies the
                # element
                break
            elif isinstance(w, object):
                # W identifies a widget that contains other widgets, as it
                # should. Try to locate the child
                parent = w

                # Part is of type "VVerticalLayout[0]", split this into
                # VVerticalLayout and 0
                split = part.split('\\[', 2)
                widgetClassName = split[0]
                indexString = split[1]
                widgetPosition = int(indexString[:-1])

                # Locate the child
                # VWindow and VContextMenu workarounds for backwards
                # compatibility
                if widgetClassName == 'VWindow':
                    iterator = self._client.getView().getSubWindowList()
                elif widgetClassName == 'VContextMenu':
                    return self._client.getContextMenu()
                else:
                    iterator = parent

                ok = False

                # Find the widgetPosition:th child of type "widgetClassName"
                for child in iterator:
                    simpleName2 = Util.getSimpleName(child)

                    if widgetClassName == simpleName2:
                        if widgetPosition == 0:
                            w = child
                            ok = True
                            break

                        widgetPosition -= 1

                if not ok:
                    # Did not find the child
                    return None
            else:
                # W identifies something that is not a "HasWidgets". This
                # should not happen as all widget containers should implement
                # HasWidgets.
                return None

        return w


    def isStaticPid(self, pid):
        """Checks if the given pid is a static pid.

        @param pid:
                   The pid to check
        @return: true if the pid is a static pid, false otherwise
        """
        if pid is None:
            return False

        return pid.startswith('PID_S')
