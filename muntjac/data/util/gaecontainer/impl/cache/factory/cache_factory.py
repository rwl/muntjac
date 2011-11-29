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

from muntjac.data.util.gaecontainer.impl.cache.local_memory_cache_impl \
    import LocalMemoryCacheImpl

from muntjac.data.util.gaecontainer.impl.cache.mem_cache_impl \
    import MemCacheImpl

from muntjac.data.util.gaecontainer.impl.cache.factory.LocalMemoryCacheConfig \
    import LocalMemoryCacheConfig

from muntjac.data.util.gaecontainer.impl.cache.factory.MemCacheConfig \
    import MemCacheConfig


class CacheFactory(object):
    """Creates caches that can be used with {@link GAEContainer}

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    @classmethod
    def getCache(cls, c):
        """Creates a L{LocalMemoryCacheImpl}

        Note that:
        L{Builder.withLineSize}
        L{Builder.withIndexCapacity},
        L{Builder.withItemCapacity},
        L{Builder.withSizeCapacity},
        L{Builder.withRemoveStrategy}
        must be the same for all L{LocalMemoryCacheImpl}
        """
        if isinstance(c, LocalMemoryCacheConfig):
            LRU = False
            if c.getRemoveStrategy() == LocalMemoryCacheConfig.RemoveStrategy.LRU:
                LRU = True
            return LocalMemoryCacheImpl(c.getLineSize(), c.getIndexLifeTime(),
                    c.getItemLifeTime(), c.getCacheFilteredIndexes(),
                    c.getSizeLifeTime(), c.getIndexCapacity(),
                    c.getItemCapacity(), c.getSizeCapacity(),
                    c.getCacheFilteredSizes(), LRU)
        else:
            return MemCacheImpl(c.getLineSize(), c.getIndexLifeTime(),
                    c.getItemLifeTime(), c.getCacheFilteredIndexes())


    @classmethod
    def getDefaultMemCache(cls):
        """Creates a L{MemCacheImpl} with default values.
        Line size - 50
        Index life time - 180 seconds
        Item life time - 180 seconds
        Cache filtered indexes - true
        @return
        """
        return MemCacheImpl(50, 180, 180, True)


    @classmethod
    def getDefaultLocalMemoryCache(cls):
        """Creates a L{LocalMemoryCacheImpl} with default values.
        Line size - 25 items
        Index life time - 120 seconds
        Item life time - 120 seconds
        Cache filtered indexes - true
        Size life time - 60 seconds
        Index capacity - 1000 indexes
        Item capacity - 1000 items
        Size capacity - 100 sizes
        Cache filtered sizes - true
        Remove strategy - LRU
        """
        return LocalMemoryCacheImpl(25, 120, 120, True, 60, 40, 1000,
                100, True, True)
