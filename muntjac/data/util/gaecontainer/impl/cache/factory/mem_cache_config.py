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


class MemCacheConfig(cache_config.CacheConfig):
    """Use this config to create a L{MemCacheImpl} with L{CacheFactory}.
    Create with L{Builder}

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def __init__(self, lineSize, indexLifeTime, itemLifeTime,
                cacheFilteredIndexes):
        super(MemCacheConfig, self)(lineSize, indexLifeTime, itemLifeTime,
                cacheFilteredIndexes)


class Builder(cache_config.Builder):
    """Builder for creating a L{MemCacheConfig}.
    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def withLineSize(self, size):
        """Length of one cache line.

        @return L{Builder} for chaining.
        """
        self.lineSize = size
        return self


    def withIndexLifeTime(self, seconds):
        """Life time of indexes.

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


    def build(self):
        return MemCacheConfig(self.lineSize, self.indexLifeTime,
                self.itemLifeTime, self.cacheFilteredIndexes)
