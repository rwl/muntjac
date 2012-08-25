# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

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
