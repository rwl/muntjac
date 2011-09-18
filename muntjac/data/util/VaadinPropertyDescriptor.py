# -*- coding: utf-8 -*-
# from java.io.Serializable import (Serializable,)


class VaadinPropertyDescriptor(Serializable):
    """Property descriptor that can create a property instance for a bean.

    Used by {@link BeanItem} and {@link AbstractBeanContainer} to keep track of
    the set of properties of items.

    @param <BT>
               bean type

    @since 6.6
    """

    def getName(self):
        """Returns the name of the property.

        @return
        """
        pass

    def getPropertyType(self):
        """Returns the type of the property.

        @return Class<?>
        """
        pass

    def createProperty(self, bean):
        """Creates a new {@link Property} instance for this property for a bean.

        @param bean
        @return
        """
        pass
