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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.ui.AbstractLayout import (AbstractLayout,)
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
# from com.vaadin.event.LayoutEvents.LayoutClickEvent import (LayoutClickEvent,)
# from com.vaadin.event.LayoutEvents.LayoutClickListener import (LayoutClickListener,)
# from com.vaadin.event.LayoutEvents.LayoutClickNotifier import (LayoutClickNotifier,)
# from java.io.Serializable import (Serializable,)
# from java.util.Collection import (Collection,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedHashSet import (LinkedHashSet,)
# from java.util.Map import (Map,)


class AbsoluteLayout(AbstractLayout, LayoutClickNotifier):
    """AbsoluteLayout is a layout implementation that mimics html absolute
    positioning.
    """
    _CLICK_EVENT = EventId.LAYOUT_CLICK
    # The components in the layout
    _components = LinkedHashSet()
    # Maps each component to a position
    _componentToCoordinates = dict()

    def __init__(self):
        """Creates an AbsoluteLayout with full size."""
        self.setSizeFull()

    def getComponentIterator(self):
        """Gets an iterator for going through all components enclosed in the
        absolute layout.
        """
        return self._components

    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the iterator
        returned by {@link #getComponentIterator()}.

        @return the number of contained components
        """
        return len(self._components)

    def replaceComponent(self, oldComponent, newComponent):
        """Replaces one component with another one. The new component inherits the
        old components position.
        """
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.ui.AbstractComponentContainer#addComponent(com.vaadin.ui.Component
        # )

        position = self.getPosition(oldComponent)
        self.removeComponent(oldComponent)
        self.addComponent(newComponent)
        self._componentToCoordinates.put(newComponent, position)

    def addComponent(self, *args):
        """None
        ---
        Adds a component to the layout. The component can be positioned by
        providing a string formatted in CSS-format.
        <p>
        For example the string "top:10px;left:10px" will position the component
        10 pixels from the left and 10 pixels from the top. The identifiers:
        "top","left","right" and "bottom" can be used to specify the position.
        </p>

        @param c
                   The component to add to the layout
        @param cssPosition
                   The css position string
        """
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.ui.AbstractComponentContainer#removeComponent(com.vaadin.ui
        # .Component)

        _0 = args
        _1 = len(args)
        if _1 == 1:
            c, = _0
            self._components.add(c)
            try:
                super(AbsoluteLayout, self).addComponent(c)
                self.requestRepaint()
            except IllegalArgumentException, e:
                self._components.remove(c)
                raise e
        elif _1 == 2:
            c, cssPosition = _0
            position = self.ComponentPosition()
            position.setCSSString(cssPosition)
            self._componentToCoordinates.put(c, position)
            # Remove component coordinates if adding fails
            try:
                self.addComponent(c)
            except IllegalArgumentException, e:
                self._componentToCoordinates.remove(c)
                raise e
        else:
            raise ARGERROR(1, 2)

    def removeComponent(self, c):
        self._components.remove(c)
        self._componentToCoordinates.remove(c)
        super(AbsoluteLayout, self).removeComponent(c)
        self.requestRepaint()

    # Create position instance and add it to componentToCoordinates map. We
    # need to do this before we call addComponent so the attachListeners
    # can access this position. #6368

    def getPosition(self, component):
        """Gets the position of a component in the layout. Returns null if component
        is not attached to the layout.

        @param component
                   The component which position is needed
        @return An instance of ComponentPosition containing the position of the
                component, or null if the component is not enclosed in the
                layout.
        """
        if component.getParent() != self:
            return None
        elif component in self._componentToCoordinates:
            return self._componentToCoordinates[component]
        else:
            coords = self.ComponentPosition()
            self._componentToCoordinates.put(component, coords)
            return coords

    class ComponentPosition(Serializable):
        """The CompontPosition class represents a components position within the
        absolute layout. It contains the attributes for left, right, top and
        bottom and the units used to specify them.
        """
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.ui.AbstractLayout#paintContent(com.vaadin.terminal.PaintTarget
        # )

        _zIndex = -1
        _topValue = None
        _rightValue = None
        _bottomValue = None
        _leftValue = None
        _topUnits = None
        _rightUnits = None
        _bottomUnits = None
        _leftUnits = None

        def setCSSString(self, css):
            """Sets the position attributes using CSS syntax. Attributes not
            included in the string are reset to their unset states.

            <code><pre>
            setCSSString("top:10px;left:20%;z-index:16;");
            </pre></code>

            @param css
            """
            self._topValue = self._rightValue = self._bottomValue = self._leftValue = None
            self._topUnits = self._rightUnits = self._bottomUnits = self._leftUnits = 0
            self._zIndex = -1
            if css is None:
                return
            cssProperties = css.split(';')
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(cssProperties)):
                    break
                keyValuePair = cssProperties[i].split(':')
                key = keyValuePair[0].trim()
                if key == '':
                    continue
                if key == 'z-index':
                    self._zIndex = int(keyValuePair[1].trim())
                else:
                    if len(keyValuePair) > 1:
                        value = keyValuePair[1].trim()
                    else:
                        value = ''
                    unit = value.replaceAll('[0-9\\.\\-]+', '')
                    if not (unit == ''):
                        value = value[:value.find(unit)].trim()
                    v = self.float(value)
                    unitInt = self.parseCssUnit(unit)
                    if key == 'top':
                        self._topValue = v
                        self._topUnits = unitInt
                    elif key == 'right':
                        self._rightValue = v
                        self._rightUnits = unitInt
                    elif key == 'bottom':
                        self._bottomValue = v
                        self._bottomUnits = unitInt
                    elif key == 'left':
                        self._leftValue = v
                        self._leftUnits = unitInt
            self.requestRepaint()

        def parseCssUnit(self, string):
            """Parses a string and checks if a unit is found. If a unit is not found
            from the string the unit pixels is used.

            @param string
                       The string to parse the unit from
            @return The found unit
            """
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < self.UNIT_SYMBOLS.length):
                    break
                if self.UNIT_SYMBOLS[i] == string:
                    return i
            return 0
            # defaults to px (eg. top:0;)

        def getCSSString(self):
            """Converts the internal values into a valid CSS string.

            @return A valid CSS string
            """
            s = ''
            if self._topValue is not None:
                s += 'top:' + self._topValue + self.UNIT_SYMBOLS[self._topUnits] + ';'
            if self._rightValue is not None:
                s += 'right:' + self._rightValue + self.UNIT_SYMBOLS[self._rightUnits] + ';'
            if self._bottomValue is not None:
                s += 'bottom:' + self._bottomValue + self.UNIT_SYMBOLS[self._bottomUnits] + ';'
            if self._leftValue is not None:
                s += 'left:' + self._leftValue + self.UNIT_SYMBOLS[self._leftUnits] + ';'
            if self._zIndex >= 0:
                s += 'z-index:' + self._zIndex + ';'
            return s

        def setTop(self, topValue, topUnits):
            """Sets the 'top' attribute; distance from the top of the component to
            the top edge of the layout.

            @param topValue
                       The value of the 'top' attribute
            @param topUnits
                       The unit of the 'top' attribute. See UNIT_SYMBOLS for a
                       description of the available units.
            """
            self._topValue = topValue
            self._topUnits = topUnits
            self.requestRepaint()

        def setRight(self, rightValue, rightUnits):
            """Sets the 'right' attribute; distance from the right of the component
            to the right edge of the layout.

            @param rightValue
                       The value of the 'right' attribute
            @param rightUnits
                       The unit of the 'right' attribute. See UNIT_SYMBOLS for a
                       description of the available units.
            """
            self._rightValue = rightValue
            self._rightUnits = rightUnits
            self.requestRepaint()

        def setBottom(self, bottomValue, bottomUnits):
            """Sets the 'bottom' attribute; distance from the bottom of the
            component to the bottom edge of the layout.

            @param bottomValue
                       The value of the 'bottom' attribute
            @param units
                       The unit of the 'bottom' attribute. See UNIT_SYMBOLS for a
                       description of the available units.
            """
            self._bottomValue = bottomValue
            self._bottomUnits = bottomUnits
            self.requestRepaint()

        def setLeft(self, leftValue, leftUnits):
            """Sets the 'left' attribute; distance from the left of the component to
            the left edge of the layout.

            @param leftValue
                       The value of the 'left' attribute
            @param units
                       The unit of the 'left' attribute. See UNIT_SYMBOLS for a
                       description of the available units.
            """
            self._leftValue = leftValue
            self._leftUnits = leftUnits
            self.requestRepaint()

        def setZIndex(self, zIndex):
            """Sets the 'z-index' attribute; the visual stacking order

            @param zIndex
                       The z-index for the component.
            """
            self._zIndex = zIndex
            self.requestRepaint()

        def setTopValue(self, topValue):
            """Sets the value of the 'top' attribute; distance from the top of the
            component to the top edge of the layout.

            @param topValue
                       The value of the 'left' attribute
            """
            self._topValue = topValue
            self.requestRepaint()

        def getTopValue(self):
            """Gets the 'top' attributes value in current units.

            @see #getTopUnits()
            @return The value of the 'top' attribute, null if not set
            """
            return self._topValue

        def getRightValue(self):
            """Gets the 'right' attributes value in current units.

            @return The value of the 'right' attribute, null if not set
            @see #getRightUnits()
            """
            return self._rightValue

        def setRightValue(self, rightValue):
            """Sets the 'right' attribute value (distance from the right of the
            component to the right edge of the layout). Currently active units
            are maintained.

            @param rightValue
                       The value of the 'right' attribute
            @see #setRightUnits(int)
            """
            self._rightValue = rightValue
            self.requestRepaint()

        def getBottomValue(self):
            """Gets the 'bottom' attributes value using current units.

            @return The value of the 'bottom' attribute, null if not set
            @see #getBottomUnits()
            """
            return self._bottomValue

        def setBottomValue(self, bottomValue):
            """Sets the 'bottom' attribute value (distance from the bottom of the
            component to the bottom edge of the layout). Currently active units
            are maintained.

            @param bottomValue
                       The value of the 'bottom' attribute
            @see #setBottomUnits(int)
            """
            self._bottomValue = bottomValue
            self.requestRepaint()

        def getLeftValue(self):
            """Gets the 'left' attributes value using current units.

            @return The value of the 'left' attribute, null if not set
            @see #getLeftUnits()
            """
            return self._leftValue

        def setLeftValue(self, leftValue):
            """Sets the 'left' attribute value (distance from the left of the
            component to the left edge of the layout). Currently active units are
            maintained.

            @param leftValue
                       The value of the 'left' CSS-attribute
            @see #setLeftUnits(int)
            """
            self._leftValue = leftValue
            self.requestRepaint()

        def getTopUnits(self):
            """Gets the unit for the 'top' attribute

            @return See {@link Sizeable} UNIT_SYMBOLS for a description of the
                    available units.
            """
            return self._topUnits

        def setTopUnits(self, topUnits):
            """Sets the unit for the 'top' attribute

            @param topUnits
                       See {@link Sizeable} UNIT_SYMBOLS for a description of the
                       available units.
            """
            self._topUnits = topUnits
            self.requestRepaint()

        def getRightUnits(self):
            """Gets the unit for the 'right' attribute

            @return See {@link Sizeable} UNIT_SYMBOLS for a description of the
                    available units.
            """
            return self._rightUnits

        def setRightUnits(self, rightUnits):
            """Sets the unit for the 'right' attribute

            @param rightUnits
                       See {@link Sizeable} UNIT_SYMBOLS for a description of the
                       available units.
            """
            self._rightUnits = rightUnits
            self.requestRepaint()

        def getBottomUnits(self):
            """Gets the unit for the 'bottom' attribute

            @return See {@link Sizeable} UNIT_SYMBOLS for a description of the
                    available units.
            """
            return self._bottomUnits

        def setBottomUnits(self, bottomUnits):
            """Sets the unit for the 'bottom' attribute

            @param bottomUnits
                       See {@link Sizeable} UNIT_SYMBOLS for a description of the
                       available units.
            """
            self._bottomUnits = bottomUnits
            self.requestRepaint()

        def getLeftUnits(self):
            """Gets the unit for the 'left' attribute

            @return See {@link Sizeable} UNIT_SYMBOLS for a description of the
                    available units.
            """
            return self._leftUnits

        def setLeftUnits(self, leftUnits):
            """Sets the unit for the 'left' attribute

            @param leftUnits
                       See {@link Sizeable} UNIT_SYMBOLS for a description of the
                       available units.
            """
            self._leftUnits = leftUnits
            self.requestRepaint()

        def getZIndex(self):
            """Gets the 'z-index' attribute.

            @return the zIndex The z-index attribute
            """
            # (non-Javadoc)
            # 
            # @see java.lang.Object#toString()

            return self._zIndex

        def toString(self):
            return self.getCSSString()

    def paintContent(self, target):
        super(AbsoluteLayout, self).paintContent(target)
        for component in self._components:
            target.startTag('cc')
            target.addAttribute('css', self.getPosition(component).getCSSString())
            component.paint(target)
            target.endTag('cc')

    def addListener(self, listener):
        self.addListener(self._CLICK_EVENT, LayoutClickEvent, listener, LayoutClickListener.clickMethod)

    def removeListener(self, listener):
        self.removeListener(self._CLICK_EVENT, LayoutClickEvent, listener)
