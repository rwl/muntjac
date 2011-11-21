# Copyright (C) 2011 Vaadin Ltd.
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
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

"""Wraps the data that is to be imported into another component."""


class ITransferable(object):
    """ITransferable wraps the data that is to be imported into another
    component. Currently ITransferable is only used for drag and drop.
    """

    def getData(self, dataFlavor):
        """Returns the data from ITransferable by its data flavor (aka data
        type). Data types can be any string keys, but MIME types like
        "text/plain" are commonly used.

        Note, implementations of L{ITransferable} often provide a better
        typed API for accessing data.

        @param dataFlavor:
                   the data flavor to be returned from ITransferable
        @return: the data stored in the ITransferable or null if ITransferable
                contains no data for given data flavour
        """
        raise NotImplementedError


    def setData(self, dataFlavor, value):
        """Stores data of given data flavor to ITransferable. Possibly existing
        value of the same data flavor will be replaced.

        @param dataFlavor:
                   the data flavor
        @param value:
                   the new value of the data flavor
        """
        raise NotImplementedError


    def getDataFlavors(self):
        """@return: a collection of data flavors ( data types ) available in
                this ITransferable
        """
        raise NotImplementedError


    def getSourceComponent(self):
        """@return: the component that created the ITransferable or null if
                the source component is unknown
        """
        raise NotImplementedError
