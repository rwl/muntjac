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
from muntjac.data.util.gaecontainer.Cache.IndexCache import (IndexCache,)
from muntjac.data.util.gaecontainer.Cache.Cache import (Cache,)
from muntjac.data.util.gaecontainer.Cache.SizeCache import (SizeCache,)
# from java.io.IOException import (IOException,)
# from java.util.Calendar import (Calendar,)
# from java.util.Collection import (Collection,)
# from java.util.Date import (Date,)
# from java.util.HashMap import (HashMap,)
# from java.util.LinkedHashMap import (LinkedHashMap,)
# from java.util.Map import (Map,)
# from java.util.concurrent.locks.ReadWriteLock import (ReadWriteLock,)
# from java.util.concurrent.locks.ReentrantReadWriteLock import (ReentrantReadWriteLock,)
# from java.util.logging.Logger import (Logger,)


class LocalMemoryCacheImpl(Cache, IndexCache, SizeCache):
    """This cache should be instantiated by {@link CacheFactory} using {@link LocalMemoryCacheConfig}.
    The local memory used by this cache is not infinitely big and poses a upper limit on how much can be stored.
    <br>
    Does not represent a global view of the data but is local for every server instance.
    Cached data is shared by all threads in the same instance. Is thread safe.
    Shared variables such as capacity, remove strategy and line size must be the same for all {@link LocalMemoryCacheImpl} in the same instance.
    @author: Johan Selanniemi
    @author: Richard Lincoln
    """
    # local to every memory cache
    _index_life_time = None
    _item_life_time = None
    _size_life_time = None
    _cacheFilteredSizes = None
    _cacheFilteredIndexes = None
    # shared by all memory caches in the same Container or JVM
    log = Logger.getLogger('MemoryCache')
    _cachedIndexes = None
    _cachedEntities = None
    _cachedSizes = None
    _indexLock = ReentrantReadWriteLock()
    _itemLock = ReentrantReadWriteLock()
    _sizeLock = ReentrantReadWriteLock()
    _LINE_SIZE = None
    _LRU = None
    _index_capacity = None
    _item_capacity = None
    _size_capcaity = None

    def __init__(self, lineSize, indexLifeTime, itemLifeTime, cacheFilteredIndexes, sizeLifeTime, indexCapacity, itemCapacity, sizeCapacity, cacheFilteredSizes, LRU):
        """@param lineSize	Length of one cache line
        @param indexLifeTime Life time of indexes
        @param itemLifeTime Life time of raw data
        @param cacheFilteredIndexes Should indexes with filters applied be cached
        @param sizeLifeTime Life time of cached sizes
        @param indexCapacity Number of lines with indexes to store
        @param itemCapacity Number of entities to store
        @param sizeCapacity Number of sizes to store
        @param cacheFilteredSizes Should sizes with filters applied be cached
        @param LRU If true use LRU else FIFO
        """
        self._LINE_SIZE = lineSize
        self._index_life_time = indexLifeTime
        self._item_life_time = itemLifeTime
        self._size_life_time = sizeLifeTime
        self._cacheFilteredSizes = cacheFilteredSizes
        self._cacheFilteredIndexes = cacheFilteredIndexes
        self._LRU = LRU
        self._index_capacity = indexCapacity
        self._item_capacity = itemCapacity
        self._size_capcaity = sizeCapacity
        self.InitCaches()

    def InitCaches(self):
        if self._cachedIndexes is None:
            self._cachedIndexes = self.CacheMap(self._index_capacity, self._LRU)
        if self._cachedEntities is None:
            self._cachedEntities = self.CacheMap(self._item_capacity, self._LRU)
        if self._cachedSizes is None:
            self._cachedSizes = self.CacheMap(self._size_capcaity, self._LRU)

    def contains(self, key):
        raise self.UnsupportedOperationException()

    def flush(self):
        # (non-Javadoc)
        # @see muntjac.data.util.gaecontainer.Cache.Cache#get(java.util.Collection)
        # returns only the pairs that could be found in the cache. Hence a incomplete map could be returned.

        self._indexLock.writeLock().lock()
        self._cachedIndexes.clear()
        self._indexLock.writeLock().unlock()
        self._itemLock.writeLock().lock()
        self._cachedEntities.clear()
        self._itemLock.writeLock().unlock()

    def get(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Collection):
                keys, = _0
                entities = dict()
                for key in keys:
                    entities.put(key, self.get(key))
                if len(entities) > 0:
                    return entities
                return None
            else:
                key, = _0
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
        else:
            raise ARGERROR(1, 1)

    def put(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            entities, = _0
            for key in entities.keys():
                self.put(key, entities.get(key))
        elif _1 == 2:
            key, entity = _0
            self._itemLock.writeLock().lock()
            self._cachedEntities.put(key, self.MemoryCacheItem(entity, self._item_life_time))
            self._itemLock.writeLock().unlock()
        else:
            raise ARGERROR(1, 2)

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
        self._cachedSizes.put(identifier, self.MemoryCacheItem(new_size, self._size_life_time))

    class MemoryCacheItem(object):
        _value = None
        _expires = None

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
                    slice = [None] * amount
                    _0 = True
                    i = offset
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            i += 1
                        if not (i < offset + amount):
                            break
                        slice[i - offset] = cache_line[i]
                    return slice
            else:
                self._indexLock.writeLock().lock()
                self._cachedIndexes.remove(key)
                self._indexLock.writeLock().unlock()
        return None

    def getLineSize(self):
        return self._LINE_SIZE

    def putIndexes(self, queryIdentifier, index_start, indexes):
        if index_start % self._LINE_SIZE != 0:
            self.log.warning('inconsistent start index given to putIndexes')
            return
        self.log.info('Memorycaches indexes are beeing updated')
        line_index = index_start / self._LINE_SIZE
        key = queryIdentifier + line_index
        self._indexLock.writeLock().lock()
        self._cachedIndexes.put(key, self.MemoryCacheItem(indexes, self._index_life_time))
        self._indexLock.writeLock().unlock()

    def remove(self, key):
        self._itemLock.writeLock().lock()
        self._cachedEntities.remove(key)
        self._itemLock.writeLock().unlock()

    class CacheMap(LinkedHashMap):
        _serialVersionUID = 1L
        _MAX_SIZE = None

        def __init__(self, maxSize, accessOrder):
            super(CacheMap, self)(maxSize, 0.75, accessOrder)
            self._MAX_SIZE = maxSize

        def removeEldestEntry(self, eldest):
            return len(self) > self._MAX_SIZE

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
