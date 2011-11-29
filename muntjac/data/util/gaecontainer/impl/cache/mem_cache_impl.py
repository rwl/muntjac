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

from muntjac.data.util.gaecontainer.cache.index_cache import IndexCache
from muntjac.data.util.gaecontainer.cache.cache import Cache


logger = logging.getLogger('MemCache')


class MemCacheImpl(Cache, IndexCache):
    """Use L{CacheFactory} to more convienently create an instance.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    memcache = MemcacheServiceFactory.getMemcacheService()

    def __init__(self, lineSize, indexLifeTime, itemLifeTime,
                cacheFilteredIndexes):
        """@param lineSize: Length of one cache line
        @param indexLifeTime: Life time of indexes
        @param itemLifeTime: Life time of raw data
        @param cacheFilteredIndexes:
                    Should indexes with filters applied be cached
        """
        # Length of one line
        self._LINE_SIZE = lineSize
        self._index_expiry = indexLifeTime
        self._data_expiry = itemLifeTime

        # Life time of raw data
        self._DATA_EXPIRY = Expiration.byDeltaSeconds(self._data_expiry)

        # Life time of indexes
        self._INDEX_EXPIRY = Expiration.byDeltaSeconds(self._index_expiry)

        # Should indexes with filters applied be cached
        self._cacheFilteredIndexes = cacheFilteredIndexes


    def contains(self, key):
        return self.memcache.contains(key)


    def flush(self):
        self.memcache.clearAll()


    def get(self, k):
        if isinstance(k, list):
            return self.memcache.getAll(k)
        else:
            return self.memcache.get(k)


    def put(self, *args):
        args = args
        nargs = len(args)
        if nargs == 1:
            entities, = args
            self.memcache.putAll(entities, self._DATA_EXPIRY,
                    MemcacheService.SetPolicy.ADD_ONLY_IF_NOT_PRESENT)
        elif nargs == 2:
            key, entity = args
            self.memcache.put(key, entity, self._DATA_EXPIRY,
                    MemcacheService.SetPolicy.ADD_ONLY_IF_NOT_PRESENT)
        else:
            raise ValueError


    def flushIndexes(self):
        raise NotImplementedError


    def getLineSize(self):
        return self._LINE_SIZE


    def getIndexes(self, queryIdentifier, index_start, amount):
        line_index = index_start / self._LINE_SIZE
        offset = index_start % self._LINE_SIZE

        cache_line = self.memcache.get(queryIdentifier + line_index)

        if cache_line is not None and len(cache_line) >= offset + amount:
            _slice = [None] * amount
            for i in range(offset, offset + amount):
                _slice[i - offset] = cache_line[i]
            return _slice
        return None


    def putIndexes(self, queryIdentifier, index_start, indexes):
        if index_start % self._LINE_SIZE != 0:
            return
        line_index = index_start / self._LINE_SIZE
        self.memcache.put(queryIdentifier + line_index, indexes,
                self._INDEX_EXPIRY, SetPolicy.SET_ALWAYS)


    def remove(self, key):
        self.memcache.delete(key)


    def cacheFilteredIndexes(self):
        return self._cacheFilteredIndexes


    def readObject(self, in_):
        in_.defaultReadObject()
        self._DATA_EXPIRY = Expiration.byDeltaSeconds(self._data_expiry)
        self._INDEX_EXPIRY = Expiration.byDeltaSeconds(self._index_expiry)
