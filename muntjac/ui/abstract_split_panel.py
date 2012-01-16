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

"""Defines a base class for a component container that can contain two
components."""

from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.ui.abstract_layout import AbstractLayout
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails
from muntjac.event.mouse_events import ClickEvent as MouseClickEvent
from muntjac.event.component_event_listener import IComponentEventListener

from muntjac.terminal.gwt.client.ui.v_split_panel import VSplitPanel
from muntjac.ui.abstract_component import AbstractComponent


class ComponentIterator(object):
    """Modifiable and serializable iterator for the components, used by
    L{AbstractSplitPanel.getComponentIterator}.
    """

    def __init__(self, sp):
        self.sp = sp
        self._i = 0


    def __iter__(self):
        return self


    def hasNext(self):
        if self._i < self.sp.getComponentCount():
            return True
        return False


    def next(self):  #@PydevCodeAnalysisIgnore
        if not self.hasNext():
            raise StopIteration

        self._i += 1

        if self._i == 1:
            if self.sp._firstComponent is None:
                return self.sp._secondComponent
            else:
                return self.sp._firstComponent
        elif self._i == 2:
            return self.sp._secondComponent

        return None


    def remove(self):
        if self._i == 1:
            if self.sp._firstComponent is not None:
                self.sp.setFirstComponent(None)
                self._i = 0
            else:
                self.sp.setSecondComponent(None)
        elif self._i == 2:
            self.sp.setSecondComponent(None)


