# Copyright (C) 2010 IT Mill Ltd.
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
from muntjac.terminal.gwt.client.EventId import EventId

from muntjac.event.LayoutEvents import \
    ILayoutClickNotifier, LayoutClickEvent, ILayoutClickListener


class CssLayout(AbstractLayout, ILayoutClickNotifier):
    """CssLayout is a layout component that can be used in browser environment
    only. It simply renders components and their captions into a same div
    element. Component layout can then be adjusted with css.

    In comparison to {@link HorizontalLayout} and {@link VerticalLayout}
    <ul>
    <li>rather similar server side api
    <li>no spacing, alignment or expand ratios
    <li>much simpler DOM that can be styled by skilled web developer
    <li>no abstraction of browser differences (developer must ensure that
    the result works properly on each browser)
    <li>different kind of handling for relative sizes (that are set from
    server side) (*)
    <li>noticeably faster rendering time in some situations as we rely more
    on the browser's rendering engine.
    </ul>

    With {@link CustomLayout} one can often achieve similar results (good
    looking layouts with web technologies), but with CustomLayout developer
    needs to work with fixed templates.

    By extending CssLayout one can also inject some css rules straight to
    child components using {@link #getCss(Component)}.

    (*) Relative sizes (set from server side) are treated bit differently than
    in other layouts in Vaadin. In cssLayout the size is calculated relatively
    to CSS layouts content area which is pretty much as in html and css. In
    other layouts the size of component is calculated relatively to the "slot"
    given by layout.

    Also note that client side framework in Vaadin modifies inline style
    properties width and height. This happens on each update to component. If
    one wants to set component sizes with CSS, component must have undefined
    size on server side (which is not the default for all components) and the
    size must be defined with class styles - not by directly injecting width
    and height.

    @since 6.1 brought in from "FastLayouts" incubator project
    """

    #CLIENT_WIDGET = ClientWidget(VCssLayout)

    _CLICK_EVENT = EventId.LAYOUT_CLICK


    def addComponent(self, c, index=None):
        """Add a component into this container. The component is added to
        the right or under the previous component.

        @param c
                   the component to be added.
        ---
        Adds a component into indexed position in this container.

        @param c
                   the component to be added.
        @param index
                   the Index of the component position. The components
                   currently in and after the position are shifted forwards.
        """
        # Custom layout slots containing the components.
        self.components = list()

        if index is None:
            self.components.append(c)
            try:
                super(CssLayout, self).addComponent(c)
                self.requestRepaint()
            except ValueError, e:
                self.components.remove(c)
                raise e
        else:
            self.components.insert(index, c)
            try:
                super(CssLayout, self).addComponent(c)
                self.requestRepaint()
            except ValueError, e:
                self.components.remove(c)
                raise e


    def addComponentAsFirst(self, c):
        """Adds a component into this container. The component is added to
        the left or on top of the other components.

        @param c
                   the component to be added.
        """
        self.components.insert(0, c)
        try:
            super(CssLayout, self).addComponent(c)
            self.requestRepaint()
        except ValueError, e:
            self.components.remove(c)
            raise e


    def removeComponent(self, c):
        """Removes the component from this container.

        @param c: the component to be removed.
        """
        self.components.remove(c)
        super(CssLayout, self).removeComponent(c)
        self.requestRepaint()


    def getComponentIterator(self):
        """Gets the component container iterator for going trough all the
        components in the container.

        @return the Iterator of the components inside the container.
        """
        return iter(self.components)


    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the
        iterator returned by {@link #getComponentIterator()}.

        @return the number of contained components
        """
        return len(self.components)


    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   the Paint Event.
        @throws PaintException
                    if the paint operation failed.
        """
        super(CssLayout, self).paintContent(target)
        componentCss = None
        # Adds all items in all the locations
        for c in self.components:
            # Paint child component UIDL
            c.paint(target)
            componentCssString = self.getCss(c)
            if componentCssString is not None:
                if componentCss is None:
                    componentCss = dict()
                componentCss[c] = componentCssString
        if componentCss is not None:
            target.addAttribute('css', componentCss)


    def getCss(self, c):
        """Returns styles to be applied to given component. Override this
        method to inject custom style rules to components.

        Note that styles are injected over previous styles before actual
        child rendering. Previous styles are not cleared, but overridden.

        Note that one most often achieves better code style, by separating
        styling to theme (with custom theme and {@link #addStyleName(String)}.
        With own custom styles it is also very easy to break browser
        compatibility.

        @param c: the component
        @return css rules to be applied to component
        """
        return None


    def replaceComponent(self, oldComponent, newComponent):
        # Gets the locations
        oldLocation = -1
        newLocation = -1
        location = 0
        for component in self.components:

            if component == oldComponent:
                oldLocation = location
            if component == newComponent:
                newLocation = location

            location += 1

        if oldLocation == -1:
            self.addComponent(newComponent)
        elif newLocation == -1:
            self.removeComponent(oldComponent)
            self.addComponent(newComponent, oldLocation)
        else:
            if oldLocation > newLocation:
                self.components.remove(oldComponent)
                self.components.append(newLocation, oldComponent)
                self.components.remove(newComponent)
                self.components.append(oldLocation, newComponent)
            else:
                self.components.remove(newComponent)
                self.components.append(oldLocation, newComponent)
                self.components.remove(oldComponent)
                self.components.append(newLocation, oldComponent)
            self.requestRepaint()


    def addListener(self, listener):
        self.addListener(self._CLICK_EVENT, LayoutClickEvent, listener,
                ILayoutClickListener.clickMethod)


    def removeListener(self, listener):
        self.removeListener(self._CLICK_EVENT, LayoutClickEvent, listener)
