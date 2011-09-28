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

from muntjac.ui.AbstractComponentContainer import AbstractComponentContainer

#from muntjac.terminal.gwt.client.ui.VCustomComponent import VCustomComponent
#from muntjac.ui.ClientWidget import LoadStyle


class CustomComponent(AbstractComponentContainer):
    """Custom component provides simple implementation of Component interface for
    creation of new UI components by composition of existing components.
    <p>
    The component is used by inheriting the CustomComponent class and setting
    composite root inside the Custom component. The composite root itself can
    contain more components, but their interfaces are hidden from the users.
    </p>

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

#    CLIENT_WIDGET = VCustomComponent
#    LOAD_STYLE = LoadStyle.EAGER


    def __init__(self, compositionRoot=None):
        """Constructs a new custom component.

        <p>
        The component is implemented by wrapping the methods of the composition
        root component given as parameter. The composition root must be set
        before the component can be used.
        </p>
        ---
        Constructs a new custom component.

        <p>
        The component is implemented by wrapping the methods of the composition
        root component given as parameter. The composition root must not be null
        and can not be changed after the composition.
        </p>

        @param compositionRoot
                   the root of the composition component tree.
        """
        # The root component implementing the custom component.
        self._root = None

        # Type of the component.
        self._componentType = None

        # expand horizontally by default
        self.setWidth(100, self.UNITS_PERCENTAGE)

        if compositionRoot is not None:
            self.setCompositionRoot(compositionRoot)


    def getCompositionRoot(self):
        """Returns the composition root.

        @return the Component Composition root.
        """
        return self._root


    def setCompositionRoot(self, compositionRoot):
        """Sets the compositions root.
        <p>
        The composition root must be set to non-null value before the component
        can be used. The composition root can only be set once.
        </p>

        @param compositionRoot
                   the root of the composition component tree.
        """
        if compositionRoot != self._root:
            if self._root is not None:
                # remove old component
                super(CustomComponent, self).removeComponent(self._root)

            if compositionRoot is not None:
                # set new component
                super(CustomComponent, self).addComponent(compositionRoot)

            self._root = compositionRoot
            self.requestRepaint()


    def paintContent(self, target):
        if self._root is None:
            raise ValueError, 'Composition root must be set to' \
                    + ' non-null value before the ' \
                    + self.getClass().getName() \
                    + ' can be painted'

        if self.getComponentType() is not None:
            target.addAttribute('type', self.getComponentType())

        self._root.paint(target)


    def getComponentType(self):
        """Gets the component type.

        The component type is textual type of the component. This is included in
        the UIDL as component tag attribute.

        @deprecated not more useful as the whole tag system has been removed

        @return the component type.
        """
        return self._componentType


    def setComponentType(self, componentType):
        """Sets the component type.

        The component type is textual type of the component. This is included in
        the UIDL as component tag attribute.

        @deprecated not more useful as the whole tag system has been removed

        @param componentType
                   the componentType to set.
        """
        self._componentType = componentType


    def getComponentIterator(self):
        return ComponentIterator(self)


    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the iterator
        returned by {@link #getComponentIterator()}.

        @return the number of contained components (zero or one)
        """
        return 1 if self._root is not None else 0


    def replaceComponent(self, oldComponent, newComponent):
        """This method is not supported by CustomComponent.

        @see com.vaadin.ui.ComponentContainer#replaceComponent(com.vaadin.ui.Component,
             com.vaadin.ui.Component)
        """
        raise NotImplementedError


    def addComponent(self, c):
        """This method is not supported by CustomComponent. Use
        {@link CustomComponent#setCompositionRoot(Component)} to set
        CustomComponents "child".

        @see com.vaadin.ui.AbstractComponentContainer#addComponent(com.vaadin.ui.Component)
        """
        raise NotImplementedError


    def moveComponentsFrom(self, source):
        """This method is not supported by CustomComponent.

        @see com.vaadin.ui.AbstractComponentContainer#moveComponentsFrom(com.vaadin.ui.ComponentContainer)
        """
        raise NotImplementedError


    def removeAllComponents(self):
        """This method is not supported by CustomComponent.

        @see com.vaadin.ui.AbstractComponentContainer#removeAllComponents()
        """
        raise NotImplementedError


    def removeComponent(self, c):
        """This method is not supported by CustomComponent.

        @see com.vaadin.ui.AbstractComponentContainer#removeComponent(com.vaadin.ui.Component)
        """
        raise NotImplementedError


class ComponentIterator(object):  # FIXME: implement iterator

    def __init__(self, c):
        self._first = c.getCompositionRoot() is not None


    def hasNext(self):
        return self._first


    def __iter__(self):
        self._first = False
        return self.root


    def remove(self):
        raise NotImplementedError