class AbstractSplitPanel(AbstractLayout):
    """C{AbstractSplitPanel} is base class for a component container that can
    contain two components. The comopnents are split by a divider element.

    @author: Vaadin Ltd.
    @version: 1.1.0
    """

    _SPLITTER_CLICK_EVENT = VSplitPanel.SPLITTER_CLICK_EVENT_IDENTIFIER

    def __init__(self):
        super(AbstractSplitPanel, self).__init__()

        self._firstComponent = None
        self._secondComponent = None
        self._pos = 50
        self._posUnit = self.UNITS_PERCENTAGE
        self._posReversed = False
        self._locked = False


    def addComponent(self, c):
        """Add a component into this container. The component is added to
        the right or under the previous component.

        @param c:
                   the component to be added.
        """
        if self._firstComponent is None:
            self._firstComponent = c
        elif self._secondComponent is None:
            self._secondComponent = c
        else:
            raise NotImplementedError, \
                    'Split panel can contain only two components'

        super(AbstractSplitPanel, self).addComponent(c)
        self.requestRepaint()


    def setFirstComponent(self, c):
        if self._firstComponent == c:
            return  # Nothing to do

        if self._firstComponent is not None:
            self.removeComponent(self._firstComponent)  # detach old

        self._firstComponent = c
        super(AbstractSplitPanel, self).addComponent(c)
        self.requestRepaint()


    def setSecondComponent(self, c):
        if c == self._secondComponent:
            return  # Nothing to do

        if self._secondComponent is not None:
            self.removeComponent(self._secondComponent)  # detach old

        self._secondComponent = c
        super(AbstractSplitPanel, self).addComponent(c)
        self.requestRepaint()


    def getFirstComponent(self):
        """@return: the first component of this SplitPanel."""
        return self._firstComponent


    def getSecondComponent(self):
        """@return: the second component of this SplitPanel."""
        return self._secondComponent


    def removeComponent(self, c):
        """Removes the component from this container.

        @param c: the component to be removed.
        """
        super(AbstractSplitPanel, self).removeComponent(c)

        if c == self._firstComponent:
            self._firstComponent = None
        elif c == self._secondComponent:
            self._secondComponent = None

        self.requestRepaint()


    def getComponentIterator(self):
        return ComponentIterator(self)


    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the
        iterator returned by L{getComponentIterator}.

        @return: the number of contained components (zero, one or two)
        """
        count = 0
        if self._firstComponent is not None:
            count += 1

        if self._secondComponent is not None:
            count += 1

        return count


    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the Paint Event.
        @raise PaintException:
                    if the paint operation failed.
        """
        super(AbstractSplitPanel, self).paintContent(target)

        position = str(self._pos) + self.UNIT_SYMBOLS[self._posUnit]

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

        @param args: tuple of the form
            - (pos)
              1. the new size of the region in the unit that was last
                 used (default is percentage)
            - (pos, reverse)
              1. size of the first region
              2. if set to true the split splitter position is measured by
                 the second region else it is measured by the first region
            - (pos, unit, reverse)
              1. size of the first region
              2. the unit (from L{Sizeable}) in which the size is given.
              3. if set to true the split splitter position is measured by
                 the second region else it is measured by the first region
            - (pos, unit, repaintNotNeeded)
              1. size of the first region
              2. the unit (from L{Sizeable}) in which the size is given.
              3. true if client side needs to be updated. Use false if
                 the position info has come from the client side, thus it
                 already knows the position.
        """
        nargs = len(args)
        if nargs == 1:
            pos, = args
            self.setSplitPosition(pos, self._posUnit, True, False)
        elif nargs == 2:
            if isinstance(args[1], bool):
                pos, reverse = args
                self.setSplitPosition(pos, self._posUnit, True, reverse)
            else:
                pos, unit = args
                self.setSplitPosition(pos, unit, True, False)
        elif nargs == 3:
            pos, unit, reverse = args
            self.setSplitPosition(pos, unit, True, reverse)
        elif nargs == 4:
            pos, unit, repaintNeeded, reverse = args
            if unit != self.UNITS_PERCENTAGE and unit != self.UNITS_PIXELS:
                raise ValueError, \
                        'Only percentage and pixel units are allowed'
            self._pos = pos
            self._posUnit = unit
            self._posReversed = reverse
            if repaintNeeded:
                self.requestRepaint()
        else:
            raise ValueError, 'too many arguments'


    def getSplitPosition(self):
        """Returns the current position of the splitter, in
        L{getSplitPositionUnit} units.

        @return: position of the splitter
        """
        return self._pos


    def getSplitPositionUnit(self):
        """Returns the unit of position of the splitter

        @return: unit of position of the splitter
        """
        return self._posUnit


    def setLocked(self, locked):
        """Lock the SplitPanels position, disabling the user from dragging
        the split handle.

        @param locked:
                   Set C{True} if locked, C{False} otherwise.
        """
        self._locked = locked
        self.requestRepaint()


    def isLocked(self):
        """Is the SplitPanel handle locked (user not allowed to change
        split position by dragging).

        @return: C{True} if locked, C{False} otherwise.
        """
        return self._locked


    def changeVariables(self, source, variables):
        # Invoked when a variable of the component changes.
        super(AbstractSplitPanel, self).changeVariables(source, variables)

        if 'position' in variables and not self.isLocked():
            newPos = variables.get('position')
            self.setSplitPosition(newPos, self._posUnit, self._posReversed)

        if self._SPLITTER_CLICK_EVENT in variables:
            self.fireClick(variables.get(self._SPLITTER_CLICK_EVENT))


    def fireClick(self, parameters):
        mouseDetails = \
                MouseEventDetails.deSerialize(parameters.get('mouseDetails'))
        self.fireEvent( SplitterClickEvent(self, mouseDetails) )


    def addListener(self, listener, iface=None):
        if (isinstance(listener, ISplitterClickListener) and
            (iface is None or issubclass(iface, ISplitterClickListener))):
            self.registerListener(self._SPLITTER_CLICK_EVENT,
                    SplitterClickEvent, listener,
                    ISplitterClickListener.clickMethod)

        super(AbstractSplitPanel, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, SplitterClickEvent):
            self.registerCallback(SplitterClickEvent, callback, None, *args)

        else:
            super(AbstractSplitPanel, self).addCallback(callback, eventType,
                    *args)


    def removeListener(self, listener, iface=None):
        if (isinstance(listener, ISplitterClickListener) and
                (iface is None or issubclass(iface, ISplitterClickListener))):
            self.withdrawListener(self._SPLITTER_CLICK_EVENT,
                    SplitterClickEvent, listener)

        super(AbstractSplitPanel, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, SplitterClickEvent):
            self.withdrawCallback(SplitterClickEvent, callback,
                    self._SPLITTER_CLICK_EVENT)

        else:
            super(AbstractSplitPanel, self).removeCallback(callback, eventType)


class ISplitterClickListener(IComponentEventListener):
    """C{ISplitterClickListener} interface for listening for
    C{SplitterClickEvent} fired by a C{SplitPanel}.

    @see: SplitterClickEvent
    """

    def splitterClick(self, event):
        """SplitPanel splitter has been clicked

        @param event:
                   SplitterClickEvent event.
        """
        raise NotImplementedError

    clickMethod = splitterClick


class SplitterClickEvent(MouseClickEvent):

    def __init__(self, source, mouseEventDetails):
        super(SplitterClickEvent, self).__init__(source, mouseEventDetails)
