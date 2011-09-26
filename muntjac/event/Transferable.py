# Copyright (C) 2011 Vaadin Ltd
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

# from java.io.Serializable import (Serializable,)
# from java.util.Collection import (Collection,)


class Transferable(object):
    """Transferable wraps the data that is to be imported into another component.
    Currently Transferable is only used for drag and drop.

    @since 6.3
    """

    def getData(self, dataFlavor):
        """Returns the data from Transferable by its data flavor (aka data type).
        Data types can be any string keys, but MIME types like "text/plain" are
        commonly used.
        <p>
        Note, implementations of {@link Transferable} often provide a better
        typed API for accessing data.

        @param dataFlavor
                   the data flavor to be returned from Transferable
        @return the data stored in the Transferable or null if Transferable
                contains no data for given data flavour
        """
        pass


    def setData(self, dataFlavor, value):
        """Stores data of given data flavor to Transferable. Possibly existing value
        of the same data flavor will be replaced.

        @param dataFlavor
                   the data flavor
        @param value
                   the new value of the data flavor
        """
        pass


    def getDataFlavors(self):
        """@return a collection of data flavors ( data types ) available in this
                Transferable
        """
        pass


    def getSourceComponent(self):
        """@return the component that created the Transferable or null if the source
                component is unknown
        """
        pass
