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


class CacheConfig(object):
    """Don't use this class directly use one of its subclasses.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def __init__(self, lineSize, indexLifeTime, itemLifeTime,
                cacheFilteredIndexes):
        self._lineSize = lineSize
        self._indexLifeTime = indexLifeTime
        self._itemLifeTime = itemLifeTime
        self._cacheFilteredIndexes = cacheFilteredIndexes


    def getLineSize(self):
        return self._lineSize


    def getIndexLifeTime(self):
        return self._indexLifeTime


    def getItemLifeTime(self):
        return self._itemLifeTime


    def getCacheFilteredIndexes(self):
        return self._cacheFilteredIndexes


class Builder(object):
    """Abstract Builder for creating a L{CacheConfig}

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def __init__(self):
        self.lineSize = None
        self.indexLifeTime = None
        self.itemLifeTime = None
        self.cacheFilteredIndexes = None


    def build(self):
        """Build the config.

        @return: A config with the specified options
        """
        pass
