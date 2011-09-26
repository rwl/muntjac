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

from muntjac.ui.AbstractLayout import AbstractLayout
from muntjac.ui.Component import Component

#from muntjac.terminal.gwt.client.ui.VCustomLayout import VCustomLayout
#from muntjac.ui.ClientWidget import LoadStyle


class CustomLayout(AbstractLayout):
    """<p>
    A container component with freely designed layout and style. The layout
    consists of items with textually represented locations. Each item contains
    one sub-component, which can be any Vaadin component, such as a layout. The
    adapter and theme are responsible for rendering the layout with a given style
    by placing the items in the defined locations.
    </p>

    <p>
    The placement of the locations is not fixed - different themes can define the
    locations in a way that is suitable for them. One typical example would be to
    create visual design for a web site as a custom layout: the visual design
    would define locations for "menu", "body", and "title", for example. The
    layout would then be implemented as an XHTML template for each theme.
    </p>

    <p>
    The default theme handles the styles that are not defined by drawing the
    subcomponents just as in OrderedLayout.
    </p>

    @author IT Mill Ltd.
    @author Duy B. Vo (<a
            href="mailto:devduy@gmail.com?subject=Vaadin">devduy@gmail.com</a>)
    @version
    @VERSION@
    @since 3.0
    """

#    CLIENT_WIDGET = VCustomLayout
#    LOAD_STYLE = LoadStyle.EAGER

    _BUFFER_SIZE = 10000

    def __init__(self, template=None):
        """Default constructor only used by subclasses. Subclasses are responsible
        for setting the appropriate fields. Either
        {@link #setTemplateName(String)}, that makes layout fetch the template
        from theme, or {@link #setTemplateContents(String)}.
        ---
        Constructs a custom layout with the template given in the stream.

        @param templateStream
                   Stream containing template data. Must be using UTF-8 encoding.
                   To use a String as a template use for instance new
                   ByteArrayInputStream("<template>".getBytes()).
        @param streamLength
                   Length of the templateStream
        @throws IOException
        ---
        Constructor for custom layout with given template name. Template file is
        fetched from "<theme>/layout/<templateName>".
        """
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
        """Adds the component into this container to given location. If the location
        is already populated, the old component is removed.

        @param c
                   the component to be added.
        @param location
                   the location of the component.
        ---
        Adds the component into this container. The component is added without
        specifying the location (empty string is then used as location). Only one
        component can be added to the default "" location and adding more
        components into that location overwrites the old components.

        @param c
                   the component to be added.
        """
        old = self._slots.get(location)
        if old is not None:
            self.removeComponent(old)
        self._slots[location] = c
        c.setParent(self)
        self.fireComponentAttachEvent(c)
        self.requestRepaint()


    def removeComponent(self, arg):
        """Removes the component from this container.

        @param c
                   the component to be removed.
        ---
        Removes the component from this container from given location.

        @param location
                   the Location identifier of the component.
        """
        if isinstance(arg, Component):
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
        """Gets the component container iterator for going trough all the components
        in the container.

        @return the Iterator of the components inside the container.
        """
        return iter( self._slots.values() )


    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the iterator
        returned by {@link #getComponentIterator()}.

        @return the number of contained components
        """
        return len( self._slots.values() )


    def getComponent(self, location):
        """Gets the child-component by its location.

        @param location
                   the name of the location where the requested component
                   resides.
        @return the Component in the given location or null if not found.
        """
        return self._slots.get(location)


    def paintContent(self, target):
        """Paints the content of this component.

        @param target
        @throws PaintException
                    if the paint operation failed.
        """
        super(CustomLayout, self).paintContent(target)

        if self._templateName is not None:
            target.addAttribute('template', self._templateName)
        else:
            target.addAttribute('templateContents', self._templateContents)

        # Adds all items in all the locations
        for location,c in self._slots.iteritems():
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
            self._slots.put(newLocation, oldComponent)
            self._slots.put(oldLocation, newComponent)
            self.requestRepaint()


    def setStyle(self, name):
        """CustomLayout's template selecting was previously implemented with
        setStyle. Overriding to improve backwards compatibility.

        @param name
                   template name
        @deprecated Use {@link #setTemplateName(String)} instead
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

        With GWT-adapter, the template with name 'templatename' is loaded from
        VAADIN/themes/themename/layouts/templatename.html. If the theme has not
        been set (with Application.setTheme()), themename is 'default'.

        @param templateName
        """
        self._templateName = templateName
        self._templateContents = None
        self.requestRepaint()


    def setTemplateContents(self, templateContents):
        """Set the contents of the template used to draw the custom layout.

        @param templateContents
        """
        self._templateContents = templateContents
        self._templateName = None
        self.requestRepaint()


    def setMargin(self, *args):
        """Although most layouts support margins, CustomLayout does not. The
        behaviour of this layout is determined almost completely by the actual
        template.

        @throws UnsupportedOperationException
        ---
        Although most layouts support margins, CustomLayout does not. The
        behaviour of this layout is determined almost completely by the actual
        template.

        @throws UnsupportedOperationException
        """
        raise NotImplementedError, 'CustomLayout does not support margins.'
