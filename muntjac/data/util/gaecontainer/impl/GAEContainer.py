# Copyright (C) 2010 Abo Akademi University
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
#
# Note: This is a modified file from GAEContainer. For further information
#       please visit http://vaadin.com/directory#addon/gaecontainer.

from __pyjamas__ import (ARGERROR,)
from muntjac.data.util.gaecontainer.impl.CachingProviderImpl import (CachingProviderImpl,)
from muntjac.data.util.gaecontainer.Cache.Cache import (Cache,)
from muntjac.data.util.gaecontainer.QueryRepresentation import (QueryRepresentation,)
from muntjac.data.util.gaecontainer.VersionedGAEItem import (VersionedGAEItem,)
from muntjac.data.util.gaecontainer.Query.QueryableContainer import (QueryableContainer,)
# from com.google.appengine.api.datastore.Blob import (Blob,)
# from com.google.appengine.api.datastore.Entity import (Entity,)
# from com.google.appengine.api.datastore.Key import (Key,)
# from com.google.appengine.api.datastore.KeyFactory import (KeyFactory,)
# from com.google.appengine.api.datastore.Query.FilterOperator import (FilterOperator,)
# from com.vaadin.data.Container import (Container,)
# from com.vaadin.data.Item import (Item,)
# from com.vaadin.data.Property import (Property,)
# from java.io.ByteArrayInputStream import (ByteArrayInputStream,)
# from java.io.ByteArrayOutputStream import (ByteArrayOutputStream,)
# from java.io.IOException import (IOException,)
# from java.io.ObjectInputStream import (ObjectInputStream,)
# from java.io.ObjectOutput import (ObjectOutput,)
# from java.io.ObjectOutputStream import (ObjectOutputStream,)
# from java.io.Serializable import (Serializable,)
# from java.lang.reflect.Constructor import (Constructor,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.Collections import (Collections,)
# from java.util.ConcurrentModificationException import (ConcurrentModificationException,)
# from java.util.Date import (Date,)
# from java.util.EventObject import (EventObject,)
# from java.util.Hashtable import (Hashtable,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.List import (List,)
# from java.util.NoSuchElementException import (NoSuchElementException,)
# from java.util.logging.Logger import (Logger,)


