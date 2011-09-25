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

from muntjac.data.util.AbstractBeanContainer import AbstractBeanContainer


class BeanContainer(AbstractBeanContainer):
    """An in-memory container for JavaBeans.

    <p>
    The properties of the container are determined automatically by introspecting
    the used JavaBean class. Only beans of the same type can be added to the
    container.
    </p>

    <p>
    In BeanContainer (unlike {@link BeanItemContainer}), the item IDs do not have
    to be the beans themselves. The container can be used either with explicit
    item IDs or the item IDs can be generated when adding beans.
    </p>

    <p>
    To use explicit item IDs, use the methods {@link #addItem(Object, Object)},
    {@link #addItemAfter(Object, Object, Object)} and
    {@link #addItemAt(int, Object, Object)}.
    </p>

    <p>
    If a bean id resolver is set using
    {@link #setBeanIdResolver(com.vaadin.data.util.AbstractBeanContainer.BeanIdResolver)}
    or {@link #setBeanIdProperty(Object)}, the methods {@link #addBean(Object)},
    {@link #addBeanAfter(Object, Object)}, {@link #addBeanAt(int, Object)} and
    {@link #addAll(java.util.Collection)} can be used to add items to the
    container. If one of these methods is called, the resolver is used to
    generate an identifier for the item (must not return null).
    </p>

    <p>
    Note that explicit item identifiers can also be used when a resolver has been
    set by calling the addItem*() methods - the resolver is only used when adding
    beans using the addBean*() or {@link #addAll(Collection)} methods.
    </p>

    <p>
    It is not possible to add additional properties to the container and nested
    bean properties are not supported.
    </p>

    @param <IDTYPE>
               The type of the item identifier
    @param <BEANTYPE>
               The type of the Bean

    @see AbstractBeanContainer
    @see BeanItemContainer

    @since 6.5
    """

    def __init__(self, typ):
        super(BeanContainer, self)(typ)


    def addItem(self, itemId, bean):
        """Adds the bean to the Container.

        @see com.vaadin.data.Container#addItem(Object)
        """
        if itemId is not None and bean is not None:
            return super(BeanContainer, self).addItem(itemId, bean)
        else:
            return None


    def addItemAfter(self, previousItemId, newItemId, bean):
        """Adds the bean after the given item id.

        @see com.vaadin.data.Container.Ordered#addItemAfter(Object, Object)
        """
        if newItemId is not None and bean is not None:
            return super(BeanContainer, self).addItemAfter(previousItemId, newItemId, bean)
        else:
            return None


    def addItemAt(self, index, newItemId, bean):
        """Adds a new bean at the given index.

        The bean is used both as the item contents and as the item identifier.

        @param index
                   Index at which the bean should be added.
        @param newItemId
                   The item id for the bean to add to the container.
        @param bean
                   The bean to add to the container.

        @return Returns the new BeanItem or null if the operation fails.
        """
        # automatic item id resolution
        if newItemId is not None and bean is not None:
            return super(BeanContainer, self).addItemAt(index, newItemId, bean)
        else:
            return None


    def setBeanIdProperty(self, propertyId):
        """Sets the bean id resolver to use a property of the beans as the
        identifier.

        @param propertyId
                   the identifier of the property to use to find item identifiers
        """
        self.setBeanIdResolver(self.createBeanPropertyResolver(propertyId))


    def setBeanIdResolver(self, beanIdResolver):
        super(BeanContainer, self).setBeanIdResolver(beanIdResolver)


    def addBean(self, bean):
        return super(BeanContainer, self).addBean(bean)


    def addBeanAfter(self, previousItemId, bean):
        return super(BeanContainer, self).addBeanAfter(previousItemId, bean)


    def addBeanAt(self, index, bean):
        return super(BeanContainer, self).addBeanAt(index, bean)


    def addAll(self, collection):
        super(BeanContainer, self).addAll(collection)
