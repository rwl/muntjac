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

"""Defines a layout implementation that mimics html absolute positioning."""

import re

from muntjac.ui.abstract_layout import AbstractLayout
from muntjac.terminal.gwt.client.event_id import EventId
from muntjac.terminal.sizeable import ISizeable

from muntjac.event.layout_events import \
    LayoutClickEvent, ILayoutClickListener, ILayoutClickNotifier


class AbsoluteLayout(AbstractLayout, ILayoutClickNotifier):
    """AbsoluteLayout is a layout implementation that mimics html
    absolute positioning.
    """

    CLIENT_WIDGET = None #ClientWidget(VAbsoluteLayout)

    _CLICK_EVENT = EventId.LAYOUT_CLICK

    def __init__(self):
        """Creates an AbsoluteLayout with full size."""
        super(AbsoluteLayout, self).__init__()

        #: The components in the layout
        self._components = set()

        #: Maps each component to a position
        self._componentToCoordinates = dict()

        self.setSizeFull()


    def getComponentIterator(self):
        """Gets an iterator for going through all components enclosed
        in the absolute layout.
        """
        return iter(self._components)


    def getComponentCount(self):
        """Gets the number of contained components. Consistent with
        the iterator returned by L{getComponentIterator}.

        @return: the number of contained components
        """
        return len(self._components)


    def replaceComponent(self, oldComponent, newComponent):
        """Replaces one component with another one. The new component
        inherits the old components position.
        """
        position = self.getPosition(oldComponent)
        self.removeComponent(oldComponent)
        self.addComponent(newComponent)
        self._componentToCoordinates[newComponent] = position


    def addComponent(self, c, cssPosition=None):
        """Adds a component to the layout. The component can be positioned
        by providing a string formatted in CSS-format.

        For example the string "top:10px;left:10px" will position the
        component 10 pixels from the left and 10 pixels from the top. The
        identifiers: "top","left","right" and "bottom" can be used to
        specify the position.

        @param c:
                   The component to add to the layout
        @param cssPosition:
                   The css position string
        """
        # Create position instance and add it to componentToCoordinates
        # map. We need to do this before we call addComponent so the
        # attachListeners can access this position. #6368
        if cssPosition is not None:
            position = ComponentPosition(self)
            position.setCSSString(cssPosition)
            self._componentToCoordinates[c] = position

        self._components.add(c)
        try:
            super(AbsoluteLayout, self).addComponent(c)
            self.requestRepaint()
        except ValueError, e:
            self._components.remove(c)
            if cssPosition is not None:
                # Remove component coordinates if adding fails
                del self._componentToCoordinates[c]
                raise e


    def removeComponent(self, c):
        if c in self._components:
            self._components.remove(c)
        if c in self._componentToCoordinates:
            del self._componentToCoordinates[c]
        super(AbsoluteLayout, self).removeComponent(c)
        self.requestRepaint()


    def getPosition(self, component):
        """Gets the position of a component in the layout. Returns C{None}
        if component is not attached to the layout.

        @param component:
                   The component which position is needed
        @return: An instance of ComponentPosition containing the position
                of the component, or null if the component is not enclosed
                in the layout.
        """
        if component.getParent() != self:
            return None
        elif component in self._componentToCoordinates:
            return self._componentToCoordinates.get(component)
        else:
            coords = ComponentPosition(self)
            self._componentToCoordinates[component] = coords
            return coords


    def paintContent(self, target):
        super(AbsoluteLayout, self).paintContent(target)
        for component in self._components:
            target.startTag('cc')
            css = self.getPosition(component).getCSSString()
            target.addAttribute('css', css)
            component.paint(target)
            target.endTag('cc')


    def addListener(self, listener, iface=None):
        if (isinstance(listener, ILayoutClickListener) and
                (iface is None or issubclass(iface, ILayoutClickListener))):
            self.registerListener(self._CLICK_EVENT, LayoutClickEvent,
                    listener, ILayoutClickListener.clickMethod)

        super(AbsoluteLayout, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, LayoutClickEvent):
            self.registerCallback(LayoutClickEvent, callback,
                    self._CLICK_EVENT, *args)
        else:
            super(AbsoluteLayout, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        if (isinstance(listener, ILayoutClickListener) and
                (iface is None or issubclass(iface, ILayoutClickListener))):
            self.withdrawListener(self._CLICK_EVENT, LayoutClickEvent,
                    listener)

        super(AbsoluteLayout, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, LayoutClickEvent):
            self.withdrawCallback(LayoutClickEvent, callback,
                    self._CLICK_EVENT)
        else:
            super(AbsoluteLayout, self).removeCallback(callback, eventType)


class ComponentPosition(object):
    """The CompontPosition class represents a components position within
    the absolute layout. It contains the attributes for left, right, top
    and bottom and the units used to specify them.
    """

    def __init__(self, layout):
        self._zIndex = -1
        self._topValue = None
        self._rightValue = None
        self._bottomValue = None
        self._leftValue = None

        self._topUnits = 0
        self._rightUnits = 0
        self._bottomUnits = 0
        self._leftUnits = 0

        self._layout = layout


    def setCSSString(self, css):
        """Sets the position attributes using CSS syntax. Attributes not
        included in the string are reset to their unset states.

        C{setCSSString("top:10px;left:20%;z-index:16;")}
        """
        self._topValue = self._bottomValue = None
        self._rightValue = self._leftValue = None
        self._topUnits = self._bottomUnits = 0
        self._rightUnits = self._leftUnits = 0
        self._zIndex = -1

        if css is None:
            return

        cssProperties = css.split(';')
        for i in range(len(cssProperties)):
            keyValuePair = cssProperties[i].split(':')
            key = keyValuePair[0].strip()
            if key == '':
                continue

            if key == 'z-index':
                self._zIndex = int( keyValuePair[1].strip() )
            else:
                if len(keyValuePair) > 1:
                    value = keyValuePair[1].strip()
                else:
                    value = ''

                unit = re.sub('[0-9\\.\\-]+', '', value)
                if not (unit == ''):
                    value = value[:value.find(unit)].strip()

                v = float(value)
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

        self._layout.requestRepaint()


    def parseCssUnit(self, string):
        """Parses a string and checks if a unit is found. If a unit
        is not found from the string the unit pixels is used.

        @param string:
                   The string to parse the unit from
        @return: The found unit
        """
        for i in range(len(ISizeable.UNIT_SYMBOLS)):
            if ISizeable.UNIT_SYMBOLS[i] == string:
                return i
        return 0  # defaults to px (eg. top:0;)


    def getCSSString(self):
        """Converts the internal values into a valid CSS string.

        @return: A valid CSS string
        """
        s = ''
        if self._topValue is not None:
            symbol = ISizeable.UNIT_SYMBOLS[self._topUnits]
            s += 'top:' + str(self._topValue) + symbol + ';'

        if self._rightValue is not None:
            symbol = ISizeable.UNIT_SYMBOLS[self._rightUnits]
            s += 'right:' + str(self._rightValue) + symbol + ';'

        if self._bottomValue is not None:
            symbol = ISizeable.UNIT_SYMBOLS[self._bottomUnits]
            s += 'bottom:' + str(self._bottomValue) + symbol + ';'

        if self._leftValue is not None:
            symbol = ISizeable.UNIT_SYMBOLS[self._leftUnits]
            s += 'left:' + str(self._leftValue) + symbol + ';'

        if self._zIndex >= 0:
            s += 'z-index:' + str(self._zIndex) + ';'

        return s


    def setTop(self, topValue, topUnits):
        """Sets the 'top' attribute; distance from the top of the
        component to the top edge of the layout.

        @param topValue:
                   The value of the 'top' attribute
        @param topUnits:
                   The unit of the 'top' attribute. See UNIT_SYMBOLS
                   for a description of the available units.
        """
        self._topValue = topValue
        self._topUnits = topUnits
        self._layout.requestRepaint()


    def setRight(self, rightValue, rightUnits):
        """Sets the 'right' attribute; distance from the right of the
        component to the right edge of the layout.

        @param rightValue:
                   The value of the 'right' attribute
        @param rightUnits:
                   The unit of the 'right' attribute. See UNIT_SYMBOLS
                   for a description of the available units.
        """
        self._rightValue = rightValue
        self._rightUnits = rightUnits
        self._layout.requestRepaint()


    def setBottom(self, bottomValue, bottomUnits):
        """Sets the 'bottom' attribute; distance from the bottom of the
        component to the bottom edge of the layout.

        @param bottomValue:
                   The value of the 'bottom' attribute
        @param bottomUnits:
                   The unit of the 'bottom' attribute. See UNIT_SYMBOLS
                   for a description of the available units.
        """
        self._bottomValue = bottomValue
        self._bottomUnits = bottomUnits
        self._layout.requestRepaint()


    def setLeft(self, leftValue, leftUnits):
        """Sets the 'left' attribute; distance from the left of the
        component to the left edge of the layout.

        @param leftValue:
                   The value of the 'left' attribute
        @param leftUnits:
                   The unit of the 'left' attribute. See UNIT_SYMBOLS
                   for a description of the available units.
        """
        self._leftValue = leftValue
        self._leftUnits = leftUnits
        self._layout.requestRepaint()


    def setZIndex(self, zIndex):
        """Sets the 'z-index' attribute; the visual stacking order

        @param zIndex:
                   The z-index for the component.
        """
        self._zIndex = zIndex
        self._layout.requestRepaint()


    def setTopValue(self, topValue):
        """Sets the value of the 'top' attribute; distance from the top
        of the component to the top edge of the layout.

        @param topValue:
                   The value of the 'left' attribute
        """
        self._topValue = topValue
        self._layout.requestRepaint()


    def getTopValue(self):
        """Gets the 'top' attributes value in current units.

        @see: L{getTopUnits}
        @return: The value of the 'top' attribute, null if not set
        """
        return self._topValue


    def getRightValue(self):
        """Gets the 'right' attributes value in current units.

        @return: The value of the 'right' attribute, null if not set
        @see: L{getRightUnits}
        """
        return self._rightValue


    def setRightValue(self, rightValue):
        """Sets the 'right' attribute value (distance from the right
        of the component to the right edge of the layout). Currently
        active units are maintained.

        @param rightValue:
                   The value of the 'right' attribute
        @see: L{setRightUnits}
        """
        self._rightValue = rightValue
        self._layout.requestRepaint()


    def getBottomValue(self):
        """Gets the 'bottom' attributes value using current units.

        @return: The value of the 'bottom' attribute, null if not set
        @see: L{getBottomUnits}
        """
        return self._bottomValue


    def setBottomValue(self, bottomValue):
        """Sets the 'bottom' attribute value (distance from the bottom
        of the component to the bottom edge of the layout). Currently
        active units are maintained.

        @param bottomValue:
                   The value of the 'bottom' attribute
        @see: L{setBottomUnits}
        """
        self._bottomValue = bottomValue
        self._layout.requestRepaint()


    def getLeftValue(self):
        """Gets the 'left' attributes value using current units.

        @return: The value of the 'left' attribute, null if not set
        @see: L{getLeftUnits}
        """
        return self._leftValue


    def setLeftValue(self, leftValue):
        """Sets the 'left' attribute value (distance from the left of
        the component to the left edge of the layout). Currently active
        units are maintained.

        @param leftValue:
                   The value of the 'left' CSS-attribute
        @see: L{setLeftUnits}
        """
        self._leftValue = leftValue
        self._layout.requestRepaint()


    def getTopUnits(self):
        """Gets the unit for the 'top' attribute

        @return: See L{ISizeable} UNIT_SYMBOLS for a description of
                the available units.
        """
        return self._topUnits


    def setTopUnits(self, topUnits):
        """Sets the unit for the 'top' attribute

        @param topUnits:
                   See L{ISizeable} UNIT_SYMBOLS for a description
                   of the available units.
        """
        self._topUnits = topUnits
        self._layout.requestRepaint()


    def getRightUnits(self):
        """Gets the unit for the 'right' attribute

        @return: See L{ISizeable} UNIT_SYMBOLS for a description of
                the available units.
        """
        return self._rightUnits


    def setRightUnits(self, rightUnits):
        """Sets the unit for the 'right' attribute

        @param rightUnits:
                   See L{ISizeable} UNIT_SYMBOLS for a description
                   of the available units.
        """
        self._rightUnits = rightUnits
        self._layout.requestRepaint()


    def getBottomUnits(self):
        """Gets the unit for the 'bottom' attribute

        @return: See L{ISizeable} UNIT_SYMBOLS for a description of
                the available units.
        """
        return self._bottomUnits


    def setBottomUnits(self, bottomUnits):
        """Sets the unit for the 'bottom' attribute

        @param bottomUnits:
                   See L{ISizeable} UNIT_SYMBOLS for a description
                   of the available units.
        """
        self._bottomUnits = bottomUnits
        self._layout.requestRepaint()


    def getLeftUnits(self):
        """Gets the unit for the 'left' attribute

        @return: See L{ISizeable} UNIT_SYMBOLS for a description
                of the available units.
        """
        return self._leftUnits


    def setLeftUnits(self, leftUnits):
        """Sets the unit for the 'left' attribute

        @param leftUnits:
                   See L{ISizeable} UNIT_SYMBOLS for a description
                   of the available units.
        """
        self._leftUnits = leftUnits
        self._layout.requestRepaint()


    def getZIndex(self):
        """Gets the 'z-index' attribute.

        @return: the zIndex The z-index attribute
        """
        return self._zIndex


    def toString(self):
        return self.getCSSString()
