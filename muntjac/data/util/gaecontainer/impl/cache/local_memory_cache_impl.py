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

from datetime import date as Date

from muntjac.data.util.gaecontainer.cache.index_cache import IIndexCache
from muntjac.data.util.gaecontainer.cache.cache import ICache
from muntjac.data.util.gaecontainer.cache.size_cache import ISizeCache


logger = logging.getLogger('MemoryCache')


class LocalMemoryCacheImpl(ISizeCache, IIndexCache):#ICache
    """This cache should be instantiated by I{CacheFactory} using
    L{LocalMemoryCacheConfig}.

    The local memory used by this cache is not infinitely big and poses a
    upper limit on how much can be stored.

    Does not represent a global view of the data but is local for every server
    instance. Cached data is shared by all threads in the same instance. Is
    thread safe. Shared variables such as capacity, remove strategy and line
    size must be the same for all L{LocalMemoryCacheImpl} in the same instance.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    # shared by all memory caches in the same Container
    _cachedIndexes = None
    _cachedEntities = None
    _cachedSizes = None


    def __init__(self, lineSize, indexLifeTime, itemLifeTime,
                cacheFilteredIndexes, sizeLifeTime, indexCapacity,
                itemCapacity, sizeCapacity, cacheFilteredSizes, LRU):
        """@param lineSize: Length of one cache line
        @param indexLifeTime: Life time of indexes
        @param itemLifeTime: Life time of raw data
        @param cacheFilteredIndexes: Should indexes with filters applied be cached
        @param sizeLifeTime: Life time of cached sizes
        @param indexCapacity: Number of lines with indexes to store
        @param itemCapacity: Number of entities to store
        @param sizeCapacity: Number of sizes to store
        @param cacheFilteredSizes: Should sizes with filters applied be cached
        @param LRU: If true use LRU else FIFO
        """
        self._LINE_SIZE = lineSize
        # local to every memory cache
        self._index_life_time = indexLifeTime
        self._item_life_time = itemLifeTime
        self._size_life_time = sizeLifeTime
        self._cacheFilteredSizes = cacheFilteredSizes
        self._cacheFilteredIndexes = cacheFilteredIndexes

        self._indexLock = ReentrantReadWriteLock()  # transient
        self._itemLock = ReentrantReadWriteLock()  # transient
        self._sizeLock = ReentrantReadWriteLock()  # transient

        self._LRU = LRU
        self._index_capacity = indexCapacity
        self._item_capacity = itemCapacity
        self._size_capcaity = sizeCapacity
        self.InitCaches()


    def InitCaches(self):
        if self._cachedIndexes is None:
            self._cachedIndexes = CacheMap(self._index_capacity, self._LRU)

        if self._cachedEntities is None:
            self._cachedEntities = CacheMap(self._item_capacity, self._LRU)

        if self._cachedSizes is None:
            self._cachedSizes = CacheMap(self._size_capcaity, self._LRU)


    def contains(self, key):
        raise NotImplementedError


    def flush(self):
        self._indexLock.writeLock().lock()
        self._cachedIndexes.clear()
        self._indexLock.writeLock().unlock()
        self._itemLock.writeLock().lock()
        self._cachedEntities.clear()
        self._itemLock.writeLock().unlock()


    def get(self, k):
        # Returns only the pairs that could be found in the cache. Hence a
        # incomplete map could be returned.
        if isinstance(k, list):
            entities = dict()
            for key in k:
                entities[key] = self.get(key)
            if len(entities) > 0:
                return entities
            return None
        else:
            key = k
            self._itemLock.readLock().lock()
            cachedItem = self._cachedEntities.get(key)
            self._itemLock.readLock().unlock()
            if cachedItem is not None:
                if cachedItem.isValid():
                    return cachedItem.getValue()
                else:
                    self._itemLock.writeLock().lock()
                    self._cachedEntities.remove(key)
                    self._itemLock.writeLock().unlock()
            return None


    def put(self, *args):
        args = args
        nargs = len(args)
        if nargs == 1:
            entities, = args
            for key in entities.keys():
                self.put(key, entities.get(key))
        elif nargs == 2:
            key, entity = args
            self._itemLock.writeLock().lock()
            self._cachedEntities.put(key, MemoryCacheItem(entity,
                    self._item_life_time))
            self._itemLock.writeLock().unlock()
        else:
            raise ValueError


    def flushIndexes(self):
        self._indexLock.writeLock().lock()
        self._cachedIndexes.clear()
        self._indexLock.writeLock().unlock()


    def size(self, identifer):
        self._sizeLock.readLock().lock()
        cachedSize = self._cachedSizes.get(identifer)
        self._sizeLock.readLock().unlock()
        size = -1
        if cachedSize is not None:
            if cachedSize.isValid():
                size = cachedSize.getValue().intValue()
            else:
                self._sizeLock.writeLock().lock()
                self._cachedSizes.remove(identifer)
                self._sizeLock.writeLock().unlock()
        return size


    def updateSize(self, identifier, new_size):
        self._cachedSizes.put(identifier, MemoryCacheItem(new_size,
                self._size_life_time))


    def getIndexes(self, queryIdentifier, index_start, amount):
        line_index = index_start / self._LINE_SIZE
        offset = index_start % self._LINE_SIZE
        key = queryIdentifier + line_index
        self._indexLock.readLock().lock()
        cachedIndex = self._cachedIndexes.get(key)
        self._indexLock.readLock().unlock()
        if cachedIndex is not None:
            if cachedIndex.isValid():
                cache_line = cachedIndex.getValue()
                if cache_line is not None and len(cache_line) == amount:
                    return cache_line
                if cache_line is not None and len(cache_line) >= offset + amount:
                    _slice = [None] * amount

                    for i in range(offset, offset + amount):
                        _slice[i - offset] = cache_line[i]

                    return _slice
            else:
                self._indexLock.writeLock().lock()
                self._cachedIndexes.remove(key)
                self._indexLock.writeLock().unlock()

        return None


    def getLineSize(self):
        return self._LINE_SIZE


    def putIndexes(self, queryIdentifier, index_start, indexes):
        if index_start % self._LINE_SIZE != 0:
            logger.warning('inconsistent start index given to putIndexes')
            return

        logger.info('Memorycaches indexes are beeing updated')
        line_index = index_start / self._LINE_SIZE

        key = queryIdentifier + line_index
        self._indexLock.writeLock().lock()
        self._cachedIndexes.put(key, MemoryCacheItem(indexes,
                self._index_life_time))
        self._indexLock.writeLock().unlock()


    def remove(self, key):
        self._itemLock.writeLock().lock()
        self._cachedEntities.remove(key)
        self._itemLock.writeLock().unlock()


    def cacheFilteredSizes(self):
        return self._cacheFilteredSizes


    def cacheFilteredIndexes(self):
        return self._cacheFilteredIndexes


    def readObject(self, in_):
        in_.defaultReadObject()
        self.InitCaches()
        self._indexLock = ReentrantReadWriteLock()
        self._itemLock = ReentrantReadWriteLock()
        self._sizeLock = ReentrantReadWriteLock()


class MemoryCacheItem(object):

    def __init__(self, value, lifeTime):
        # lifetime in seconds
        cal = Calendar.getInstance()
        cal.add(Calendar.SECOND, lifeTime)
        self._expires = cal.getTime()
        self._value = value


    def getValue(self):
        if self._expires.after(Date()):
            return self._value
        return None


    def isValid(self):
        return self._expires.after(Date())


class CacheMap(LinkedHashMap):

    def __init__(self, maxSize, accessOrder):
        super(CacheMap, self).__init__(maxSize, 0.75, accessOrder)
        self._MAX_SIZE = maxSize


    def removeEldestEntry(self, eldest):
        return len(self) > self._MAX_SIZE
