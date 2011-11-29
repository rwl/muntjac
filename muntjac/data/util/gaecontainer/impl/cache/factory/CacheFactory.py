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
from muntjac.data.util.gaecontainer.impl.Cache.LocalMemoryCacheImpl import (LocalMemoryCacheImpl,)
from muntjac.data.util.gaecontainer.impl.Cache.MemCacheImpl import (MemCacheImpl,)
from muntjac.data.util.gaecontainer.impl.Cache.Factory.LocalMemoryCacheConfig import (LocalMemoryCacheConfig,)
from muntjac.data.util.gaecontainer.impl.Cache.Factory.MemCacheConfig import (MemCacheConfig,)


class CacheFactory(object):
    """Creates caches that can be used with {@link GAEContainer}

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    @classmethod
    def getCache(cls, *args):
        """Creates a {@link LocalMemoryCacheImpl}
        Note that:<br>
        {@link LocalMemoryCacheConfig.Builder#withLineSize(int)} <br>
        {@link LocalMemoryCacheConfig.Builder#withIndexCapacity(int)}, <br>
        {@link LocalMemoryCacheConfig.Builder#withItemCapacity(int)}, <br>
        {@link LocalMemoryCacheConfig.Builder#withSizeCapacity(int)},<br>
        {@link LocalMemoryCacheConfig.Builder#withRemoveStrategy(muntjac.data.util.gaecontainer.impl.Cache.Factory.LocalMemoryCacheConfig.RemoveStrategy)} <br>
        must be the same for all {@link LocalMemoryCacheImpl}
        @param c
        @return
        ---
        Creates a {@link MemCacheImpl}
        @param c
        @return
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], LocalMemoryCacheConfig):
                c, = _0
                LRU = False
                if c.getRemoveStrategy() == LocalMemoryCacheConfig.RemoveStrategy.LRU:
                    LRU = True
                return LocalMemoryCacheImpl(c.getLineSize(), c.getIndexLifeTime(), c.getItemLifeTime(), c.getCacheFilteredIndexes(), c.getSizeLifeTime(), c.getIndexCapacity(), c.getItemCapacity(), c.getSizeCapacity(), c.getCacheFilteredSizes(), LRU)
            else:
                c, = _0
                return MemCacheImpl(c.getLineSize(), c.getIndexLifeTime(), c.getItemLifeTime(), c.getCacheFilteredIndexes())
        else:
            raise ARGERROR(1, 1)

    @classmethod
    def getDefaultMemCache(cls):
        """Creates a {@link MemCacheImpl} with default values
        Line size - 50
        Index life time - 180 seconds
        Item life time - 180 seconds
        Cache filtered indexes - true
        @return
        """
        return MemCacheImpl(50, 180, 180, True)

    @classmethod
    def getDefaultLocalMemoryCache(cls):
        """Creates a {@link LocalMemoryCacheImpl} with default values
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
        @return
        """
        return LocalMemoryCacheImpl(25, 120, 120, True, 60, 40, 1000, 100, True, True)
