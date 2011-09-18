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
from com.vaadin.data.util.NestedPropertyDescriptor import (NestedPropertyDescriptor,)
from com.vaadin.data.util.AbstractInMemoryContainer import (AbstractInMemoryContainer,)
from com.vaadin.data.Container import (Filterable, PropertySetChangeNotifier, SimpleFilterable, Sortable,)
from com.vaadin.data.util.filter.SimpleStringFilter import (SimpleStringFilter,)
from com.vaadin.data.Property import (ValueChangeListener,)
from com.vaadin.data.util.BeanItem import (BeanItem,)
# from com.vaadin.data.Container.Filterable import (Filterable,)
# from com.vaadin.data.Container.PropertySetChangeNotifier import (PropertySetChangeNotifier,)
# from com.vaadin.data.Container.SimpleFilterable import (SimpleFilterable,)
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.data.Property.ValueChangeListener import (ValueChangeListener,)
# from com.vaadin.data.Property.ValueChangeNotifier import (ValueChangeNotifier,)
# from java.io.Serializable import (Serializable,)


class AbstractBeanContainer(AbstractInMemoryContainer, Filterable, SimpleFilterable, Sortable, ValueChangeListener, PropertySetChangeNotifier):
    """An abstract base class for in-memory containers for JavaBeans.

    <p>
    The properties of the container are determined automatically by introspecting
    the used JavaBean class and explicitly adding or removing properties is not
    supported. Only beans of the same type can be added to the container.
    </p>

    <p>
    Subclasses should implement any public methods adding items to the container,
    typically calling the protected methods {@link #addItem(Object, Object)},
    {@link #addItemAfter(Object, Object, Object)} and
    {@link #addItemAt(int, Object, Object)}.
    </p>

    @param <IDTYPE>
               The type of the item identifier
    @param <BEANTYPE>
               The type of the Bean

    @since 6.5
    """

    class BeanIdResolver(Serializable):
        """Resolver that maps beans to their (item) identifiers, removing the need
        to explicitly specify item identifiers when there is no need to customize
        this.

        Note that beans can also be added with an explicit id even if a resolver
        has been set.

        @param <IDTYPE>
        @param <BEANTYPE>

        @since 6.5
        """

        def getIdForBean(self, bean):
            """Return the item identifier for a bean.

            @param bean
            @return
            """
            pass

    class PropertyBasedBeanIdResolver(BeanIdResolver):
        """A item identifier resolver that returns the value of a bean property.

        The bean must have a getter for the property, and the getter must return
        an object of type IDTYPE.
        """
        # The resolver that finds the item ID for a bean, or null not to use
        # automatic resolving.
        # 
        # Methods that add a bean without specifying an ID must not be called if no
        # resolver has been set.

        _propertyId = None

        def __init__(self, propertyId):
            if propertyId is None:
                raise self.IllegalArgumentException('Property identifier must not be null')
            self._propertyId = propertyId

        def getIdForBean(self, bean):
            pd = self.model.get(self._propertyId)
            if None is pd:
                raise self.IllegalStateException('Property ' + self._propertyId + ' not found')
            try:
                property = pd.createProperty(bean)
                return property.getValue()
            except MethodException, e:
                raise self.IllegalArgumentException(e)

    _beanIdResolver = None
    # Maps all item ids in the container (including filtered) to their
    # corresponding BeanItem.

    _itemIdToItem = dict()
    # The type of the beans in the container.
    _type = None
    # A description of the properties found in beans of type {@link #type}.
    # Determines the property ids that are present in the container.

    _model = None

    def __init__(self, type):
        """Constructs a {@code AbstractBeanContainer} for beans of the given type.

        @param type
                   the type of the beans that will be added to the container.
        @throws IllegalArgumentException
                    If {@code type} is null
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#getType(java.lang.Object)

        if type is None:
            raise self.IllegalArgumentException('The bean type passed to AbstractBeanContainer must not be null')
        self._type = type
        self._model = BeanItem.getPropertyDescriptors(type)

    def getType(self, propertyId):
        return self._model.get(propertyId).getPropertyType()

    def createBeanItem(self, bean):
        """Create a BeanItem for a bean using pre-parsed bean metadata (based on
        {@link #getBeanType()}).

        @param bean
        @return created {@link BeanItem} or null if bean is null
        """
        return None if bean is None else BeanItem(bean, self._model)

    def getBeanType(self):
        """Returns the type of beans this Container can contain.

        This comes from the bean type constructor parameter, and bean metadata
        (including container properties) is based on this.

        @return
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#getContainerPropertyIds()

        return self._type

    def getContainerPropertyIds(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#removeAllItems()

        return self._model.keys()

    def removeAllItems(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#getItem(java.lang.Object)

        origSize = len(self)
        self.internalRemoveAllItems()
        # detach listeners from all Items
        for item in self._itemIdToItem.values():
            self.removeAllValueChangeListeners(item)
        self._itemIdToItem.clear()
        # fire event only if the visible view changed, regardless of whether
        # filtered out items were removed or not
        if origSize != 0:
            self.fireItemSetChange()
        return True

    def getItem(self, itemId):
        # TODO return only if visible?
        return self.getUnfilteredItem(itemId)

    def getUnfilteredItem(self, itemId):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#getItemIds()

        return self._itemIdToItem[itemId]

    def getItemIds(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#getContainerProperty(java.lang.Object,
        # java.lang.Object)

        return super(AbstractBeanContainer, self).getItemIds()

    def getContainerProperty(self, itemId, propertyId):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#removeItem(java.lang.Object)

        item = self.getItem(itemId)
        if item is None:
            return None
        return item.getItemProperty(propertyId)

    def removeItem(self, itemId):
        # TODO should also remove items that are filtered out
        origSize = len(self)
        item = self.getItem(itemId)
        position = self.indexOfId(itemId)
        if self.internalRemoveItem(itemId):
            # detach listeners from Item
            self.removeAllValueChangeListeners(item)
            # remove item
            self._itemIdToItem.remove(itemId)
            # fire event only if the visible view changed, regardless of
            # whether filtered out items were removed or not
            if len(self) != origSize:
                self.fireItemRemoved(position, itemId)
            return True
        else:
            return False

    def valueChange(self, event):
        """Re-filter the container when one of the monitored properties changes."""
        # if a property that is used in a filter is changed, refresh filtering
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.data.Container.Filterable#addContainerFilter(java.lang.Object,
        # java.lang.String, boolean, boolean)

        self.filterAll()

    def addContainerFilter(self, *args):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container.Filterable#removeAllContainerFilters()

        _0 = args
        _1 = len(args)
        if _1 == 1:
            filter, = _0
            self.addFilter(filter)
        elif _1 == 4:
            propertyId, filterString, ignoreCase, onlyMatchPrefix = _0
            # the filter instance created here is always valid for in-memory
            # containers
            try:
                self.addFilter(SimpleStringFilter(propertyId, filterString, ignoreCase, onlyMatchPrefix))
            except UnsupportedFilterException, e:
                pass # astStmt: [Stmt([]), None]
        else:
            raise ARGERROR(1, 4)

    def removeAllContainerFilters(self):
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.data.Container.Filterable#removeContainerFilters(java.lang
        # .Object)

        if not self.getFilters().isEmpty():
            for item in self._itemIdToItem.values():
                self.removeAllValueChangeListeners(item)
            self.removeAllFilters()

    def removeContainerFilters(self, propertyId):
        removedFilters = super(AbstractBeanContainer, self).removeFilters(propertyId)
        if not removedFilters.isEmpty():
            # stop listening to change events for the property
            for item in self._itemIdToItem.values():
                self.removeValueChangeListener(item, propertyId)

    def removeContainerFilter(self, filter):
        self.removeFilter(filter)

    def addValueChangeListener(self, item, propertyId):
        """Make this container listen to the given property provided it notifies
        when its value changes.

        @param item
                   The {@link Item} that contains the property
        @param propertyId
                   The id of the property
        """
        property = item.getItemProperty(propertyId)
        if isinstance(property, ValueChangeNotifier):
            # avoid multiple notifications for the same property if
            # multiple filters are in use
            notifier = property
            notifier.removeListener(self)
            notifier.addListener(self)

    def removeValueChangeListener(self, item, propertyId):
        """Remove this container as a listener for the given property.

        @param item
                   The {@link Item} that contains the property
        @param propertyId
                   The id of the property
        """
        property = item.getItemProperty(propertyId)
        if isinstance(property, ValueChangeNotifier):
            property.removeListener(self)

    def removeAllValueChangeListeners(self, item):
        """Remove this contains as a listener for all the properties in the given
        {@link Item}.

        @param item
                   The {@link Item} that contains the properties
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container.Sortable#getSortableContainerPropertyIds()

        for propertyId in item.getItemPropertyIds():
            self.removeValueChangeListener(item, propertyId)

    def getSortableContainerPropertyIds(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container.Sortable#sort(java.lang.Object[],
        # boolean[])

        return self.getSortablePropertyIds()

    def sort(self, propertyId, ascending):
        self.sortContainer(propertyId, ascending)

    def getItemSorter(self):
        return super(AbstractBeanContainer, self).getItemSorter()

    def setItemSorter(self, itemSorter):
        super(AbstractBeanContainer, self).setItemSorter(itemSorter)

    def registerNewItem(self, position, itemId, item):
        self._itemIdToItem.put(itemId, item)
        # add listeners to be able to update filtering on property
        # changes
        for filter in self.getFilters():
            for propertyId in self.getContainerPropertyIds():
                if filter.appliesToProperty(propertyId):
                    # addValueChangeListener avoids adding duplicates
                    self.addValueChangeListener(item, propertyId)

    def validateBean(self, bean):
        """Check that a bean can be added to the container (is of the correct type
        for the container).

        @param bean
        @return
        """
        return bean is not None and self.getBeanType().isAssignableFrom(bean.getClass())

    def addItem(self, itemId, bean):
        """Adds the bean to the Container.

        Note: the behavior of this method changed in Vaadin 6.6 - now items are
        added at the very end of the unfiltered container and not after the last
        visible item if filtering is used.

        @see com.vaadin.data.Container#addItem(Object)
        """
        if not self.validateBean(bean):
            return None
        return self.internalAddItemAtEnd(itemId, self.createBeanItem(bean), True)

    def addItemAfter(self, previousItemId, newItemId, bean):
        """Adds the bean after the given bean.

        @see com.vaadin.data.Container.Ordered#addItemAfter(Object, Object)
        """
        if not self.validateBean(bean):
            return None
        return self.internalAddItemAfter(previousItemId, newItemId, self.createBeanItem(bean), True)

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
        if not self.validateBean(bean):
            return None
        return self.internalAddItemAt(index, newItemId, self.createBeanItem(bean), True)

    def addBean(self, bean):
        """Adds a bean to the container using the bean item id resolver to find its
        identifier.

        A bean id resolver must be set before calling this method.

        @see #addItem(Object, Object)

        @param bean
                   the bean to add
        @return BeanItem<BEANTYPE> item added or null
        @throws IllegalStateException
                    if no bean identifier resolver has been set
        @throws IllegalArgumentException
                    if an identifier cannot be resolved for the bean
        """
        if bean is None:
            return None
        itemId = self.resolveBeanId(bean)
        if itemId is None:
            raise self.IllegalArgumentException('Resolved identifier for a bean must not be null')
        return self.addItem(itemId, bean)

    def addBeanAfter(self, previousItemId, bean):
        """Adds a bean to the container after a specified item identifier, using the
        bean item id resolver to find its identifier.

        A bean id resolver must be set before calling this method.

        @see #addItemAfter(Object, Object, Object)

        @param previousItemId
                   the identifier of the bean after which this bean should be
                   added, null to add to the beginning
        @param bean
                   the bean to add
        @return BeanItem<BEANTYPE> item added or null
        @throws IllegalStateException
                    if no bean identifier resolver has been set
        @throws IllegalArgumentException
                    if an identifier cannot be resolved for the bean
        """
        if bean is None:
            return None
        itemId = self.resolveBeanId(bean)
        if itemId is None:
            raise self.IllegalArgumentException('Resolved identifier for a bean must not be null')
        return self.addItemAfter(previousItemId, itemId, bean)

    def addBeanAt(self, index, bean):
        """Adds a bean at a specified (filtered view) position in the container
        using the bean item id resolver to find its identifier.

        A bean id resolver must be set before calling this method.

        @see #addItemAfter(Object, Object, Object)

        @param index
                   the index (in the filtered view) at which to add the item
        @param bean
                   the bean to add
        @return BeanItem<BEANTYPE> item added or null
        @throws IllegalStateException
                    if no bean identifier resolver has been set
        @throws IllegalArgumentException
                    if an identifier cannot be resolved for the bean
        """
        if bean is None:
            return None
        itemId = self.resolveBeanId(bean)
        if itemId is None:
            raise self.IllegalArgumentException('Resolved identifier for a bean must not be null')
        return self.addItemAt(index, itemId, bean)

    def addAll(self, collection):
        """Adds all the beans from a {@link Collection} in one operation using the
        bean item identifier resolver. More efficient than adding them one by
        one.

        A bean id resolver must be set before calling this method.

        Note: the behavior of this method changed in Vaadin 6.6 - now items are
        added at the very end of the unfiltered container and not after the last
        visible item if filtering is used.

        @param collection
                   The collection of beans to add. Must not be null.
        @throws IllegalStateException
                    if no bean identifier resolver has been set
        """
        modified = False
        for bean in collection:
            # TODO skipping invalid beans - should not allow them in javadoc?
            if (
                (bean is None) or (not self.getBeanType().isAssignableFrom(bean.getClass()))
            ):
                continue
            itemId = self.resolveBeanId(bean)
            if (
                self.internalAddItemAtEnd(itemId, self.createBeanItem(bean), False) is not None
            ):
                modified = True
        if modified:
            # Filter the contents when all items have been added
            if self.isFiltered():
                self.filterAll()
            else:
                self.fireItemSetChange()

    def resolveBeanId(self, bean):
        """Use the bean resolver to get the identifier for a bean.

        @param bean
        @return resolved bean identifier, null if could not be resolved
        @throws IllegalStateException
                    if no bean resolver is set
        """
        if self._beanIdResolver is None:
            raise self.IllegalStateException('Bean item identifier resolver is required.')
        return self._beanIdResolver.getIdForBean(bean)

    def setBeanIdResolver(self, beanIdResolver):
        """Sets the resolver that finds the item id for a bean, or null not to use
        automatic resolving.

        Methods that add a bean without specifying an id must not be called if no
        resolver has been set.

        Note that methods taking an explicit id can be used whether a resolver
        has been defined or not.

        @param beanIdResolver
                   to use or null to disable automatic id resolution
        """
        self._beanIdResolver = beanIdResolver

    def getBeanIdResolver(self):
        """Returns the resolver that finds the item ID for a bean.

        @return resolver used or null if automatic item id resolving is disabled
        """
        return self._beanIdResolver

    def createBeanPropertyResolver(self, propertyId):
        """Create an item identifier resolver using a named bean property.

        @param propertyId
                   property identifier, which must map to a getter in BEANTYPE
        @return created resolver
        """
        return self.PropertyBasedBeanIdResolver(propertyId)

    def addListener(self, listener):
        super(AbstractBeanContainer, self).addListener(listener)

    def removeListener(self, listener):
        super(AbstractBeanContainer, self).removeListener(listener)

    def addContainerProperty(self, *args):
        """None
        ---
        Adds a property for the container and all its items.

        Primarily for internal use, may change in future versions.

        @param propertyId
        @param propertyDescriptor
        @return true if the property was added
        """
        _0 = args
        _1 = len(args)
        if _1 == 2:
            propertyId, propertyDescriptor = _0
            if (None is propertyId) or (None is propertyDescriptor):
                return False
            # Fails if the Property is already present
            if propertyId in self._model:
                return False
            self._model.put(propertyId, propertyDescriptor)
            for item in self._itemIdToItem.values():
                item.addItemProperty(propertyId, propertyDescriptor.createProperty(item.getBean()))
            # Sends a change event
            self.fireContainerPropertySetChange()
            return True
        elif _1 == 3:
            propertyId, type, defaultValue = _0
            raise self.UnsupportedOperationException('Use addNestedContainerProperty(String) to add container properties to a ' + self.getClass().getSimpleName())
        else:
            raise ARGERROR(2, 3)

    def addNestedContainerProperty(self, propertyId):
        """Adds a nested container property for the container, e.g.
        "manager.address.street".

        All intermediate getters must exist and must return non-null values when
        the property value is accessed.

        @see NestedMethodProperty

        @param propertyId
        @param propertyType
        @return true if the property was added
        """
        return self.addContainerProperty(propertyId, NestedPropertyDescriptor(propertyId, self._type))

    def removeContainerProperty(self, propertyId):
        # Fails if the Property is not present
        if not (propertyId in self._model):
            return False
        # Removes the Property to Property list and types
        self._model.remove(propertyId)
        # If remove the Property from all Items
        _0 = True
        i = self.getAllItemIds()
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            self.getUnfilteredItem(i.next()).removeItemProperty(propertyId)
        # Sends a change event
        self.fireContainerPropertySetChange()
        return True
