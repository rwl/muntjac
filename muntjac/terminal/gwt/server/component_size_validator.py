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

import logging
import traceback

from collections import deque

try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from muntjac.ui.ordered_layout import OrderedLayout
from muntjac.terminal.sizeable import ISizeable
from muntjac.ui.custom_component import CustomComponent
from muntjac.ui.panel import Panel
from muntjac.ui.component_container import IComponentContainer
from muntjac.ui.form import Form
from muntjac.ui.window import Window
from muntjac.ui.abstract_ordered_layout import AbstractOrderedLayout
from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.ui.grid_layout import GridLayout
from muntjac.ui.split_panel import SplitPanel
from muntjac.ui.tab_sheet import TabSheet


logger = logging.getLogger(__name__)


class ComponentSizeValidator(object):

    _LAYERS_SHOWN = 4

    _creationLocations = dict()
    _widthLocations = dict()
    _heightLocations = dict()

    @classmethod
    def validateComponentRelativeSizes(cls, component, errors, parent):
        """Recursively checks given component and its subtree for invalid
        layout setups. Prints errors to std err stream.

        @param component:
                   component to check
        @return: set of first level errors found
        """

        invalidHeight = not cls.checkHeights(component)
        invalidWidth = not cls.checkWidths(component)

        if invalidHeight or invalidWidth:
            error = InvalidLayout(component, invalidHeight, invalidWidth)
            if parent is not None:
                parent.addError(error)
            else:
                if errors is None:
                    errors = list()
                errors.append(error)
            parent = error

        if isinstance(component, Panel):
            panel = component
            errors = cls.validateComponentRelativeSizes(panel.getContent(),
                    errors, parent)

        elif isinstance(component, IComponentContainer):
            lo = component
            for c in lo.getComponentIterator():
                errors = cls.validateComponentRelativeSizes(c, errors, parent)

        elif isinstance(component, Form):
            form = component
            if form.getLayout() is not None:
                errors = cls.validateComponentRelativeSizes(form.getLayout(),
                        errors, parent)
            if form.getFooter() is not None:
                errors = cls.validateComponentRelativeSizes(form.getFooter(),
                        errors, parent)

        return errors


    @classmethod
    def printServerError(cls, msg, attributes, widthError, errorStream):
        err = StringIO()
        err.write('Muntjac DEBUG\n')

        indent = str()
        if attributes is not None:
            while len(attributes) > cls._LAYERS_SHOWN:
                attributes.pop()
            while len(attributes) > 0:
                ci = attributes.pop()
                cls.showComponent(ci.component, ci.info, err, indent,
                        widthError)

        err.write('Layout problem detected: ')
        err.write(msg)
        err.write('\n')
        err.write('Relative sizes were replaced by undefined sizes, '
                'components may not render as expected.\n')
        errorStream.write(err.getvalue())
        err.close()


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
        except Exception:
            logger.info('An exception occurred while validating sizes.')
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
        except Exception:
            logger.info('An exception occurred while validating sizes.')
            return True


    @classmethod
    def getHeightAttributes(cls, component):
        attributes = deque()
        info = ComponentInfo(component, cls.getHeightString(component))
        attributes.append(info)
        parent = component.getParent()
        info = ComponentInfo(parent, cls.getHeightString(parent))
        attributes.append(info)

        while parent is not None:
            info = ComponentInfo(parent, cls.getHeightString(parent))
            attributes.append(info)
            parent = parent.getParent()

        return attributes


    @classmethod
    def getWidthAttributes(cls, component):
        attributes = deque()
        info = ComponentInfo(component, cls.getWidthString(component))
        attributes.append(info)
        parent = component.getParent()
        info = ComponentInfo(parent, cls.getWidthString(parent))
        attributes.append(info)

        while parent is not None:
            info = ComponentInfo(parent, cls.getWidthString(parent))
            attributes.append(info)
            parent = parent.getParent()

        return attributes


    @classmethod
    def getWidthString(cls, component):
        width = 'width: '
        if cls.hasRelativeWidth(component):
            width += 'RELATIVE, ' + component.getWidth() + ' %'
        elif isinstance(component, Window) and component.getParent() is None:
            width += 'MAIN WINDOW'
        elif component.getWidth() >= 0:
            width += 'ABSOLUTE, ' + component.getWidth() + ' ' \
                + ISizeable.UNIT_SYMBOLS[ component.getWidthUnits() ]
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
            height += 'ABSOLUTE, ' + component.getHeight() + ' ' \
                + ISizeable.UNIT_SYMBOLS[ component.getHeightUnits() ]
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

        err.write(indent)
        indent.write('  ')
        err.write('- ')
        err.write(component.__class__.__name__)
        err.write('/')
        err.write(hex( hash(component) ))

        if component.getCaption() is not None:
            err.write(' \"')
            err.write(component.getCaption())
            err.write('\"')

        if component.getDebugId() is not None:
            err.write(' debugId: ')
            err.write(component.getDebugId())

        if createLoc is not None:
            err.write(', created at (' + createLoc.file \
                    + ':' + createLoc.lineNumber + ')')

        if attribute is not None:
            err.write(' (')
            err.write(attribute)
            if sizeLoc is not None:
                err.write(', set at (' + sizeLoc.file
                        + ':' + sizeLoc.lineNumber + ')')
            err.write(')')

        err.write('\n')


    @classmethod
    def hasNonRelativeHeightComponent(cls, ol):
        for c in ol.getComponentIterator():
            if not cls.hasRelativeHeight(c):
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
                    horizontal = (parent.getOrientation() ==
                            OrderedLayout.ORIENTATION_HORIZONTAL)
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

                row = componentArea.getRow1()
                while not rowHasHeight and row <= componentArea.getRow2():
                    row += 1
                    column = 0
                    while not rowHasHeight and column < gl.getColumns():
                        column += 1
                        c = gl.getComponent(column, row)
                        if c is not None:
                            rowHasHeight = not cls.hasRelativeHeight(c)

                if not rowHasHeight:
                    return False
                else:
                    # Other components define row height
                    return True

            if isinstance(parent, Panel) \
                    or isinstance(parent, SplitPanel) \
                    or isinstance(parent, TabSheet) \
                    or isinstance(parent, CustomComponent):
                # height undefined, we know how how component works and no
                # exceptions
                # TODO horiz SplitPanel ??
                return False
            else:
                # We cannot generally know if undefined component can serve
                # space for children (like CustomLayout or component built
                # by third party) so we assume they can
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
        return (component.getHeightUnits() == ISizeable.UNITS_PERCENTAGE
                and component.getHeight() > 0)


    @classmethod
    def hasNonRelativeWidthComponent(cls, arg):
        if isinstance(arg, AbstractOrderedLayout):
            ol = arg
            for c in ol.getComponentIterator():
                if not cls.hasRelativeWidth(c):
                    return True
            return False
        else:
            form = arg
            layout = form.getLayout()
            footer = form.getFooter()

            if layout is not None and not cls.hasRelativeWidth(layout):
                return True

            if footer is not None and not cls.hasRelativeWidth(footer):
                return True

            return False


    @classmethod
    def hasRelativeWidth(cls, paintable):
        return (paintable.getWidth() > 0
                and paintable.getWidthUnits() == ISizeable.UNITS_PERCENTAGE)


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
                    if (ol.getOrientation()
                            == OrderedLayout.ORIENTATION_VERTICAL):
                        horizontal = False
                elif isinstance(ol, VerticalLayout):
                    horizontal = False
                if (not horizontal) and cls.hasNonRelativeWidthComponent(ol):
                    # valid situation, other components defined width
                    return True
                else:
                    return False
            elif isinstance(parent, GridLayout):
                gl = parent
                componentArea = gl.getComponentArea(component)
                columnHasWidth = False
                col = componentArea.getColumn1()
                while ((not columnHasWidth)
                       and col <= componentArea.getColumn2()):
                    col += 1
                    row = 0
                    while (not columnHasWidth) and row < gl.getRows():
                        row += 1
                        c = gl.getComponent(col, row)
                        if c is not None:
                            columnHasWidth = not cls.hasRelativeWidth(c)

                if not columnHasWidth:
                    return False
                else:
                    # Other components define column width
                    return True
            elif isinstance(parent, Form):
                # If some other part of the form is not relative it
                # determines the component width
                return cls.hasNonRelativeWidthComponent(parent)
            elif (isinstance(parent, SplitPanel)
                    or isinstance(parent, TabSheet)
                    or isinstance(parent, CustomComponent)):
                # FIXME: Could we use com.vaadin package name here and
                # fail for all component containers?
                # FIXME: Actually this should be moved to containers so
                # it can be implemented for custom containers
                # TODO vertical splitpanel with another non relative
                # component?
                return False
            elif isinstance(parent, Window):
                # Sub window can define width based on caption
                if (parent.getCaption() is not None
                        and not (parent.getCaption() == '')):
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


    @classmethod
    def setCreationLocation(cls, obj):
        cls.setLocation(cls._creationLocations, obj)


    @classmethod
    def setWidthLocation(cls, obj):
        cls.setLocation(cls._widthLocations, obj)


    @classmethod
    def setHeightLocation(cls, obj):
        cls.setLocation(cls._heightLocations, obj)


    @classmethod
    def setLocation(cls, mapp, obj):
        traceLines = traceback.extract_stack()
        for traceElement in traceLines:
            try:
                # FIXME: reduce map sizes

