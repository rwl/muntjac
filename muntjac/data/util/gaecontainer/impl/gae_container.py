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

import logging

from muntjac.data.container import IItemSetChangeEvent

from muntjac.util \
    import EventObject

from muntjac.data.util.indexed_container \
    import ItemSetChangeEvent

from muntjac.data.property \
    import ValueChangeEvent as PropertyValueChangeEvent, IProperty

from muntjac.data.container \
    import ISortable, IIndexed, IPropertySetChangeNotifier, \
    IItemSetChangeNotifier

from muntjac.data.util.gaecontainer.impl.caching_provider_impl \
    import CachingProviderImpl

from muntjac.data.util.gaecontainer.query_representation \
    import QueryRepresentation

from muntjac.data.util.gaecontainer.query.queryable_container \
    import IQueryableContainer

from muntjac.data.util.gaecontainer.cache.cache import ICache
from muntjac.data.util.gaecontainer.versioned_gae_item import IVersionedGAEItem


logger = logging.getLogger(__name__)


class GAEContainer(ISortable, IIndexed, IPropertySetChangeNotifier,
            IItemSetChangeNotifier, IQueryableContainer):
    """Container for Google App Engine that supports optimistic locking, caching and querying

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def __init__(self, kind, propertyWriteTrough=True, versioned=False, *cache):
        """Creates a L{GAEContainer} with custom settings. L{Cache} can be
        created with L{CacheFactory}.

        Caches from the left are higher up in the hiearchy.

        @param kind: The kind of items this container handles.
        @param propertyWriteTrough: If true write values immediately else
        manual L{VersionedGAEItem.commit} is needed.
        @param versioned: If true use optimistic locking.
        @param cache: List of caches to use.
        """
        # States which kind of entities we are working with in the datastore
        self._kind = kind

        # Provider for talking to the datastore and caches
        self._cachingProvider = CachingProviderImpl()

        # Map of propertyId, default value pair
        self._propertyDefaultValues = dict()

        # Map of propertyId, Class pair
        self._propertyTypes = dict()

        # States which properties are eligible for sorting
        self._sortableProperties = list()

        # Current sort criteria set by the sort method
        self._currentSort = QueryRepresentation(kind)

        self._propertyValueChangeListeners = None
        self._itemSetChangeListeners = None

        # Should properties be written immediately.
        self._propertyWriteTrough = propertyWriteTrough

        # Is optimistic locking beeing used
        self._versioned = versioned

        for c in cache:
            self._cachingProvider.addCache(c)


    def addContainerProperty(self, propertyId, type, defaultValue):

        if propertyId is None or type is None or defaultValue is None:
            logger.warning('addContainerProperty was called with null parameter')
            return False

        self._propertyTypes[propertyId] = type
        self._propertyDefaultValues[propertyId] = defaultValue

        # check if datastore supports sorting for the given type
        if self.isCoreValue(type):
            self._sortableProperties.add(propertyId)

        return True


    def addItem(self, entity=None):
        if entity is None:
            entity = Entity(self._kind)
            for prop in self._propertyDefaultValues.keys():
                # properties must exist in datastore to enable sorting
                entity.setProperty(str(prop), None)
            key = self._cachingProvider.addEntity(entity)
            if key is None:
                return None
            return key.getId()
        else:
            raise NotImplementedError


    def containsId(self, itemId):
        if itemId is None:
            logger.warning('containsId was called with null parameter')
            return False

        itemIdAsLong = -1
        try:
            itemIdAsLong = long(itemId)
        except ClassCastException:
            # TODO: try to convert string to long also
            return False  # should maybe throw some informative exception

        key = KeyFactory.createKey(self._kind, itemIdAsLong)
        return self._cachingProvider.containsEntity(key)


    def getContainerProperty(self, itemId, propertyId):
        if (itemId is None) or (propertyId is None):
            logger.warning('getContainerProperty was called with null parameter')
            return None

        entity = self._cachingProvider.getEntity(
                KeyFactory.createKey(self._kind, itemId))

        if (entity is None) or (propertyId not in self._propertyDefaultValues):
            return None

        gaeProperty = self.createProperty(entity, itemId, str(propertyId), True)

        return gaeProperty


    def getContainerPropertyIds(self):
        return list(self._propertyTypes.keys())


    def getItem(self, itemId):
        if itemId is None:
            logger.warning('getItem was called with null parameter')
            return None

        entity = self._cachingProvider.getEntity(
                KeyFactory.createKey(self._kind, itemId))

        if entity is None:
            return None

        return self.createItem(entity)


    def createItem(self, entity):
        properties = list()
        for key in self._propertyDefaultValues:
            properties.add(self.createProperty(entity, entity.getKey().getId(),
                    str(key), self._propertyWriteTrough))

        versionProperty = entity.getProperty('version')
        if versionProperty is not None:
            return self.GAEItem(entity.getKey().getId(),
                    properties, versionProperty)
        else:
            return self.GAEItem(entity.getKey().getId(),
                    properties, -1)


    def createProperty(self, entity, itemId, propertyId, writeThrough):
        # add a property to the given entity using datastore value if set
        value = entity.getProperty(str(propertyId))
        if isinstance(value, Blob):
            value = self.deserializeFromBlob(value)
        elif value is None:  # property was not set, use default value
            value = self._propertyDefaultValues.get(propertyId)

        typ = self._propertyTypes[propertyId]
        versionProperty = entity.getProperty('version')
        if versionProperty is not None:
            return GAEproperty(value, typ, itemId, propertyId,
                    versionProperty, writeThrough)
        else:
            return GAEproperty(value, typ, itemId, propertyId,
                    -1, writeThrough)


    def getItemIds(self):
        # return list(itemIds);
        raise NotImplementedError


    def getType(self, propertyId):
        if propertyId is None:
            logger.warning('getType was called with null parameter')
            return None
        return self._propertyTypes.get(propertyId)


    def removeAllItems(self):
        raise NotImplementedError


    def removeContainerProperty(self, propertyId):
        raise NotImplementedError


    def removeItem(self, itemId):
        if itemId is None:
            logger.warning('removeItem was called with null parameter')
            return False
        return self._cachingProvider.removeEntity(
                KeyFactory.createKey(self._kind, itemId))


    def size(self):
        return len(self._currentSort)


    def __len__(self):
        return self.size()


    def firePropertyValueChange(self, source):
        # todo add error handling
        entity = Entity(KeyFactory.createKey(self._kind, source.getItemId()))

        if self.isCoreValue(source.getType()):  # if core value set it directly
            entity.setProperty(str(source.getId()), source.getValue())
        else:  # otherwise store it as a blob
            blob = self.serializeToBlob(source.getValue())
            entity.setProperty(str(source.getId()), blob)

        if self._versioned:
            entity.setProperty('version', source.getVersion())

        self._cachingProvider.updateProperty(entity, self._versioned)

        # Sends event to listeners listening all value changes
        if self._propertyValueChangeListeners is not None:
            l = list(self._propertyValueChangeListeners)
            event = PropertyValueChangeEvent(source)
            for i in range(len(l)):
                l[i].valueChange(event)


    def commitItem(self, item):
        propertyIds = item.getItemPropertyIds()
        entity = Entity(KeyFactory.createKey(self._kind, item.getId()))
        for id in propertyIds:
            prop = item.getItemProperty(id)
            if self._propertyDefaultValues[id] == prop.getValue():
                # do not store default values in the database
                entity.setProperty(str(prop.getId()), None)
            else:
                if self.isCoreValue(prop.getType()):
                    # if core value set it
                    # directly
                    entity.setProperty(str(prop.getId()), prop.getValue())
                else:
                    # otherwise store it as a blob
                    blob = self.serializeToBlob(prop.getValue())
                    entity.setProperty(str(prop.getId()), blob)

        if self._versioned:
            entity.setUnindexedProperty('version', item.getVersion())

        self._cachingProvider.updateEntity(entity, self._versioned)


    def addListener(self, listener):
        if isinstance(listener, self.ItemSetChangeListener):
            if self._itemSetChangeListeners is None:
                self._itemSetChangeListeners = list()
            self._itemSetChangeListeners.add(listener)
        else:
            if self._propertyValueChangeListeners is None:
                self._propertyValueChangeListeners = list()
            self._propertyValueChangeListeners.add(listener)


    def removeListener(self, listener):
        if isinstance(listener, self.ItemSetChangeListener):
            if self._itemSetChangeListeners is not None:
                self._itemSetChangeListeners.remove(listener)
        else:
            if self._propertyValueChangeListeners is not None:
                self._propertyValueChangeListeners.remove(listener)


    def serializeToBlob(self, obj):
        # given a Object return a Blob containing the serialized Object or null if
        # failed
        try:
            bos = ByteArrayOutputStream()
            out = ObjectOutputStream(bos)
            out.writeObject(obj)
            out.close()
            buf = bos.toByteArray()
            return Blob(buf)
        except IOError, e:
            e.printStackTrace()
            return None


    def deserializeFromBlob(self, blob):
        # given a Blob return a deserialized Object or null if failed
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
        # check if a type is a datastore core value
        if ((str == type) or (bool == type) or (int == type)
                or (int == type) or (int == type) or (long == type)
                or (float == type) or (float == type) or (Date == type)
                or (type == list)):
            return True
        return False


    def addItemAfter(self, previousItemId, newItemId=None):
        raise NotImplementedError


    def firstItemId(self):
        key = self._cachingProvider.getKeyByIndexFromStart(self._currentSort, 0)
        if key is not None:
            return key.getId()
        return None


    def isFirstId(self, itemId):
        if itemId is None:
            logger.warning('isFirstId was called with null parameter')
            return False
        return itemId == self.firstItemId()


    def isLastId(self, itemId):
        if itemId is None:
            logger.warning('isLastId was called with null parameter')
            return False
        return itemId == self.lastItemId()


    def lastItemId(self):
        key = self._cachingProvider.getKeyByIndexFromEnd(self._currentSort, 0)
        if key is not None:
            return key.getId()
        return None


    def nextItemId(self, itemId):
        if itemId is None:
            logger.warning('nextItemId was called with null parameter')
            return None

        key = KeyFactory.createKey(self._kind, itemId)
        nextKey = self._cachingProvider.getNextKey(key, self._currentSort)
        if nextKey is not None:
            return nextKey.getId()

        return None


    def prevItemId(self, itemId):
        if itemId is None:
            logger.warning('prevItemId was called with null parameter')
            return None

        key = KeyFactory.createKey(self._kind, itemId)
        prevKey = self._cachingProvider.getPreviousKey(key, self._currentSort)
        if prevKey is not None:
            return prevKey.getId()

        return None


    def getSortableContainerPropertyIds(self):
        return list(self._sortableProperties)


    def sort(self, propertyId, ascending):
        if (propertyId is None) or (ascending is None):
            logger.warning('sort was called with null parameter')
            return

        if len(propertyId) != len(ascending):
            raise ValueError('parameters must be of same length')

        for i in range(len(propertyId)):
            if propertyId[i] not in self._sortableProperties:
                raise ValueError(str(propertyId[i])
                        + ' is not a sortable property')
        self._currentSort.sort(propertyId, ascending)


    def addItemAt(self, index, newItemId=None):
        raise NotImplementedError


    def getIdByIndex(self, index):
        if index < 0:
            logger.warning('getIdByIndex was called with negative parameter')
            return None

        key = self._cachingProvider.getKeyByIndexFromStart(self._currentSort,
                index)

        if key is not None:
            return key.getId()

        return None


    def indexOfId(self, itemId):
        logger.warning('using indexOfId is very slow and should be avoided')
        if itemId is None:
            logger.warning('indexOfId was called with null parameter')
            return -1

        for i in range(len(self.size())):
            key = self._cachingProvider.getKeyByIndexFromStart(
                    self._currentSort, i)
            if key is not None and itemId == key.getId():
                return i

        return -1


    def addFilter(self, propertyId, fltr, value):
        if ((propertyId is None) or (fltr is None)) or (value is None):
            raise ValueError('parameters must not be null')

        if propertyId == '__key__':
            value = KeyFactory.createKey(self._kind, value)

        if not self._sortableProperties.contains(propertyId):
            raise ValueError(str(propertyId) + ' is not a sortable property')

        if ((self._propertyTypes[propertyId] != value.__class__)
                and self._propertyTypes.get(propertyId) != list):
            raise ValueError(str(propertyId) + ' is not of type: '
                    + self._propertyTypes[propertyId].getName())

        self._currentSort.addFilter(propertyId, fltr, value)
        self.fireItemChange()


    def query(self, amount):
        if amount > 1000:
            raise ValueError('amount cannot exceed 1000')

        if amount <= 0:
            raise ValueError('amount must exceed 0')

        entities = self._cachingProvider.query(self._currentSort, amount)
        if (entities is None) or (len(entities) == 0):
            return None

        items = list()
        for entity in entities:
            items.add(self.createItem(entity))

        return items


    def removeFilters(self, propertyId=None):
        if propertyId is None:
            for propertyId in self._sortableProperties:
                self.removeFilters(propertyId)
            self.fireItemChange()
        else:
            self._currentSort.removeFilters(propertyId)
            self.fireItemChange()


    def fireItemChange(self):
        # Sends event to listeners listening all value changes
        if self._propertyValueChangeListeners is not None:
            l = list(self._propertyValueChangeListeners)

            event = ItemSetChangeEvent(self)
            for i in range(len(l)):
                l[i].containerItemSetChange(event)


class PropertyValueChangeEvent(EventObject, PropertyValueChangeEvent):

    def __init__(self, source):
        super(PropertyValueChangeEvent, self).__init__(source)


    def getProperty(self):
        return self.getSource()



class GAEProperty(IProperty):

    def __init__(self, value, c, ownerItemid, Id, version, writeTrough=True):
        self._isReadOnly = False

        self._value = value
        self._type = c
        self._id = Id
        self._itemId = ownerItemid
        self._version = version
        self._writeThrough = writeTrough


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
            raise ReadOnlyException()

        if (newValue is None) or issubclass(newValue.__class__, self._type):
            self._value = newValue
        else:
            try:
                constructor = self.getType()
                self._value = constructor([str(newValue)])
            except Exception:
                raise property.ConversionException('Conversion for value \''
                        + newValue + '\' of class '
                        + newValue.__class__.__name__ + ' to '
                        + self.getType().__name__ + ' failed')

        if self._writeThrough:
            GAEContainer_this.firePropertyValueChange(self)


    def getId(self):
        return self._id


    def getItemId(self):
        return self._itemId


    def getVersion(self):
        return self._version


    def __str__(self):
        value = self.getValue()
        if value is None:
            return None
        return str(value)



class GAEItem(IVersionedGAEItem):

    def __init__(self, itemId, itemProperties, version):
        self._itemProperties = dict()
        for prop in itemProperties:
            self._itemProperties.put(prop.getId(), prop)
        self._version = version
        self._itemId = itemId


    def addItemProperty(self, id, prop):
        raise NotImplementedError

    def getItemProperty(self, Id):
        return self._itemProperties.get(Id)


    def getItemPropertyIds(self):
        return list(self._itemProperties.keys())


    def removeItemProperty(self, id):
        raise NotImplementedError


    def commit(self):
        GAEContainer_this.commitItem(self)


    def getVersion(self):
        return self._version


    def getId(self):
        return self._itemId


    def isWriteThrough(self):
        return GAEContainer_this._propertyWriteTrough


class ItemSetChangeEvent(EventObject, IItemSetChangeEvent):

    def __init__(self, source):
        self._source = None
        super(ItemSetChangeEvent, self).__init__(source)

    def getContainer(self):
        return self._source
