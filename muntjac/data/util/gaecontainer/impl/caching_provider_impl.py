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

from muntjac.data.util.gaecontainer.caching_provider import ICachingProvider
from muntjac.data.util.gaecontainer.cache.index_cache import IIndexCache
from muntjac.data.util.gaecontainer.query.query_provider import IQueryProvider
from muntjac.data.util.gaecontainer.cache.size_cache import ISizeCache
from muntjac.data.util.gaecontainer.impl.datastore_impl import DatastoreImpl


logger = logging.getLogger(__name__)


class CachingProviderImpl(ICachingProvider, IQueryProvider):
    """DataProvider implementation that supports caching and queries.

    This implementation does not clear indexes when entities are added,
    deleted or changed. Manage data consistency by specifying lifetime.

    Raw data in caches (ie entities) are updated on delete and add.

    Caches are traversed for values starting from the first added with
    L{addCache}. The caches that miss are consequently updated from hits
    lower in the hierarchy.

    All the settings for the caches are done trough L{CacheConfig}.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    _datastore = DatastoreImpl()


    def addEntity(self, entity):
        self._caches = list()

        try:
            entity = self._datastore.put(entity, True)
        except self.IllegalArgumentException:
            return None

        if entity is None:  # there was some error adding the entity
            return None

        for cache in self._caches:
            cache.put(entity.getKey(), entity)
            if isinstance(cache, SizeCache):
                # could maybe update instead of discarding
                cache.updateSize(entity.getKind(), -1)

        return entity.getKey()


    def containsEntity(self, key):
        return self.getEntity(key) is not None


    def getEntity(self, key):
        cachesForUpdate = list()
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
        cachesForUpdate = list()

        # first check caches
        for cache in self._caches:
            if isinstance(cache, IIndexCache):
                if query.hasFilters() and not cache.cacheFilteredIndexes():
                    continue

                # how many elements to fetch from cache
                amount = 1
                # where the cache line start
                indexStart = index
                # the offset to the part the cache for update is interested in
                offset = 0

                if len(cachesForUpdate) > 0:
                    amount = cachesForUpdate.getFirst().getLineSize()
                    indexStart = index - (index % amount)
                    offset = index % amount

                indexes = cache.getIndexes(query.getQueryIdentifier(),
                        indexStart, amount)
                if ((indexes is None) or (not (len(indexes) >= offset))
                        or (indexes[offset] is None)):
                    cachesForUpdate.addFirst(cache)
                else:
                    # found what we were looking for, update caches that missed
                    if len(cachesForUpdate) > 0:

                        # check also the case when 2 consecutive caches have
                        # same linesize -> speedup
                        indexList = list(indexes)
                        entities = cache.get(indexList)

                        for c in cachesForUpdate:

                            sliceoffset = index - (index % c.getLineSize()) - indexStart
                            indexSlice = indexList.subList(sliceoffset, sliceoffset + c.getLineSize())

                            entitySlice = dict()
                            for indexKey in indexSlice:
                                entitySlice.put(indexKey, entities[indexKey])

                            c.put(entitySlice)
                            c.putIndexes(query.getQueryIdentifier(),
                                    indexStart + sliceoffset, list(indexSlice))

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
        except IndexOutOfBoundsException:
            return None

        if len(result) > 0:
            for c in cachesForUpdate:
                startIndex = (index / c.getLineSize()) * c.getLineSize()
                entityMap = self.getKeyEntityMap(result, c.getLineSize())
                c.put(entityMap)
                c.putIndexes(query.getQueryIdentifier(), startIndex,
                        list(entityMap.keys()))
        return key


    def getKeyEntityMap(self, entities, size):
        # build a <key,entity> map of size size
        entityMap = dict()

        i = 0
        while i < size:
            try:
                entity = entities.next()
                entityMap.put(entity.getKey(), entity)
                i += 1
            except StopIteration:
                break

        return entityMap


    def getKeys(self, kind):
        raise NotImplementedError


    def removeEntity(self, key):
        for cache in self._caches:
            cache.remove(key)
            if isinstance(cache, ISizeCache):
                # could maybe update instead of discarding
                cache.updateSize(key.getKind(), -1)
        try:
            self._datastore.delete(key)
            return True
        except IllegalArgumentException:
            return False
        except ConcurrentModificationException:
            return False
        except DatastoreFailureException:
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
            raise IllegalArgumentException(
                    'cache line size must be a factor of 1000')

        for existingCache in self._caches:
            if cache.getLineSize() < existingCache.getLineSize():
                raise IllegalArgumentException('caches lower down in the '
                        'hierarchy must have larger line size')
        self._caches.add(cache)


    def getNextKey(self, key, q):
        return self._datastore.getNextKey(key, q)


    def getPreviousKey(self, key, q):
        return self._datastore.getPreviousKey(key, q)


    def query(self, query, amount):
        return self._datastore.get(query.getQuery(), 0, amount)


    def size(self, query):
        cachesForUpdate = list()
        size = -1
        identifier = query.getFilterRepresentation()
        for cache in self._caches:
            if isinstance(cache, ISizeCache) and cache.cacheFilteredSizes():
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
