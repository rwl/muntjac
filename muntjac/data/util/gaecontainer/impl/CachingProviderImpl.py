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

from muntjac.data.util.gaecontainer.CachingProvider import (CachingProvider,)
from muntjac.data.util.gaecontainer.Cache.IndexCache import (IndexCache,)
from muntjac.data.util.gaecontainer.Query.QueryProvider import (QueryProvider,)
from muntjac.data.util.gaecontainer.Cache.SizeCache import (SizeCache,)
from muntjac.data.util.gaecontainer.impl.DatastoreImpl import (DatastoreImpl,)
# from com.google.appengine.api.datastore.DatastoreFailureException import (DatastoreFailureException,)
# from com.google.appengine.api.datastore.Entity import (Entity,)
# from com.google.appengine.api.datastore.Key import (Key,)
# from java.util.Arrays import (Arrays,)
# from java.util.ConcurrentModificationException import (ConcurrentModificationException,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedHashMap import (LinkedHashMap,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.List import (List,)
# from java.util.Map import (Map,)
# from java.util.logging.Logger import (Logger,)


class CachingProviderImpl(CachingProvider, QueryProvider):
    """Dataprovider implementation that supports caching and queries.

    This implementation does not clear indexes when entities are added, deleted or changed. Manage data consistency by specifying lifetime.
     *Raw data in caches (ie entities) are updated on delete and add.
    <br>

    Caches are traversed for values starting from the first added with {@link #addCache(Cache)}. The caches that miss are consequently updated from hits lower in the hierarchy.
    All the settings for the caches are done trough {@link CacheConfig}.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """
    _caches = LinkedList()
    _datastore = DatastoreImpl()
    log = Logger.getLogger(CachingProviderImpl.getName())

    def addEntity(self, entity):
        try:
            entity = self._datastore.put(entity, True)
        except self.IllegalArgumentException, e:
            return None
        if entity is None:
            # there was some error adding the entity
            return None
        for cache in self._caches:
            cache.put(entity.getKey(), entity)
            if isinstance(cache, SizeCache):
                cache.updateSize(entity.getKind(), -1)
                # could maybe update instead of discarding
        return entity.getKey()

    def containsEntity(self, key):
        return self.getEntity(key) is not None

    def getEntity(self, key):
        cachesForUpdate = LinkedList()
        entity = None
        for cache in self._caches:
            entity = cache.get(key)
            if entity is not None:
                break
            else:
                cachesForUpdate.addFirst(cache)
        if entity is None:
            entity = self._datastore.get(key)
        if entity is not None:
            for c in cachesForUpdate:
                c.put(key, entity)
        return entity

    def getKeyByIndexFromEnd(self, query, index):
        result = self._datastore.get(query.getQueryFromEnd(), index, 1)
        if len(result) > 0:
            return result[0].getKey()
        return None

    def getKeyByIndexFromStart(self, query, index):
        cachesForUpdate = LinkedList()
        # first check caches
        for cache in self._caches:
            if isinstance(cache, IndexCache):
                if query.hasFilters() and not cache.cacheFilteredIndexes():
                    continue
                # how many elements to fetch from cache
                # where the cache line start
                # the offset to the part the cache for update is interested in
                if len(cachesForUpdate) > 0:
                    amount = cachesForUpdate.getFirst().getLineSize()
                    indexStart = index - (index % amount)
                    offset = index % amount
                else:
                    amount = 1
                    indexStart = index
                    offset = 0
                indexes = cache.getIndexes(query.getQueryIdentifier(), indexStart, amount)
                if (
                    ((indexes is None) or (not (len(indexes) >= offset))) or (indexes[offset] is None)
                ):
                    cachesForUpdate.addFirst(cache)
                else:
                    # found what we were looking for, update caches that missed
                    if len(cachesForUpdate) > 0:
                        # check also the case when 2 consecutive caches have same linesize -> speedup
                        indexList = Arrays.asList(indexes)
                        entities = cache.get(indexList)
                        for c in cachesForUpdate:
                            sliceoffset = index - (index % c.getLineSize()) - indexStart
                            indexSlice = indexList.subList(sliceoffset, sliceoffset + c.getLineSize())
                            entitySlice = dict()
                            for indexKey in indexSlice:
                                entitySlice.put(indexKey, entities[indexKey])
                            c.put(entitySlice)
                            c.putIndexes(query.getQueryIdentifier(), indexStart + sliceoffset, list(indexSlice))
                    return indexes[offset]
        # fetch from datastore
        if len(cachesForUpdate) > 0:
            amount = cachesForUpdate.getFirst().getLineSize()
            startIndex = (index / amount) * amount
        else:
            amount = 1
            startIndex = index
        result = self._datastore.get(query.getQuery(), startIndex, amount)
        try:
            key = result[index % amount].getKey()
        except self.IndexOutOfBoundsException, e:
            return None
        if not result.isEmpty():
            for c in cachesForUpdate:
                startIndex = (index / c.getLineSize()) * c.getLineSize()
                entityMap = self.getKeyEntityMap(result, c.getLineSize())
                c.put(entityMap)
                c.putIndexes(query.getQueryIdentifier(), startIndex, list(entityMap.keys()))
        return key
        # build a <key,entity> map of size size

    def getKeyEntityMap(self, entities, size):
        entityMap = LinkedHashMap()
        it = entities
        i = 0
        while it.hasNext() and i < size:
            entity = it.next()
            entityMap.put(entity.getKey(), entity)
            i += 1
        return entityMap

    def getKeys(self, kind):
        # TODO Auto-generated method stub
        raise self.UnsupportedOperationException()

    def removeEntity(self, key):
        for cache in self._caches:
            cache.remove(key)
            if isinstance(cache, SizeCache):
                cache.updateSize(key.getKind(), -1)
                # could maybe update instead of discarding
        try:
            self._datastore.delete(key)
            return True
        except self.IllegalArgumentException, e:
            return False
        except ConcurrentModificationException, e:
            return False
        except DatastoreFailureException, e:
            return False

    def updateEntity(self, entity, versioned):
        for cache in self._caches:
            cache.remove(entity.getKey())
        self._datastore.put(entity, versioned)

    def updateProperty(self, entity, versioned):
        oldEntity = self.getEntity(entity.getKey())
        oldEntity.setPropertiesFrom(entity)
        for cache in self._caches:
            cache.remove(entity.getKey())
        self._datastore.put(oldEntity, versioned)

    def addCache(self, cache):
        if 1000 % cache.getLineSize() != 0:
            raise self.IllegalArgumentException('cache line size must be a factor of 1000')
        for existingCache in self._caches:
            if cache.getLineSize() < existingCache.getLineSize():
                raise self.IllegalArgumentException('caches lower down in the hierarchy must have larger line size')
        self._caches.add(cache)

    def getNextKey(self, key, q):
        return self._datastore.getNextKey(key, q)

    def getPreviousKey(self, key, q):
        return self._datastore.getPreviousKey(key, q)

    def query(self, query, amount):
        return self._datastore.get(query.getQuery(), 0, amount)

    def size(self, query):
        cachesForUpdate = LinkedList()
        size = -1
        identifier = query.getFilterRepresentation()
        for cache in self._caches:
            if isinstance(cache, SizeCache) and cache.cacheFilteredSizes():
                size = len(identifier)
                if size != -1:
                    break
                else:
                    cachesForUpdate.addFirst(cache)
        if size == -1:
            size = len(query.getQuery())
        if size != -1:
            for c in cachesForUpdate:
                c.updateSize(identifier, size)
        return size
