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


class IFormFieldFactory(object):
    """Factory interface for creating new Field-instances based on
    L{Item}, property id and uiContext (the component responsible for
    displaying fields). Currently this interface is used by L{Form}, but
    might later be used by some other components for L{Field} generation.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    @see: L{TableFieldFactory}
    """

    def createField(self, item, propertyId, uiContext):
        """Creates a field based on the item, property id and the component
        (most commonly L{Form}) where the Field will be presented.

        @param item:
                   the item where the property belongs to.
        @param propertyId:
                   the Id of the property.
        @param uiContext:
                   the component where the field is presented, most commonly
                   this is L{Form}. uiContext will not necessary be the
                   parent component of the field, but the one that is
                   responsible for creating it.
        @return: Field the field suitable for editing the specified data.
        """
        raise NotImplementedError
