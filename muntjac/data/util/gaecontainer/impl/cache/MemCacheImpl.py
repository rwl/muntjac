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
# from com.google.appengine.api.memcache.Expiration import (Expiration,)
# from com.google.appengine.api.memcache.MemcacheService import (MemcacheService,)
# from com.google.appengine.api.memcache.MemcacheService.SetPolicy import (SetPolicy,)
# from com.google.appengine.api.memcache.MemcacheServiceFactory import (MemcacheServiceFactory,)
# from java.io.IOException import (IOException,)
# from java.util.Collection import (Collection,)
# from java.util.Map import (Map,)
# from java.util.logging.Logger import (Logger,)


class MemCacheImpl(Cache, IndexCache):
    """Use {@link muntjac.data.util.gaecontainer.impl.Cache.Factory.CacheFactory} to more convienently create an instance.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """
    # Life time of raw data
    _DATA_EXPIRY = None
    _data_expiry = None
    # Life time of indexes
    _INDEX_EXPIRY = None
    _index_expiry = None
    log = Logger.getLogger('MemCache')
    memcache = MemcacheServiceFactory.getMemcacheService()
    # Length of one line
    _LINE_SIZE = None
    # Should indexes with filters applied be cached
    _cacheFilteredIndexes = None

    def __init__(self, lineSize, indexLifeTime, itemLifeTime, cacheFilteredIndexes):
        """@param lineSize Length of one cache line
        @param indexLifeTime Life time of indexes
        @param itemLifeTime Life time of raw data
        @param cacheFilteredIndexes Should indexes with filters applied be cached
        """
        self._LINE_SIZE = lineSize
        self._index_expiry = indexLifeTime
        self._data_expiry = itemLifeTime
        self._DATA_EXPIRY = Expiration.byDeltaSeconds(self._data_expiry)
        self._INDEX_EXPIRY = Expiration.byDeltaSeconds(self._index_expiry)
        self._cacheFilteredIndexes = cacheFilteredIndexes

    def contains(self, key):
        try:
            return self.memcache.contains(key)
        except self.IllegalArgumentException, e:
            raise e

    def flush(self):
        self.memcache.clearAll()

    def get(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Collection):
                keys, = _0
                return self.memcache.getAll(keys)
            else:
                key, = _0
                return self.memcache.get(key)
        else:
            raise ARGERROR(1, 1)

    def put(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            entities, = _0
            self.memcache.putAll(entities, self._DATA_EXPIRY, MemcacheService.SetPolicy.ADD_ONLY_IF_NOT_PRESENT)
        elif _1 == 2:
            key, entity = _0
            self.memcache.put(key, entity, self._DATA_EXPIRY, MemcacheService.SetPolicy.ADD_ONLY_IF_NOT_PRESENT)
        else:
            raise ARGERROR(1, 2)

    def flushIndexes(self):
        raise self.UnsupportedOperationException()

    def getLineSize(self):
        return self._LINE_SIZE

    def getIndexes(self, queryIdentifier, index_start, amount):
        line_index = index_start / self._LINE_SIZE
        offset = index_start % self._LINE_SIZE
        cache_line = self.memcache.get(queryIdentifier + line_index)
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
        return None

    def putIndexes(self, queryIdentifier, index_start, indexes):
        if index_start % self._LINE_SIZE != 0:
            return
        line_index = index_start / self._LINE_SIZE
        self.memcache.put(queryIdentifier + line_index, indexes, self._INDEX_EXPIRY, SetPolicy.SET_ALWAYS)

    def remove(self, key):
        self.memcache.delete(key)

    def cacheFilteredIndexes(self):
        return self._cacheFilteredIndexes

    def readObject(self, in_):
        in_.defaultReadObject()
        self._DATA_EXPIRY = Expiration.byDeltaSeconds(self._data_expiry)
        self._INDEX_EXPIRY = Expiration.byDeltaSeconds(self._index_expiry)
