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
from com.vaadin.data.util.AbstractBeanContainer import (AbstractBeanContainer,)


class BeanItemContainer(AbstractBeanContainer):
    """An in-memory container for JavaBeans.

    <p>
    The properties of the container are determined automatically by introspecting
    the used JavaBean class. Only beans of the same type can be added to the
    container.
    </p>

    <p>
    BeanItemContainer uses the beans themselves as identifiers. The
    {@link Object#hashCode()} of a bean is used when storing and looking up beans
    so it must not change during the lifetime of the bean (it should not depend
    on any part of the bean that can be modified). Typically this restricts the
    implementation of {@link Object#equals(Object)} as well in order for it to
    fulfill the contract between {@code equals()} and {@code hashCode()}.
    </p>

    <p>
    To add items to the container, use the methods {@link #addBean(Object)},
    {@link #addBeanAfter(Object, Object)} and {@link #addBeanAt(int, Object)}.
    Also {@link #addItem(Object)}, {@link #addItemAfter(Object, Object)} and
    {@link #addItemAt(int, Object)} can be used as synonyms for them.
    </p>

    <p>
    It is not possible to add additional properties to the container and nested
    bean properties are not supported.
    </p>

    @param <BEANTYPE>
               The type of the Bean

    @since 5.4
    """

    class IdentityBeanIdResolver(BeanIdResolver):
        """Bean identity resolver that returns the bean itself as its item
        identifier.

        This corresponds to the old behavior of {@link BeanItemContainer}, and
        requires suitable (identity-based) equals() and hashCode() methods on the
        beans.

        @param <BT>

        @since 6.5
        """

        def getIdForBean(self, bean):
            return bean

    def __init__(self, *args):
        """Constructs a {@code BeanItemContainer} for beans of the given type.

        @param type
                   the type of the beans that will be added to the container.
        @throws IllegalArgumentException
                    If {@code type} is null
        ---
        Constructs a {@code BeanItemContainer} and adds the given beans to it.
        The collection must not be empty.
        {@link BeanItemContainer#BeanItemContainer(Class)} can be used for
        creating an initially empty {@code BeanItemContainer}.

        Note that when using this constructor, the actual class of the first item
        in the collection is used to determine the bean properties supported by
        the container instance, and only beans of that class or its subclasses
        can be added to the collection. If this is problematic or empty
        collections need to be supported, use {@link #BeanItemContainer(Class)}
        and {@link #addAll(Collection)} instead.

        @param collection
                   a non empty {@link Collection} of beans.
        @throws IllegalArgumentException
                    If the collection is null or empty.

        @deprecated use {@link #BeanItemContainer(Class, Collection)} instead
        ---
        Constructs a {@code BeanItemContainer} and adds the given beans to it.

        @param type
                   the type of the beans that will be added to the container.
        @param collection
                   a {@link Collection} of beans (can be empty or null).
        @throws IllegalArgumentException
                    If {@code type} is null
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Class):
                type, = _0
                super(BeanItemContainer, self)(type)
                super(BeanItemContainer, self).setBeanIdResolver(self.IdentityBeanIdResolver())
            else:
                collection, = _0
                self.__init__(self.getBeanClassForCollection(collection), collection)
        elif _1 == 2:
            type, collection = _0
            super(BeanItemContainer, self)(type)
            super(BeanItemContainer, self).setBeanIdResolver(self.IdentityBeanIdResolver())
            if collection is not None:
                self.addAll(collection)
        else:
            raise ARGERROR(1, 2)

    # must assume the class is BT
    # the class information is erased by the compiler

    @classmethod
    def getBeanClassForCollection(cls, collection):
        """Internal helper method to support the deprecated {@link Collection}
        container.

        @param <BT>
        @param collection
        @return
        @throws IllegalArgumentException
        """
        if (collection is None) or collection.isEmpty():
            raise cls.IllegalArgumentException('The collection passed to BeanItemContainer constructor must not be null or empty. Use the other BeanItemContainer constructor.')
        return collection.next().getClass()

    def addAll(self, collection):
        """Adds all the beans from a {@link Collection} in one go. More efficient
        than adding them one by one.

        @param collection
                   The collection of beans to add. Must not be null.
        """
        super(BeanItemContainer, self).addAll(collection)

    def addItemAfter(self, previousItemId, newItemId):
        """Adds the bean after the given bean.

        The bean is used both as the item contents and as the item identifier.

        @param previousItemId
                   the bean (of type BT) after which to add newItemId
        @param newItemId
                   the bean (of type BT) to add (not null)

        @see com.vaadin.data.Container.Ordered#addItemAfter(Object, Object)
        """
        return super(BeanItemContainer, self).addBeanAfter(previousItemId, newItemId)

    def addItemAt(self, index, newItemId):
        """Adds a new bean at the given index.

        The bean is used both as the item contents and as the item identifier.

        @param index
                   Index at which the bean should be added.
        @param newItemId
                   The bean to add to the container.
        @return Returns the new BeanItem or null if the operation fails.
        """
        return super(BeanItemContainer, self).addBeanAt(index, newItemId)

    def addItem(self, itemId):
        """Adds the bean to the Container.

        The bean is used both as the item contents and as the item identifier.

        @see com.vaadin.data.Container#addItem(Object)
        """
        return super(BeanItemContainer, self).addBean(itemId)

    def addBean(self, bean):
        """Adds the bean to the Container.

        The bean is used both as the item contents and as the item identifier.

        @see com.vaadin.data.Container#addItem(Object)
        """
        return self.addItem(bean)

    def setBeanIdResolver(self, beanIdResolver):
        """Unsupported in BeanItemContainer."""
        raise self.UnsupportedOperationException('BeanItemContainer always uses an IdentityBeanIdResolver')
