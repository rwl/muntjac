# -*- coding: utf-8 -*-
from com.vaadin.data.util.NestedMethodProperty import (NestedMethodProperty,)
from com.vaadin.data.util.VaadinPropertyDescriptor import (VaadinPropertyDescriptor,)


class NestedPropertyDescriptor(VaadinPropertyDescriptor):
    """Property descriptor that is able to create nested property instances for a
    bean.

    The property is specified in the dotted notation, e.g. "address.street", and
    can contain multiple levels of nesting.

    @param <BT>
               bean type

    @since 6.6
    """
    _name = None
    _propertyType = None

    def __init__(self, name, beanType):
        """Creates a property descriptor that can create MethodProperty instances to
        access the underlying bean property.

        @param name
                   of the property in a dotted path format, e.g. "address.street"
        @param beanType
                   type (class) of the top-level bean
        @throws IllegalArgumentException
                    if the property name is invalid
        """
        self._name = name
        property = NestedMethodProperty(beanType, name)
        self._propertyType = property.getType()

    def getName(self):
        return self._name

    def getPropertyType(self):
        return self._propertyType

    def createProperty(self, bean):
        return NestedMethodProperty(bean, self._name)
