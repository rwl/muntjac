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

"""Defines a simple implementation of IComponent interface for creation
of new UI components by composition of existing components."""

from warnings import warn

from muntjac.util import fullname

from muntjac.ui.abstract_component_container import AbstractComponentContainer


class CustomComponent(AbstractComponentContainer):
    """Custom component provides simple implementation of Component interface
    for creation of new UI components by composition of existing components.

    The component is used by inheriting the CustomComponent class and setting
    composite root inside the Custom component. The composite root itself can
    contain more components, but their interfaces are hidden from the users.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    CLIENT_WIDGET = None #ClientWidget(VCustomComponent, LoadStyle.EAGER)

    def __init__(self, compositionRoot=None):
        """Constructs a new custom component.

        The component is implemented by wrapping the methods of the
        composition root component given as parameter. The composition root
        must not be null and can not be changed after the composition.

        @param compositionRoot:
                   the root of the composition component tree.
        """

        # The root component implementing the custom component.
        self._root = None

        # Type of the component.
        self._componentType = None

        super(CustomComponent, self).__init__()

        # expand horizontally by default
        self.setWidth(100, self.UNITS_PERCENTAGE)

        if compositionRoot is not None:
            self.setCompositionRoot(compositionRoot)


    def getCompositionRoot(self):
        """Returns the composition root.

        @return: the Component Composition root.
        """
        return self._root


    def setCompositionRoot(self, compositionRoot):
        """Sets the compositions root.

        The composition root must be set to non-null value before the
        component can be used. The composition root can only be set once.

        @param compositionRoot:
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
            raise ValueError, ('Composition root must be set to'
                    + ' non-null value before the ' + fullname(self)
                    + ' can be painted')

        if self.getComponentType() is not None:
            target.addAttribute('type', self.getComponentType())

        self._root.paint(target)


    def getComponentType(self):
        """Gets the component type.

        The component type is textual type of the component. This is included
        in the UIDL as component tag attribute.

        @deprecated: not more useful as the whole tag system has been removed

        @return: the component type.
        """
        warn('tag system has been removed', DeprecationWarning)
        return self._componentType


    def setComponentType(self, componentType):
        """Sets the component type.

        The component type is textual type of the component. This is included
        in the UIDL as component tag attribute.

        @deprecated: not more useful as the whole tag system has been removed

        @param componentType:
                   the componentType to set.
        """
        warn('tag system has been removed', DeprecationWarning)
        self._componentType = componentType


    def getComponentIterator(self):
        return ComponentIterator(self)


    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the
        iterator returned by L{getComponentIterator}.

        @return: the number of contained components (zero or one)
        """
        return 1 if self._root is not None else 0


    def replaceComponent(self, oldComponent, newComponent):
        """This method is not supported by CustomComponent.

        @see: L{ComponentContainer.replaceComponent()}
        """
        raise NotImplementedError


    def addComponent(self, c):
        """This method is not supported by CustomComponent. Use
        L{CustomComponent.setCompositionRoot} to set CustomComponents "child".

        @see: L{AbstractComponentContainer.addComponent}
        """
        raise NotImplementedError


    def moveComponentsFrom(self, source):
        """This method is not supported by CustomComponent.

        @see: L{AbstractComponentContainer.moveComponentsFrom}
        """
        raise NotImplementedError


    def removeAllComponents(self):
        """This method is not supported by CustomComponent.

        @see: L{AbstractComponentContainer.removeAllComponents}
        """
        raise NotImplementedError


    def removeComponent(self, c):
        """This method is not supported by CustomComponent.

        @see: L{AbstractComponentContainer.removeComponent}
        """
        raise NotImplementedError


class ComponentIterator(object):

    def __init__(self, c):
        self._component = c
        self._first = c.getCompositionRoot() is not None


    def __iter__(self):
        return self


    def hasNext(self):
        return self._first


    def next(self):  #@PydevCodeAnalysisIgnore
        if not self._first:
            raise StopIteration
        self._first = False
        return self._component._root


    def remove(self):
        raise NotImplementedError
