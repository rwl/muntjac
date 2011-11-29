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

from muntjac.data.util.gaecontainer.data_provider import IDataProvider


class ICachingProvider(IDataProvider):
    """Providers that implement this cache must be able to handle a hierarchy
    of at least L{Cache} but may also take advantage of L{SizeCache} and
    L{IndexCache}.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def addCache(self, cache):
        """Adds a new cache to the hierarchy.

        The cache added last will be lowest down in the hierarchy.
        Caches of higher order must have a smaller or equal
        L{Cache.getLineSize} to the cache one step higher up in the hierarchy.
        Line size must be a factor of 1000

        @param cache: cache to be added
        @raise ValueError: if line size was inconsistent
        """
        raise NotImplementedError
