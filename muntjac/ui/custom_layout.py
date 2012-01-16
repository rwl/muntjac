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

"""Defines a container component with freely designed layout and style."""

from muntjac.ui.abstract_layout import AbstractLayout
from muntjac.ui.component import IComponent


class CustomLayout(AbstractLayout):
    """A container component with freely designed layout and style. The
    layout consists of items with textually represented locations. Each item
    contains one sub-component, which can be any Muntjac component, such as a
    layout. The adapter and theme are responsible for rendering the layout
    with a given style by placing the items in the defined locations.

    The placement of the locations is not fixed - different themes can define
    the locations in a way that is suitable for them. One typical example
    would be to create visual design for a web site as a custom layout: the
    visual design would define locations for "menu", "body", and "title", for
    example. The layout would then be implemented as an XHTML template for
    each theme.

    The default theme handles the styles that are not defined by drawing the
    subcomponents just as in OrderedLayout.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @author: Duy B. Vo
    @version: 1.1.0
    """

    CLIENT_WIDGET = None #ClientWidget(VCustomLayout, LoadStyle.EAGER)

    _BUFFER_SIZE = 10000

    def __init__(self, template=None):
        """Default constructor only used by subclasses. Subclasses are
        responsible for setting the appropriate fields. Either
        L{setTemplateName}, that makes layout fetch the template from theme,
        or L{setTemplateContents}.

        Template file is fetched from "<theme>/layout/<templateName>".

        @raise IOException:
        """
        super(CustomLayout, self).__init__()

        # Custom layout slots containing the components.
        self._slots = dict()
        self._templateContents = None
        self._templateName = None

        self.setWidth(100, self.UNITS_PERCENTAGE)

        if template is not None:
            if isinstance(template, basestring):
                self._templateName = template
            else:
                self.initTemplateContentsFromInputStream(template)


    def initTemplateContentsFromInputStream(self, templateStream):
        self._templateContents = templateStream.getvalue()


    def addComponent(self, c, location=''):
        """Adds the component into this container to given location. If
        the location is already populated, the old component is removed.
        If the component is added without specifying the location (empty
        string is then used as location). Only one component can be added
        to the default "" location and adding more components into that
        location overwrites the old components.

        @param c: the component to be added.
        @param location: the location of the component.
        """
        old = self._slots.get(location)
        if old is not None:
            self.removeComponent(old)
        self._slots[location] = c
        c.setParent(self)
        self.fireComponentAttachEvent(c)
        self.requestRepaint()


    def removeComponent(self, arg):
        """Removes the component from this container or the given location.

        @param arg: the component to be removed or the location identifier
                    of the component.
        """
        if isinstance(arg, IComponent):
            c = arg
            if c is None:
                return
            for k, v in self._slots.iteritems():
                if v == c:
                    del self._slots[k]
                    break
            super(CustomLayout, self).removeComponent(c)
            self.requestRepaint()
        else:
            location = arg
            self.removeComponent(self._slots.get(location))


    def getComponentIterator(self):
        """Gets the component container iterator for going trough all
        the components in the container.

        @return: the iterator of the components inside the container.
        """
        return iter( self._slots.values() )


    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the
        iterator returned by L{getComponentIterator}.

        @return: the number of contained components
        """
        return len( self._slots.values() )


    def getComponent(self, location):
        """Gets the child-component by its location.

        @param location: the name of the location where the requested
               component resides.
        @return: the IComponent in the given location or null if not found.
        """
        return self._slots.get(location)


    def paintContent(self, target):
        """Paints the content of this component.

        @raise PaintException: if the paint operation failed.
        """
        super(CustomLayout, self).paintContent(target)

        if self._templateName is not None:
            target.addAttribute('template', self._templateName)
        else:
            target.addAttribute('templateContents', self._templateContents)

        # Adds all items in all the locations
        for location, c in self._slots.iteritems():
            if c is not None:
                # Writes the item
                target.startTag('location')
                target.addAttribute('name', location)
                c.paint(target)
                target.endTag('location')


    def replaceComponent(self, oldComponent, newComponent):
        # Gets the locations
        oldLocation = None
        newLocation = None

        for location, component in self._slots.iteritems():
            if component == oldComponent:
                oldLocation = location
            if component == newComponent:
                newLocation = location

        if oldLocation is None:
            self.addComponent(newComponent)

        elif newLocation is None:
            self.removeComponent(oldLocation)
            self.addComponent(newComponent, oldLocation)

        else:
            self._slots[newLocation] = oldComponent
            self._slots[oldLocation] = newComponent
            self.requestRepaint()


    def setStyle(self, name):
        """CustomLayout's template selecting was previously implemented
        with setStyle. Overriding to improve backwards compatibility.

        @param name: template name
        @deprecated: Use L{setTemplateName} instead
        """
        self.setTemplateName(name)


    def getTemplateName(self):
        """Get the name of the template"""
        return self._templateName


    def getTemplateContents(self):
        """Get the contents of the template"""
        return self._templateContents


    def setTemplateName(self, templateName):
        """Set the name of the template used to draw custom layout.

        With GWT-adapter, the template with name 'templatename' is loaded
        from VAADIN/themes/themename/layouts/templatename.html. If the theme
        has not been set (with Application.setTheme()), themename is
        'default'.
        """
        self._templateName = templateName
        self._templateContents = None
        self.requestRepaint()


    def setTemplateContents(self, templateContents):
        """Set the contents of the template used to draw the custom layout.
        """
        self._templateContents = templateContents
        self._templateName = None
        self.requestRepaint()


    def setMargin(self, *args):
        """Although most layouts support margins, CustomLayout does not.
        The behaviour of this layout is determined almost completely by
        the actual template.

        @raise NotImplementedError: CustomLayout does not support margins
        """
        raise NotImplementedError, 'CustomLayout does not support margins.'