class GAEContainer(Container.Sortable, Container.Indexed, Container.PropertySetChangeNotifier, Container.ItemSetChangeNotifier, QueryableContainer):
    """Container for Google App Engine that supports optimistic locking, caching and querying

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """
    _serialVersionUID = 1L
    log = Logger.getLogger('VersionedContainer')
    # States which kind of entities we are working with in the datastore
    _kind = None
    # Provider for talking to the datastore and caches
    _cachingProvider = None
    # Map of propertyId, default value pair
    _propertyDefaultValues = dict()
    # Map of propertyId, Class pair
    _propertyTypes = dict()
    # States which properties are eligible for sorting
    _sortableProperties = list()
    # Current sort criteria set by the sort method
    _currentSort = None
    _propertyValueChangeListeners = None
    _itemSetChangeListeners = None
    # Should properties be written immediately.
    _propertyWriteTrough = None
    # Is optimistic locking beeing used
    _versioned = None

    def __init__(self, *args):
        """Creates a {@link GAEContainer} with property write trough, no optimistic locking and no caching.
        @param kind The kind of items this container handles.
        ---
        Creates a {@link GAEContainer} with custom settings.
        {@link Cache} can be created with {@link CacheFactory}.
        Caches from the left are higher up in the hiearchy.

        @param kind The kind of items this container handles.
        @param propertyWriteTrough If true write values immediately else manual {@link VersionedGAEItem#commit()} is needed.
        @param versioned If true use optimistic locking.
        @param Cache List of caches to use.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            kind, = _0
            self.__init__(kind, True, False)
        elif _1 == 4:
            kind, propertyWriteTrough, versioned, Cache = _0
            self._propertyWriteTrough = propertyWriteTrough
            self._kind = kind
            self._currentSort = QueryRepresentation(kind)
            self._versioned = versioned
            self._cachingProvider = CachingProviderImpl()
            for cache in Cache:
                self._cachingProvider.addCache(cache)
        else:
            raise ARGERROR(1, 4)

    def addContainerProperty(self, propertyId, type, defaultValue):
        if ((propertyId is None) or (type is None)) or (defaultValue is None):
            self.log.warning('addContainerProperty was called with null parameter')
            return False
        self._propertyTypes.put(propertyId, type)
        self._propertyDefaultValues.put(propertyId, defaultValue)
        if self.isCoreValue(type):
            # check if datastore supports sorting for the
            # given type
            self._sortableProperties.add(propertyId)
        return True

    def addItem(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            entity = Entity(self._kind)
            for property in self._propertyDefaultValues.keys():
                # properties must exist in datastore to enable sorting
                entity.setProperty(str(property), None)
            key = self._cachingProvider.addEntity(entity)
            if key is None:
                return None
            return key.getId()
        elif _1 == 1:
            itemId, = _0
            raise self.UnsupportedOperationException()
        else:
            raise ARGERROR(0, 1)

    def containsId(self, itemId):
        if itemId is None:
            self.log.warning('containsId was called with null parameter')
            return False
        itemIdAsLong = -1
        # todo try to convert string to long also
        try:
            itemIdAsLong = itemId
        except self.ClassCastException, c:
            return False
            # should maybe throw some informative exception
        key = KeyFactory.createKey(self._kind, itemIdAsLong)
        return self._cachingProvider.containsEntity(key)

    def getContainerProperty(self, itemId, propertyId):
        if (itemId is None) or (propertyId is None):
            self.log.warning('getContainerProperty was called with null parameter')
            return None
        entity = self._cachingProvider.getEntity(KeyFactory.createKey(self._kind, itemId))
        if (entity is None) or (not (propertyId in self._propertyDefaultValues)):
            return None
        gaeProperty = self.createProperty(entity, itemId, str(propertyId), True)
        return gaeProperty

    def getContainerPropertyIds(self):
        return Collections.unmodifiableCollection(self._propertyTypes.keys())

    def getItem(self, itemId):
        if itemId is None:
            self.log.warning('getItem was called with null parameter')
            return None
        entity = self._cachingProvider.getEntity(KeyFactory.createKey(self._kind, itemId))
        if entity is None:
            return None
        return self.createItem(entity)

    def createItem(self, entity):
        # add a property to the given entity using datastore value if set
        properties = LinkedList()
        for key in self._propertyDefaultValues.keys():
            properties.add(self.createProperty(entity, entity.getKey().getId(), str(key), self._propertyWriteTrough))
        versionProperty = entity.getProperty('version')
        if versionProperty is not None:
            return self.GAEItem(entity.getKey().getId(), properties, versionProperty)
        else:
            return self.GAEItem(entity.getKey().getId(), properties, -1)

    def createProperty(self, entity, itemId, propertyId, writeThrough):
        value = entity.getProperty(str(propertyId))
        if Blob.isInstance(value):
            value = self.deserializeFromBlob(value)
        elif value is None:
            # property was not set, use default value
            value = self._propertyDefaultValues[propertyId]
        type = self._propertyTypes[propertyId]
        versionProperty = entity.getProperty('version')
        if versionProperty is not None:
            return self.GAEproperty(value, type, itemId, propertyId, versionProperty, writeThrough)
        else:
            return self.GAEproperty(value, type, itemId, propertyId, -1, writeThrough)

    def getItemIds(self):
        # return Collections.unmodifiableCollection(itemIds);
        raise self.UnsupportedOperationException()

    def getType(self, propertyId):
        if propertyId is None:
            self.log.warning('getType was called with null parameter')
            return None
        return self._propertyTypes[propertyId]

    def removeAllItems(self):
        raise self.UnsupportedOperationException()

    def removeContainerProperty(self, propertyId):
        raise self.UnsupportedOperationException()

    def removeItem(self, itemId):
        if itemId is None:
            self.log.warning('removeItem was called with null parameter')
            return False
        return self._cachingProvider.removeEntity(KeyFactory.createKey(self._kind, itemId))

    def size(self):
        return len(self._currentSort)

    def firePropertyValueChange(self, source):
        # todo add error handling
        entity = Entity(KeyFactory.createKey(self._kind, source.getItemId()))
        if self.isCoreValue(source.getType()):
            # if core value set it directly
            entity.setProperty(str(source.getId()), source.getValue())
        else:
            # otherwise store it as a blob
            blob = self.serializeToBlob(source.getValue())
            entity.setProperty(str(source.getId()), blob)
        if self._versioned:
            entity.setProperty('version', source.getVersion())
        self._cachingProvider.updateProperty(entity, self._versioned)
        # Sends event to listeners listening all value changes
        if self._propertyValueChangeListeners is not None:
            l = list(self._propertyValueChangeListeners)
            event = GAEContainer.PropertyValueChangeEvent(source)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(l)):
                    break
                l[i].valueChange(event)

    class PropertyValueChangeEvent(EventObject, Property.ValueChangeEvent, Serializable):

        def __init__(self, source):
            super(PropertyValueChangeEvent, self)(source)

        def getProperty(self):
            return self.getSource()

    def GAEproperty(GAEContainer_this, *args, **kwargs):

        class GAEproperty(Property):
            _value = None
            _type = None
            _isReadOnly = False
            _id = None
            _itemId = None
            _version = None
            _writeThrough = True

            def __init__(self, *args):
                _0 = args
                _1 = len(args)
                if _1 == 5:
                    value, c, ownerItemid, id, version = _0
                    self.__init__(value, c, ownerItemid, id, version, True)
                elif _1 == 6:
                    value, c, ownerItemid, id, version, writeTrough = _0
                    self._value = value
                    self._type = c
                    self._id = id
                    self._itemId = ownerItemid
                    self._version = version
                    self._writeThrough = writeTrough
                else:
                    raise ARGERROR(5, 6)

            def getType(self):
                return self._type

            def getValue(self):
                return self._value

            def isReadOnly(self):
                return self._isReadOnly

            def setReadOnly(self, newStatus):
                if newStatus != self._isReadOnly:
                    self._isReadOnly = newStatus
                    # tell the container

            def setValue(self, newValue):
                if self.isReadOnly():
                    raise self.ReadOnlyException()
                if (newValue is None) or self._type.isAssignableFrom(newValue.getClass()):
                    self._value = newValue
                else:
                    try:
                        constructor = self.getType().getConstructor([str])
                        self._value = constructor([str(newValue)])
                    except java.lang.Exception, e:
                        raise Property.ConversionException('Conversion for value \'' + newValue + '\' of class ' + newValue.getClass().getName() + ' to ' + self.getType().getName() + ' failed')
                if self._writeThrough:
                    GAEContainer_this.firePropertyValueChange(self)

            def getId(self):
                return self._id

            def getItemId(self):
                return self._itemId

            def getVersion(self):
                return self._version

            def toString(self):
                value = self.getValue()
                if value is None:
                    return None
                return str(value)

        return GAEproperty(*args, **kwargs)

    def GAEItem(GAEContainer_this, *args, **kwargs):

        class GAEItem(VersionedGAEItem):
            _itemProperties = dict()
            _version = None
            _itemId = None

            def __init__(self, itemId, itemProperties, version):
                for property in itemProperties:
                    self._itemProperties.put(property.getId(), property)
                self._version = version
                self._itemId = itemId

            def addItemProperty(self, id, property):
                raise self.UnsupportedOperationException()

            def getItemProperty(self, id):
                return self._itemProperties[id]

            def getItemPropertyIds(self):
                return Collections.unmodifiableCollection(self._itemProperties.keys())

            def removeItemProperty(self, id):
                raise self.UnsupportedOperationException()

            def commit(self):
                GAEContainer_this.commitItem(self)

            def getVersion(self):
                return self._version

            def getId(self):
                return self._itemId

            def isWriteThrough(self):
                return GAEContainer_this._propertyWriteTrough

        return GAEItem(*args, **kwargs)

    def commitItem(self, item):
        propertyIds = item.getItemPropertyIds()
        entity = Entity(KeyFactory.createKey(self._kind, item.getId()))
        for id in propertyIds:
            property = item.getItemProperty(id)
            if self._propertyDefaultValues[id] == property.getValue():
                # do not store default values in the database
                entity.setProperty(str(property.getId()), None)
            elif self.isCoreValue(property.getType()):
                # if core value set it
                # directly
                entity.setProperty(str(property.getId()), property.getValue())
            else:
                # otherwise store it as a blob
                blob = self.serializeToBlob(property.getValue())
                entity.setProperty(str(property.getId()), blob)
        if self._versioned:
            entity.setUnindexedProperty('version', item.getVersion())
        self._cachingProvider.updateEntity(entity, self._versioned)

    def addListener(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], self.ItemSetChangeListener):
                listener, = _0
                if self._itemSetChangeListeners is None:
                    self._itemSetChangeListeners = list()
                self._itemSetChangeListeners.add(listener)
            else:
                listener, = _0
                if self._propertyValueChangeListeners is None:
                    self._propertyValueChangeListeners = list()
                self._propertyValueChangeListeners.add(listener)
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        # given a Object return a Blob containing the serialized Object or null if
        # failed

        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], self.ItemSetChangeListener):
                listener, = _0
                if self._itemSetChangeListeners is not None:
                    self._itemSetChangeListeners.remove(listener)
            else:
                listener, = _0
                if self._propertyValueChangeListeners is not None:
                    self._propertyValueChangeListeners.remove(listener)
        else:
            raise ARGERROR(1, 1)

    def serializeToBlob(self, object):
        # given a Blob return a deserialized Object or null if failed
        try:
            bos = ByteArrayOutputStream()
            out = ObjectOutputStream(bos)
            out.writeObject(object)
            out.close()
            buf = bos.toByteArray()
            return Blob(buf)
        except IOException, e:
            e.printStackTrace()
            return None

    def deserializeFromBlob(self, blob):
        # check if a type is a datastore core value
        try:
            bytes = blob.getBytes()
            in_ = ObjectInputStream(ByteArrayInputStream(bytes))
            object = in_.readObject()
            in_.close()
            return object
        except IOException, e:
            e.printStackTrace()
            return None
        except self.ClassNotFoundException, e:
            e.printStackTrace()
            return None

    def isCoreValue(self, type):
        if (
            (((((((((str == type) or (bool == type)) or (int == type)) or (int == type)) or (int == type)) or (long == type)) or (float == type)) or (float == type)) or (Date == type)) or (type == java.util.List)
        ):
            return True
        return False

    def addItemAfter(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            previousItemId, = _0
            raise self.UnsupportedOperationException()
        elif _1 == 2:
            previousItemId, newItemId = _0
            raise self.UnsupportedOperationException()
        else:
            raise ARGERROR(1, 2)

    def firstItemId(self):
        key = self._cachingProvider.getKeyByIndexFromStart(self._currentSort, 0)
        if key is not None:
            return key.getId()
        return None

    def isFirstId(self, itemId):
        if itemId is None:
            self.log.warning('isFirstId was called with null parameter')
            return False
        return itemId == self.firstItemId()

    def isLastId(self, itemId):
        if itemId is None:
            self.log.warning('isLastId was called with null parameter')
            return False
        return itemId == self.lastItemId()

    def lastItemId(self):
        key = self._cachingProvider.getKeyByIndexFromEnd(self._currentSort, 0)
        if key is not None:
            return key.getId()
        return None

    def nextItemId(self, itemId):
        if itemId is None:
            self.log.warning('nextItemId was called with null parameter')
            return None
        key = KeyFactory.createKey(self._kind, itemId)
        nextKey = self._cachingProvider.getNextKey(key, self._currentSort)
        if nextKey is not None:
            return nextKey.getId()
        return None

    def prevItemId(self, itemId):
        if itemId is None:
            self.log.warning('prevItemId was called with null parameter')
            return None
        key = KeyFactory.createKey(self._kind, itemId)
        prevKey = self._cachingProvider.getPreviousKey(key, self._currentSort)
        if prevKey is not None:
            return prevKey.getId()
        return None

    def getSortableContainerPropertyIds(self):
        return Collections.unmodifiableCollection(self._sortableProperties)

    def sort(self, propertyId, ascending):
        if (propertyId is None) or (ascending is None):
            self.log.warning('sort was called with null parameter')
            return
        if len(propertyId) != len(ascending):
            raise self.IllegalArgumentException('parameters must be of same length')
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(propertyId)):
                break
            if not self._sortableProperties.contains(propertyId[i]):
                raise self.IllegalArgumentException(str(propertyId[i]) + ' is not a sortable property')
        self._currentSort.sort(propertyId, ascending)

    def addItemAt(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            index, = _0
            raise self.UnsupportedOperationException()
        elif _1 == 2:
            index, newItemId = _0
            raise self.UnsupportedOperationException()
        else:
            raise ARGERROR(1, 2)

    def getIdByIndex(self, index):
        if index < 0:
            self.log.warning('getIdByIndex was called with negative parameter')
            return None
        key = self._cachingProvider.getKeyByIndexFromStart(self._currentSort, index)
        if key is not None:
            return key.getId()
        return None

    def indexOfId(self, itemId):
        self.log.warning('using indexOfId is very slow and should be avoided')
        if itemId is None:
            self.log.warning('indexOfId was called with null parameter')
            return -1
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self)):
                break
            key = self._cachingProvider.getKeyByIndexFromStart(self._currentSort, i)
            if key is not None and itemId == key.getId():
                return i
        return -1

    def addFilter(self, propertyId, filter, value):
        if ((propertyId is None) or (filter is None)) or (value is None):
            raise self.IllegalArgumentException('parameters must not be null')
        if propertyId == '__key__':
            value = KeyFactory.createKey(self._kind, value)
        if not self._sortableProperties.contains(propertyId):
            raise self.IllegalArgumentException(str(propertyId) + ' is not a sortable property')
        if (
            not (self._propertyTypes[propertyId] == value.getClass()) and self._propertyTypes[propertyId] != java.util.List
        ):
            raise self.IllegalArgumentException(str(propertyId) + ' is not of type: ' + self._propertyTypes[propertyId].getName())
        self._currentSort.addFilter(propertyId, filter, value)
        self.fireItemChange()

    def query(self, amount):
        if amount > 1000:
            raise self.IllegalArgumentException('amount cannot exceed 1000')
        if amount <= 0:
            raise self.IllegalArgumentException('amount must exceed 0')
        entities = self._cachingProvider.query(self._currentSort, amount)
        if (entities is None) or (len(entities) == 0):
            return None
        items = LinkedList()
        for entity in entities:
            items.add(self.createItem(entity))
        return items

    def removeFilters(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            for propertyId in self._sortableProperties:
                self.removeFilters(propertyId)
            self.fireItemChange()
        elif _1 == 1:
            propertyId, = _0
            self._currentSort.removeFilters(propertyId)
            self.fireItemChange()
        else:
            raise ARGERROR(0, 1)

    def fireItemChange(self):
        # Sends event to listeners listening all value changes
        if self._propertyValueChangeListeners is not None:
            l = list(self._propertyValueChangeListeners)
            event = GAEContainer.ItemSetChangeEvent(self)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(l)):
                    break
                l[i].containerItemSetChange(event)

    class ItemSetChangeEvent(EventObject, Container.ItemSetChangeEvent, Serializable):
        _source = None

        def __init__(self, source):
            super(ItemSetChangeEvent, self)(source)

        def getContainer(self):
            return self._source
