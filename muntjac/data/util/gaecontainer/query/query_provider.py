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


class QueryProvider(IDataProvider):
    """Implemented by providers that supports querying.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def query(self, query, amount):
        """Gets a list of entities.

        @param query: Representation of filters and sort orders
        @param amount: Number of entities to get
        @return: Complete or partial list, or null
        """
        raise NotImplementedError
