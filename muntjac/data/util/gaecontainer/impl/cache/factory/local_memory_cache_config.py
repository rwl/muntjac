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

from muntjac.data.util.gaecontainer.impl.cache.factory import cache_config


class LocalMemoryCacheConfig(cache_config.CacheConfig):
    """Use this config to create a L{LocalMemoryCacheImpl} with
    L{CacheFactory}. Create with L{Builder}

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def __init__(self, lineSize, indexLifeTime, itemLifeTime, cacheFilteredIndexes, sizeLifeTime, indexCapacity, itemCapacity, sizeCapacity, cacheFilteredSizes, removeStrategy):
        super(LocalMemoryCacheConfig, self)(lineSize, indexLifeTime, itemLifeTime, cacheFilteredIndexes)
        self._sizeLifeTime = sizeLifeTime
        self._indexCapacity = indexCapacity
        self._itemCapacity = itemCapacity
        self._sizeCapacity = sizeCapacity
        self._cacheFilteredSizes = cacheFilteredSizes
        self._removeStrategy = removeStrategy


    def getSizeLifeTime(self):
        return self._sizeLifeTime


    def setSizeLifeTime(self, seconds):
        self._sizeLifeTime = seconds


    def getIndexCapacity(self):
        return self._indexCapacity


    def getItemCapacity(self):
        return self._itemCapacity


    def getSizeCapacity(self):
        return self._sizeCapacity


    def getCacheFilteredSizes(self):
        return self._cacheFilteredSizes


    def getRemoveStrategy(self):
        return self._removeStrategy


class Builder(cache_config.Builder):
    """Builder for creating a L{LocalMemoryCacheConfig}.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def __init__(self):
        self._sizeLifeTime = None
        self._indexCapacity = None
        self._itemCapacity = None
        self._sizeCapacity = None
        self._cacheFilteredSizes = None
        self._removeStrategy = None


    def withLineSize(self, size):
        """Length of one cache line

        @return: L{Builder} for chaining
        """
        self.lineSize = size
        return self


    def withIndexLifeTime(self, seconds):
        """Life time of indexes

        @return: L{Builder} for chaining
        """
        self.indexLifeTime = seconds
        return self


    def withItemLifeTime(self, seconds):
        """Life time of raw data

        @return: L{Builder} for chaining
        """
        self.itemLifeTime = seconds
        return self


    def withCacheFilteredIndexes(self, cacheFilterIndexes):
        """Should indexes with filters applied be cached

        @return: L{Builder} for chaining
        """
        self.cacheFilteredIndexes = cacheFilterIndexes
        return self


    def withSizeLifeTime(self, seconds):
        """Life time of cached sizes

        @return: L{Builder} for chaining
        """
        self._sizeLifeTime = seconds
        return self


    def withIndexCapacity(self, amount):
        """Number of lines with indexes to cache.

        Note that the actual maximum amount of indexes stored will be
        L{withLineSize} times amount.

        @return: L{Builder} for chaining
        """
        self._indexCapacity = amount
        return self


    def withItemCapacity(self, amount):
        """Number of items to cache

        @return: L{Builder} for chaining
        """
        self._itemCapacity = amount
        return self


    def withSizeCapacity(self, amount):
        """Number of sizes to cache

        @return: L{Builder} for chaining
        """
        self._sizeCapacity = amount
        return self


    def withCacheFilteredSizes(self, cacheFilteredSizes):
        """Should sizes with filters applied be cached

        @return: L{Builder} for chaining
        """
        self._cacheFilteredSizes = cacheFilteredSizes
        return self


    def withRemoveStrategy(self, removeStrategy):
        """Remove strategy for the cache.

        @return: L{Builder} for chaining
        """
        self._removeStrategy = removeStrategy
        return self


    def build(self):
        return LocalMemoryCacheConfig(self.lineSize, self.indexLifeTime,
                self.itemLifeTime, self.cacheFilteredIndexes,
                self._sizeLifeTime, self._indexCapacity,
                self._itemCapacity, self._sizeCapacity,
                self._cacheFilteredSizes, self._removeStrategy)


class RemoveStrategy(object):

    FIFO = 'FIFO'

    LRU = 'LRU'

    _values = [FIFO, LRU]

    @classmethod
    def values(cls):
        return cls._values[:]
