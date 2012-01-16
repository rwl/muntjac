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

from muntjac.ui.table_field_factory import ITableFieldFactory
from muntjac.ui.form_field_factory import IFormFieldFactory


class IFieldFactory(IFormFieldFactory, ITableFieldFactory):
    """Factory for creating new Field-instances based on type, datasource
    and/or context.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    @deprecated: IFieldFactory was split into two lighter interfaces.
                 Use IFormFieldFactory or ITableFieldFactory or both instead.
    """

    def createField(self, *args):
        """Creates a field based on type of data.

        @param args: tuple of the form
            - (type, uiContext)
              1. the type of data presented in field.
              2. the component where the field is presented.
            - (property, uiContext)
              1. the property datasource.
              2. the component where the field is presented.
        @return: Field the field suitable for editing the specified data.
        """
        raise NotImplementedError
