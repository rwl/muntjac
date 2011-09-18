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
from com.vaadin.ui.AbstractComponentContainer import (AbstractComponentContainer,)
# from java.io.Serializable import (Serializable,)
# from java.util.Iterator import (Iterator,)


class CustomComponent(AbstractComponentContainer):
    """Custom component provides simple implementation of Component interface for
    creation of new UI components by composition of existing components.
    <p>
    The component is used by inheriting the CustomComponent class and setting
    composite root inside the Custom component. The composite root itself can
    contain more components, but their interfaces are hidden from the users.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # The root component implementing the custom component.
    _root = None
    # Type of the component.
    _componentType = None

    def __init__(self, *args):
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
        # expand horizontally by default
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setWidth(100, self.UNITS_PERCENTAGE)
        elif _1 == 1:
            compositionRoot, = _0
            self.__init__()
            self.setCompositionRoot(compositionRoot)
        else:
            raise ARGERROR(0, 1)

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
        # Basic component features ------------------------------------------
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
            raise self.IllegalStateException('Composition root must be set to' + ' non-null value before the ' + self.getClass().getName() + ' can be painted')
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

    class ComponentIterator(Iterator, Serializable):
        _first = self.getCompositionRoot() is not None

        def hasNext(self):
            return self._first

        def next(self):
            self._first = False
            return self.root

        def remove(self):
            raise self.UnsupportedOperationException()

    def getComponentIterator(self):
        return self.ComponentIterator()

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
        raise self.UnsupportedOperationException()

    def addComponent(self, c):
        """This method is not supported by CustomComponent. Use
        {@link CustomComponent#setCompositionRoot(Component)} to set
        CustomComponents "child".

        @see com.vaadin.ui.AbstractComponentContainer#addComponent(com.vaadin.ui.Component)
        """
        raise self.UnsupportedOperationException()

    def moveComponentsFrom(self, source):
        """This method is not supported by CustomComponent.

        @see com.vaadin.ui.AbstractComponentContainer#moveComponentsFrom(com.vaadin.ui.ComponentContainer)
        """
        raise self.UnsupportedOperationException()

    def removeAllComponents(self):
        """This method is not supported by CustomComponent.

        @see com.vaadin.ui.AbstractComponentContainer#removeAllComponents()
        """
        raise self.UnsupportedOperationException()

    def removeComponent(self, c):
        """This method is not supported by CustomComponent.

        @see com.vaadin.ui.AbstractComponentContainer#removeComponent(com.vaadin.ui.Component)
        """
        raise self.UnsupportedOperationException()
