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

"""Defines a field that is used to enter secret text information like
passwords."""

from muntjac.ui.abstract_text_field import AbstractTextField
from muntjac.data.property import IProperty


class PasswordField(AbstractTextField):
    """A field that is used to enter secret text information like passwords.
    The entered text is not displayed on the screen.
    """

    CLIENT_WIDGET = None #ClientWidget(VPasswordField, LoadStyle.EAGER)

    def __init__(self, *args):
        """Constructs a PasswordField with caption and/or value/data source.

        @param args: tuple of the form
            - ()
            - (caption)
              1. the caption for the field
            - (dataSource)
              1. the property data source for the field
            - (caption, dataSource)
              1. the caption for the field
              2. the property data source for the field
            - (caption, value)
              1. the caption for the field
              2. the value for the field
        """
        super(PasswordField, self).__init__()

        nargs = len(args)
        if nargs == 0:
            self.setValue('')
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                dataSource, = args
                self.setPropertyDataSource(dataSource)
            else:
                caption, = args
                PasswordField.__init__(self)
                self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], IProperty):
                caption, dataSource = args
                PasswordField.__init__(self, dataSource)
                self.setCaption(caption)
            else:
                caption, value = args
                self.setValue(value)
                self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'