#                clsName = traceElement.getClassName()
#                if clsName.startswith('java.') or clsName.startswith('sun.'):
#                    continue
#
#                clss = loadClass(clsName)
#                if (clss == ComponentSizeValidator) or (clss == Thread):
#                    continue
#
#                if (Component in clss.mro()
#                        and not CustomComponent in clss.mro()):
#                    continue

                cl = FileLocation(traceElement)
                map[object] = cl
                return
            except Exception:
                # TODO Auto-generated catch block
                logger.info('An exception occurred while validating sizes.')


class FileLocation(object):

    def __init__(self, traceElement):
        # filename, line number, function name, text
        self.file = traceElement[0]
        self.className = traceElement[2]
        self.classNameSimple = traceElement[2]
        self.lineNumber = traceElement[1]
        self.method = traceElement[2]


class InvalidLayout(object):

    def __init__(self, component, height, width):
        self._component = component
        self._invalidHeight = height
        self._invalidWidth = width
        self._subErrors = list()


    def addError(self, error):
        self._subErrors.append(error)


    def reportErrors(self, clientJSON, communicationManager,
                serverErrorStream):
        clientJSON.write('{')

        parent = self._component.getParent()
        paintableId = communicationManager.getPaintableId(self._component)

        clientJSON.write('id:\"' + paintableId + '\"')

        if self._invalidHeight:
            attributes = None
            msg = ''
            # set proper error messages
            if isinstance(parent, AbstractOrderedLayout):
                ol = parent
                vertical = False

                if isinstance(ol, OrderedLayout):
                    if (ol.getOrientation()
                            == OrderedLayout.ORIENTATION_VERTICAL):
                        vertical = True
                elif isinstance(ol, VerticalLayout):
                    vertical = True

                if vertical:
                    msg = ('Component with relative height inside a '
                            'VerticalLayout with no height defined.')
                    attributes = ComponentSizeValidator.getHeightAttributes(
                            self._component)
                else:
                    msg = ('At least one of a HorizontalLayout\'s components '
                           'must have non relative height if the height of '
                           'the layout is not defined')
                    attributes = ComponentSizeValidator.getHeightAttributes(
                            self._component)
            elif isinstance(parent, GridLayout):
                msg = ('At least one of the GridLayout\'s components in '
                        'each row should have non relative height if the '
                        'height of the layout is not defined.')
                attributes = ComponentSizeValidator.getHeightAttributes(
                        self._component)
            else:
                # default error for non sized parent issue
                msg = ('A component with relative height needs a parent '
                        'with defined height.')
                attributes = ComponentSizeValidator.getHeightAttributes(
                        self._component)

            self.printServerError(msg, attributes, False, serverErrorStream)
            clientJSON.write(',\"heightMsg\":\"' + msg + '\"')

        if self._invalidWidth:
            attributes = None
            msg = ''
            if isinstance(parent, AbstractOrderedLayout):
                ol = parent
                horizontal = True

                if isinstance(ol, OrderedLayout):
                    if (ol.getOrientation()
                            == OrderedLayout.ORIENTATION_VERTICAL):
                        horizontal = False
                elif isinstance(ol, VerticalLayout):
                    horizontal = False

                if horizontal:
                    msg = ('Component with relative width inside a '
                           'HorizontalLayout with no width defined')
                    attributes = ComponentSizeValidator.getWidthAttributes(
                            self._component)
                else:
                    msg = ('At least one of a VerticalLayout\'s components '
                            'must have non relative width if the width of '
                            'the layout is not defined')
                    attributes = ComponentSizeValidator.getWidthAttributes(
                            self._component)

            elif isinstance(parent, GridLayout):
                msg = ('At least one of the GridLayout\'s components in each '
                       'column should have non relative width if the width '
                       'of the layout is not defined.')
                attributes = ComponentSizeValidator.getWidthAttributes(
                        self._component)

            else:
                # default error for non sized parent issue
                msg = ('A component with relative width needs a parent '
                       'with defined width.')
                attributes = self.getWidthAttributes(self._component)

            clientJSON.write(',\"widthMsg\":\"' + msg + '\"')
            self.printServerError(msg, attributes, True, serverErrorStream)

        if len(self._subErrors) > 0:
            serverErrorStream.write('Sub errors >>')
            clientJSON.write(', \"subErrors\" : [')
            first = True
            for subError in self._subErrors:
                if not first:
                    clientJSON.write(',')
                else:
                    first = False
                subError.reportErrors(clientJSON, communicationManager,
                        serverErrorStream)
            clientJSON.write(']')
            serverErrorStream.write('<< Sub erros\n')

        clientJSON.write('}')


class ComponentInfo(object):

    def __init__(self, component, info):
        self._component = component
        self._info = info
