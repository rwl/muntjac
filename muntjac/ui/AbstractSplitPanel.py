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
from com.vaadin.event.ComponentEventListener import (ComponentEventListener,)
from com.vaadin.ui.VerticalLayout import (VerticalLayout,)
from com.vaadin.ui.AbstractLayout import (AbstractLayout,)
from com.vaadin.tools.ReflectTools import (ReflectTools,)
from com.vaadin.terminal.gwt.client.ui.VSplitPanel import (VSplitPanel,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
from com.vaadin.ui.Button import (ClickEvent,)
# from com.vaadin.event.MouseEvents.ClickEvent import (ClickEvent,)
# from java.io.Serializable import (Serializable,)
# from java.lang.reflect.Method import (Method,)
# from java.util.Iterator import (Iterator,)
# from java.util.Map import (Map,)


class AbstractSplitPanel(AbstractLayout):
    """AbstractSplitPanel.

    <code>AbstractSplitPanel</code> is base class for a component container that
    can contain two components. The comopnents are split by a divider element.

    @author Vaadin Ltd.
    @version
    @VERSION@
    @since 6.5
    """
    _firstComponent = None
    _secondComponent = None
    _pos = 50
    _posUnit = UNITS_PERCENTAGE
    _posReversed = False
    _locked = False
    _SPLITTER_CLICK_EVENT = VSplitPanel.SPLITTER_CLICK_EVENT_IDENTIFIER

    class ComponentIterator(Iterator, Serializable):
        """Modifiable and Serializable Iterator for the components, used by
        {@link AbstractSplitPanel#getComponentIterator()}.
        """
        _i = 0

        def hasNext(self):
            if self._i < self.getComponentCount():
                return True
            return False

        def next(self):
            if not self.hasNext():
                return None
            self._i += 1
            if self._i == 1:
                return self.secondComponent if self.firstComponent is None else self.firstComponent
            elif self._i == 2:
                return self.secondComponent
            return None

        def remove(self):
            if self._i == 1:
                if self.firstComponent is not None:
                    self.setFirstComponent(None)
                    self._i = 0
                else:
                    self.setSecondComponent(None)
            elif self._i == 2:
                self.setSecondComponent(None)

    def addComponent(self, c):
        """Add a component into this container. The component is added to the right
        or under the previous component.

        @param c
                   the component to be added.
        """
        if self._firstComponent is None:
            self._firstComponent = c
        elif self._secondComponent is None:
            self._secondComponent = c
        else:
            raise self.UnsupportedOperationException('Split panel can contain only two components')
        super(AbstractSplitPanel, self).addComponent(c)
        self.requestRepaint()

    def setFirstComponent(self, c):
        if self._firstComponent == c:
            # Nothing to do
            return
        if self._firstComponent is not None:
            # detach old
            self.removeComponent(self._firstComponent)
        self._firstComponent = c
        super(AbstractSplitPanel, self).addComponent(c)
        self.requestRepaint()

    def setSecondComponent(self, c):
        if c == self._secondComponent:
            # Nothing to do
            return
        if self._secondComponent is not None:
            # detach old
            self.removeComponent(self._secondComponent)
        self._secondComponent = c
        super(AbstractSplitPanel, self).addComponent(c)
        self.requestRepaint()

    def getFirstComponent(self):
        """@return the first component of this SplitPanel."""
        return self._firstComponent

    def getSecondComponent(self):
        """@return the second component of this SplitPanel."""
        return self._secondComponent

    def removeComponent(self, c):
        """Removes the component from this container.

        @param c
                   the component to be removed.
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.ComponentContainer#getComponentIterator()

        super(AbstractSplitPanel, self).removeComponent(c)
        if c == self._firstComponent:
            self._firstComponent = None
        elif c == self._secondComponent:
            self._secondComponent = None
        self.requestRepaint()

    def getComponentIterator(self):
        return self.ComponentIterator()

    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the iterator
        returned by {@link #getComponentIterator()}.

        @return the number of contained components (zero, one or two)
        """
        count = 0
        if self._firstComponent is not None:
            count += 1
        if self._secondComponent is not None:
            count += 1
        return count

    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   the Paint Event.
        @throws PaintException
                    if the paint operation failed.
        """
        # Documented in superclass
        super(AbstractSplitPanel, self).paintContent(target)
        position = self._pos + self.UNIT_SYMBOLS[self._posUnit]
        target.addAttribute('position', position)
        if self.isLocked():
            target.addAttribute('locked', True)
        target.addAttribute('reversed', self._posReversed)
        if self._firstComponent is not None:
            self._firstComponent.paint(target)
        else:
            temporaryComponent = VerticalLayout()
            temporaryComponent.setParent(self)
            temporaryComponent.paint(target)
        if self._secondComponent is not None:
            self._secondComponent.paint(target)
        else:
            temporaryComponent = VerticalLayout()
            temporaryComponent.setParent(self)
            temporaryComponent.paint(target)

    def replaceComponent(self, oldComponent, newComponent):
        if oldComponent == self._firstComponent:
            self.setFirstComponent(newComponent)
        elif oldComponent == self._secondComponent:
            self.setSecondComponent(newComponent)
        self.requestRepaint()

    def setSplitPosition(self, *args):
        """Moves the position of the splitter.

        @param pos
                   the new size of the first region in the unit that was last
                   used (default is percentage)
        ---
        Moves the position of the splitter.

        @param pos
                   the new size of the region in the unit that was last used
                   (default is percentage)
        @param reverse
                   if set to true the split splitter position is measured by the
                   second region else it is measured by the first region
        ---
        Moves the position of the splitter with given position and unit.

        @param pos
                   size of the first region
        @param unit
                   the unit (from {@link Sizeable}) in which the size is given.
        ---
        Moves the position of the splitter with given position and unit.

        @param pos
                   size of the first region
        @param unit
                   the unit (from {@link Sizeable}) in which the size is given.
        @param reverse
                   if set to true the split splitter position is measured by the
                   second region else it is measured by the first region
        ---
        Moves the position of the splitter.

        @param pos
                   the new size of the first region
        @param unit
                   the unit (from {@link Sizeable}) in which the size is given.
        @param repaintNotNeeded
                   true if client side needs to be updated. Use false if the
                   position info has come from the client side, thus it already
                   knows the position.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            pos, = _0
            self.setSplitPosition(pos, self._posUnit, True, False)
        elif _1 == 2:
            if isinstance(_0[1], boolean):
                pos, reverse = _0
                self.setSplitPosition(pos, self._posUnit, True, reverse)
            else:
                pos, unit = _0
                self.setSplitPosition(pos, unit, True, False)
        elif _1 == 3:
            pos, unit, reverse = _0
            self.setSplitPosition(pos, unit, True, reverse)
        elif _1 == 4:
            pos, unit, repaintNeeded, reverse = _0
            if unit != self.UNITS_PERCENTAGE and unit != self.UNITS_PIXELS:
                raise self.IllegalArgumentException('Only percentage and pixel units are allowed')
            self._pos = pos
            self._posUnit = unit
            self._posReversed = reverse
            if repaintNeeded:
                self.requestRepaint()
        else:
            raise ARGERROR(1, 4)

    def getSplitPosition(self):
        """Returns the current position of the splitter, in
        {@link #getSplitPositionUnit()} units.

        @return position of the splitter
        """
        return self._pos

    def getSplitPositionUnit(self):
        """Returns the unit of position of the splitter

        @return unit of position of the splitter
        """
        return self._posUnit

    def setLocked(self, locked):
        """Lock the SplitPanels position, disabling the user from dragging the split
        handle.

        @param locked
                   Set <code>true</code> if locked, <code>false</code> otherwise.
        """
        self._locked = locked
        self.requestRepaint()

    def isLocked(self):
        """Is the SplitPanel handle locked (user not allowed to change split
        position by dragging).

        @return <code>true</code> if locked, <code>false</code> otherwise.
        """
        # Invoked when a variable of the component changes. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        return self._locked

    def changeVariables(self, source, variables):
        super(AbstractSplitPanel, self).changeVariables(source, variables)
        if 'position' in variables and not self.isLocked():
            newPos = variables['position']
            self.setSplitPosition(newPos, self._posUnit, self._posReversed)
        if self._SPLITTER_CLICK_EVENT in variables:
            self.fireClick(variables[self._SPLITTER_CLICK_EVENT])

    def fireClick(self, parameters):
        mouseDetails = MouseEventDetails.deSerialize(parameters['mouseDetails'])
        self.fireEvent(self.SplitterClickEvent(self, mouseDetails))

    class SplitterClickListener(ComponentEventListener):
        """<code>SplitterClickListener</code> interface for listening for
        <code>SplitterClickEvent</code> fired by a <code>SplitPanel</code>.

        @see SplitterClickEvent
        @since 6.2
        """
        clickMethod = ReflectTools.findMethod(self.SplitterClickListener, 'splitterClick', self.SplitterClickEvent)

        def splitterClick(self, event):
            """SplitPanel splitter has been clicked

            @param event
                       SplitterClickEvent event.
            """
            pass

    class SplitterClickEvent(ClickEvent):

        def __init__(self, source, mouseEventDetails):
            super(SplitterClickEvent, self)(source, mouseEventDetails)

    def addListener(self, listener):
        self.addListener(self._SPLITTER_CLICK_EVENT, self.SplitterClickEvent, listener, self.SplitterClickListener.clickMethod)

    def removeListener(self, listener):
        self.removeListener(self._SPLITTER_CLICK_EVENT, self.SplitterClickEvent, listener)
