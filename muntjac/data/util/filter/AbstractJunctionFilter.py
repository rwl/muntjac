# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.data.Container import Filter


class AbstractJunctionFilter(Filter):
    """Abstract base class for filters that are composed of multiple sub-filters.

    The method {@link #appliesToProperty(Object)} is provided to help
    implementing {@link Filter} for in-memory filters.

    @since 6.6
    """
    filters = None

    def __init__(self, *filters):
        self.filters = list(filters)


    def getFilters(self):
        """Returns an unmodifiable collection of the sub-filters of this composite
        filter.

        @return
        """
        return self.filters


    def appliesToProperty(self, propertyId):
        """Returns true if a change in the named property may affect the filtering
        result. If some of the sub-filters are not in-memory filters, true is
        returned.

        By default, all sub-filters are iterated to check if any of them applies.
        If there are no sub-filters, false is returned - override in subclasses
        to change this behavior.
        """
        for fltr in self.getFilters():
            if fltr.appliesToProperty(propertyId):
                return True
        return False


#    @Override
#    public boolean equals(Object obj) {
#        if (obj == null || !getClass().equals(obj.getClass())) {
#            return false;
#        }
#        AbstractJunctionFilter other = (AbstractJunctionFilter) obj;
#        // contents comparison with equals()
#        return Arrays.equals(filters.toArray(), other.filters.toArray());
#    }
#
#    @Override
#    public int hashCode() {
#        int hash = getFilters().size();
#        for (Filter filter : filters) {
#            hash = (hash << 1) ^ filter.hashCode();
#        }
#        return hash;
#    }