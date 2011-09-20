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

from com.vaadin.ui.Component import Component
from com.vaadin.ui.OrderedLayout import OrderedLayout
from com.vaadin.terminal.Sizeable import Sizeable
from com.vaadin.ui.CustomComponent import CustomComponent
# from com.vaadin.ui.GridLayout.Area import (Area,)
# from java.io.PrintStream import (PrintStream,)
# from java.io.PrintWriter import (PrintWriter,)
# from java.io.Serializable import (Serializable,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.List import (List,)
# from java.util.Map import (Map,)
# from java.util.Stack import (Stack,)
# from java.util.Vector import (Vector,)
# from java.util.logging.Level import (Level,)
# from java.util.logging.Logger import (Logger,)


class ComponentSizeValidator(Serializable):
    _logger = Logger.getLogger(ComponentSizeValidator.getName())
    _LAYERS_SHOWN = 4

    @classmethod
    def validateComponentRelativeSizes(cls, component, errors, parent):
        """Recursively checks given component and its subtree for invalid layout
        setups. Prints errors to std err stream.

        @param component
                   component to check
        @return set of first level errors found
        """
        invalidHeight = not cls.checkHeights(component)
        invalidWidth = not cls.checkWidths(component)
        if invalidHeight or invalidWidth:
            error = cls.InvalidLayout(component, invalidHeight, invalidWidth)
            if parent is not None:
                parent.addError(error)
            else:
                if errors is None:
                    errors = LinkedList()
                errors.add(error)
            parent = error
        if isinstance(component, Panel):
            panel = component
            errors = cls.validateComponentRelativeSizes(panel.getContent(), errors, parent)
        elif isinstance(component, ComponentContainer):
            lo = component
            it = lo.getComponentIterator()
            while it.hasNext():
                errors = cls.validateComponentRelativeSizes(it.next(), errors, parent)
        elif isinstance(component, Form):
            form = component
            if form.getLayout() is not None:
                errors = cls.validateComponentRelativeSizes(form.getLayout(), errors, parent)
            if form.getFooter() is not None:
                errors = cls.validateComponentRelativeSizes(form.getFooter(), errors, parent)
        return errors

    @classmethod
    def printServerError(cls, msg, attributes, widthError, errorStream):
        err = str()
        err.__add__('Vaadin DEBUG\n')
        indent = cls.StringBuilder('')
        if attributes is not None:
            while len(attributes) > cls._LAYERS_SHOWN:
                attributes.pop()
            while not attributes.empty():
                ci = attributes.pop()
                cls.showComponent(ci.component, ci.info, err, indent, widthError)
        err.__add__('Layout problem detected: ')
        err.__add__(msg)
        err.__add__('\n')
        err.__add__('Relative sizes were replaced by undefined sizes, components may not render as expected.\n')
        print err

    @classmethod
    def checkHeights(cls, component):
        try:
            if not cls.hasRelativeHeight(component):
                return True
            if isinstance(component, Window):
                return True
            if component.getParent() is None:
                return True
            return cls.parentCanDefineHeight(component)
        except Exception, e:
            cls._logger.log(Level.FINER, 'An exception occurred while validating sizes.', e)
            return True

    @classmethod
    def checkWidths(cls, component):
        try:
            if not cls.hasRelativeWidth(component):
                return True
            if isinstance(component, Window):
                return True
            if component.getParent() is None:
                return True
            return cls.parentCanDefineWidth(component)
        except Exception, e:
            cls._logger.log(Level.FINER, 'An exception occurred while validating sizes.', e)
            return True

    @classmethod
    def getHeightAttributes(cls, component):
        attributes = Stack()
        attributes.add(cls.ComponentInfo(component, cls.getHeightString(component)))
        parent = component.getParent()
        attributes.add(cls.ComponentInfo(parent, cls.getHeightString(parent)))
        while parent = parent.getParent() is not None:
            attributes.add(cls.ComponentInfo(parent, cls.getHeightString(parent)))
        return attributes

    @classmethod
    def getWidthAttributes(cls, component):
        attributes = Stack()
        attributes.add(cls.ComponentInfo(component, cls.getWidthString(component)))
        parent = component.getParent()
        attributes.add(cls.ComponentInfo(parent, cls.getWidthString(parent)))
        while parent = parent.getParent() is not None:
            attributes.add(cls.ComponentInfo(parent, cls.getWidthString(parent)))
        return attributes

    @classmethod
    def getWidthString(cls, component):
        width = 'width: '
        if cls.hasRelativeWidth(component):
            width += 'RELATIVE, ' + component.getWidth() + ' %'
        elif isinstance(component, Window) and component.getParent() is None:
            width += 'MAIN WINDOW'
        elif component.getWidth() >= 0:
            width += 'ABSOLUTE, ' + component.getWidth() + ' ' + Sizeable.UNIT_SYMBOLS[component.getWidthUnits()]
        else:
            width += 'UNDEFINED'
        return width

    @classmethod
    def getHeightString(cls, component):
        height = 'height: '
        if cls.hasRelativeHeight(component):
            height += 'RELATIVE, ' + component.getHeight() + ' %'
        elif isinstance(component, Window) and component.getParent() is None:
            height += 'MAIN WINDOW'
        elif component.getHeight() > 0:
            height += 'ABSOLUTE, ' + component.getHeight() + ' ' + Sizeable.UNIT_SYMBOLS[component.getHeightUnits()]
        else:
            height += 'UNDEFINED'
        return height

    @classmethod
    def showComponent(cls, component, attribute, err, indent, widthError):
        createLoc = cls._creationLocations[component]
        if widthError:
            sizeLoc = cls._widthLocations[component]
        else:
            sizeLoc = cls._heightLocations[component]
        err.__add__(indent)
        indent.append('  ')
        err.__add__('- ')
        err.__add__(component.getClass().getSimpleName())
        err.__add__('/').append(Integer.toHexString.toHexString(component.hashCode()))
        if component.getCaption() is not None:
            err.__add__(' \"')
            err.__add__(component.getCaption())
            err.__add__('\"')
        if component.getDebugId() is not None:
            err.__add__(' debugId: ')
            err.__add__(component.getDebugId())
        if createLoc is not None:
            err.__add__(', created at (' + createLoc.file + ':' + createLoc.lineNumber + ')')
        if attribute is not None:
            err.__add__(' (')
            err.__add__(attribute)
            if sizeLoc is not None:
                err.__add__(', set at (' + sizeLoc.file + ':' + sizeLoc.lineNumber + ')')
            err.__add__(')')
        err.__add__('\n')

    @classmethod
    def hasNonRelativeHeightComponent(cls, ol):
        it = ol.getComponentIterator()
        while it.hasNext():
            if not cls.hasRelativeHeight(it.next()):
                return True
        return False

    @classmethod
    def parentCanDefineHeight(cls, component):
        parent = component.getParent()
        if parent is None:
            # main window, valid situation
            return True
        if parent.getHeight() < 0:
            # Undefined height
            if isinstance(parent, Window):
                w = parent
                if w.getParent() is None:
                    # main window is considered to have size
                    return True
            if isinstance(parent, AbstractOrderedLayout):
                horizontal = True
                if isinstance(parent, OrderedLayout):
                    horizontal = parent.getOrientation() == OrderedLayout.ORIENTATION_HORIZONTAL
                elif isinstance(parent, VerticalLayout):
                    horizontal = False
                if horizontal and cls.hasNonRelativeHeightComponent(parent):
                    return True
                else:
                    return False
            elif isinstance(parent, GridLayout):
                gl = parent
                componentArea = gl.getComponentArea(component)
                rowHasHeight = False
                _0 = True
                row = componentArea.getRow1()
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        row += 1
                    if not (not rowHasHeight and row <= componentArea.getRow2()):
                        break
                    _1 = True
                    column = 0
                    while True:
                        if _1 is True:
                            _1 = False
                        else:
                            column += 1
                        if not (not rowHasHeight and column < gl.getColumns()):
                            break
                        c = gl.getComponent(column, row)
                        if c is not None:
                            rowHasHeight = not cls.hasRelativeHeight(c)
                if not rowHasHeight:
                    return False
                else:
                    # Other components define row height
                    return True
            if (
                ((isinstance(parent, Panel) or isinstance(parent, SplitPanel)) or isinstance(parent, TabSheet)) or isinstance(parent, CustomComponent)
            ):
                # height undefined, we know how how component works and no
                # exceptions
                # TODO horiz SplitPanel ??
                return False
            else:
                # We cannot generally know if undefined component can serve
                # space for children (like CustomLayout or component built by
                # third party) so we assume they can
                return True
        elif cls.hasRelativeHeight(parent):
            # Relative height
            if parent.getParent() is not None:
                return cls.parentCanDefineHeight(parent)
            else:
                return True
        else:
            # Absolute height
            return True

    @classmethod
    def hasRelativeHeight(cls, component):
        return component.getHeightUnits() == Sizeable.UNITS_PERCENTAGE and component.getHeight() > 0

    @classmethod
    def hasNonRelativeWidthComponent(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], AbstractOrderedLayout):
                ol, = _0
                it = ol.getComponentIterator()
                while it.hasNext():
                    if not cls.hasRelativeWidth(it.next()):
                        return True
                return False
            else:
                form, = _0
                layout = form.getLayout()
                footer = form.getFooter()
                if layout is not None and not cls.hasRelativeWidth(layout):
                    return True
                if footer is not None and not cls.hasRelativeWidth(footer):
                    return True
                return False
        else:
            raise ARGERROR(1, 1)

    @classmethod
    def hasRelativeWidth(cls, paintable):
        return paintable.getWidth() > 0 and paintable.getWidthUnits() == Sizeable.UNITS_PERCENTAGE

    @classmethod
    def parentCanDefineWidth(cls, component):
        parent = component.getParent()
        if parent is None:
            # main window, valid situation
            return True
        if isinstance(parent, Window):
            w = parent
            if w.getParent() is None:
                # main window is considered to have size
                return True
        if parent.getWidth() < 0:
            # Undefined width
            if isinstance(parent, AbstractOrderedLayout):
                ol = parent
                horizontal = True
                if isinstance(ol, OrderedLayout):
                    if ol.getOrientation() == OrderedLayout.ORIENTATION_VERTICAL:
                        horizontal = False
                elif isinstance(ol, VerticalLayout):
                    horizontal = False
                if not horizontal and cls.hasNonRelativeWidthComponent(ol):
                    # valid situation, other components defined width
                    return True
                else:
                    return False
            elif isinstance(parent, GridLayout):
                gl = parent
                componentArea = gl.getComponentArea(component)
                columnHasWidth = False
                _0 = True
                col = componentArea.getColumn1()
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        col += 1
                    if not (not columnHasWidth and col <= componentArea.getColumn2()):
                        break
                    _1 = True
                    row = 0
                    while True:
                        if _1 is True:
                            _1 = False
                        else:
                            row += 1
                        if not (not columnHasWidth and row < gl.getRows()):
                            break
                        c = gl.getComponent(col, row)
                        if c is not None:
                            columnHasWidth = not cls.hasRelativeWidth(c)
                if not columnHasWidth:
                    return False
                else:
                    # Other components define column width
                    return True
            elif isinstance(parent, Form):
                # If some other part of the form is not relative it determines
                # the component width

                return cls.hasNonRelativeWidthComponent(parent)
            elif (
                (isinstance(parent, SplitPanel) or isinstance(parent, TabSheet)) or isinstance(parent, CustomComponent)
            ):
                # FIXME Could we use com.vaadin package name here and
                # fail for all component containers?
                # FIXME Actually this should be moved to containers so it can
                # be implemented for custom containers
                # TODO vertical splitpanel with another non relative component?
                return False
            elif isinstance(parent, Window):
                # Sub window can define width based on caption
                if parent.getCaption() is not None and not (parent.getCaption() == ''):
                    return True
                else:
                    return False
            elif isinstance(parent, Panel):
                # TODO Panel should be able to define width based on caption
                return False
            else:
                return True
        elif cls.hasRelativeWidth(parent):
            # Relative width
            if parent.getParent() is None:
                return True
            return cls.parentCanDefineWidth(parent)
        else:
            return True

    _creationLocations = dict()
    _widthLocations = dict()
    _heightLocations = dict()

    class FileLocation(Serializable):
        method = None
        file = None
        className = None
        classNameSimple = None
        lineNumber = None

        def __init__(self, traceElement):
            self.file = traceElement.getFileName()
            self.className = traceElement.getClassName()
            self.classNameSimple = self.className[self.className.rfind('.') + 1:]
            self.lineNumber = traceElement.getLineNumber()
            self.method = traceElement.getMethodName()

    @classmethod
    def setCreationLocation(cls, object):
        cls.setLocation(cls._creationLocations, object)

    @classmethod
    def setWidthLocation(cls, object):
        cls.setLocation(cls._widthLocations, object)

    @classmethod
    def setHeightLocation(cls, object):
        cls.setLocation(cls._heightLocations, object)

    @classmethod
    def setLocation(cls, map, object):
        traceLines = cls.Thread.currentThread().getStackTrace()
        for traceElement in traceLines:
            # TODO Auto-generated catch block
            try:
                className = traceElement.getClassName()
                if className.startswith('java.') or className.startswith('sun.'):
                    continue
                cls = (lambda x: getattr(__import__(x.rsplit('.', 1)[0], fromlist=x.rsplit('.', 1)[0]), x.split('.')[-1]))(className)
                if (cls == ComponentSizeValidator) or (cls == cls.Thread):
                    continue
                if (
                    Component.isAssignableFrom(cls) and not CustomComponent.isAssignableFrom(cls)
                ):
                    continue
                cl = cls.FileLocation(traceElement)
                map.put(object, cl)
                return
            except Exception, e:
                cls._logger.log(Level.FINER, 'An exception occurred while validating sizes.', e)


    class InvalidLayout(Serializable):
        _component = None
        _invalidHeight = None
        _invalidWidth = None
        _subErrors = list()

        def __init__(self, component, height, width):
            self._component = component
            self._invalidHeight = height
            self._invalidWidth = width

        def addError(self, error):
            self._subErrors.add(error)

        def reportErrors(self, clientJSON, communicationManager, serverErrorStream):
            clientJSON.write('{')
            parent = self._component.getParent()
            paintableId = communicationManager.getPaintableId(self._component)
            clientJSON.print_('id:\"' + paintableId + '\"')
            if self._invalidHeight:
                attributes = None
                msg = ''
                # set proper error messages
                if isinstance(parent, AbstractOrderedLayout):
                    ol = parent
                    vertical = False
                    if isinstance(ol, OrderedLayout):
                        if ol.getOrientation() == OrderedLayout.ORIENTATION_VERTICAL:
                            vertical = True
                    elif isinstance(ol, VerticalLayout):
                        vertical = True
                    if vertical:
                        msg = 'Component with relative height inside a VerticalLayout with no height defined.'
                        attributes = self.getHeightAttributes(self._component)
                    else:
                        msg = 'At least one of a HorizontalLayout\'s components must have non relative height if the height of the layout is not defined'
                        attributes = self.getHeightAttributes(self._component)
                elif isinstance(parent, GridLayout):
                    msg = 'At least one of the GridLayout\'s components in each row should have non relative height if the height of the layout is not defined.'
                    attributes = self.getHeightAttributes(self._component)
                else:
                    # default error for non sized parent issue
                    msg = 'A component with relative height needs a parent with defined height.'
                    attributes = self.getHeightAttributes(self._component)
                self.printServerError(msg, attributes, False, serverErrorStream)
                clientJSON.print_(',\"heightMsg\":\"' + msg + '\"')
            if self._invalidWidth:
                attributes = None
                msg = ''
                if isinstance(parent, AbstractOrderedLayout):
                    ol = parent
                    horizontal = True
                    if isinstance(ol, OrderedLayout):
                        if ol.getOrientation() == OrderedLayout.ORIENTATION_VERTICAL:
                            horizontal = False
                    elif isinstance(ol, VerticalLayout):
                        horizontal = False
                    if horizontal:
                        msg = 'Component with relative width inside a HorizontalLayout with no width defined'
                        attributes = self.getWidthAttributes(self._component)
                    else:
                        msg = 'At least one of a VerticalLayout\'s components must have non relative width if the width of the layout is not defined'
                        attributes = self.getWidthAttributes(self._component)
                elif isinstance(parent, GridLayout):
                    msg = 'At least one of the GridLayout\'s components in each column should have non relative width if the width of the layout is not defined.'
                    attributes = self.getWidthAttributes(self._component)
                else:
                    # default error for non sized parent issue
                    msg = 'A component with relative width needs a parent with defined width.'
                    attributes = self.getWidthAttributes(self._component)
                clientJSON.print_(',\"widthMsg\":\"' + msg + '\"')
                self.printServerError(msg, attributes, True, serverErrorStream)
            if len(self._subErrors) > 0:
                print 'Sub errors >>'
                clientJSON.write(', \"subErrors\" : [')
                first = True
                for subError in self._subErrors:
                    if not first:
                        clientJSON.print_(',')
                    else:
                        first = False
                    subError.reportErrors(clientJSON, communicationManager, serverErrorStream)
                clientJSON.write(']')
                print '<< Sub erros'
            clientJSON.write('}')

    class ComponentInfo(Serializable):
        _component = None
        _info = None

        def __init__(self, component, info):
            self._component = component
            self._info = info
