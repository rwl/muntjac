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

from muntjac.data import property as prop

from muntjac.data.buffered import IBufferedValidatable

from muntjac.ui.component import \
    IFocusable, Event as ComponentEvent


class IField(IBufferedValidatable, prop.IValueChangeNotifier, # IComponent,
            prop.IValueChangeListener, prop.IEditor, IFocusable):
    """@author: Vaadin Ltd.
    @author: Richard Lincoln
    """

    def setCaption(self, caption):
        """Sets the Caption.
        """
        raise NotImplementedError


    def getDescription(self):
        raise NotImplementedError


    def setDescription(self, caption):
        """Sets the Description.
        """
        raise NotImplementedError


    def isRequired(self):
        """Is this field required.

        Required fields must filled by the user.

        @return: C{True} if the field is required, otherwise C{False}.
        """
        raise NotImplementedError


    def setRequired(self, required):
        """Sets the field required. Required fields must filled by the user.

        @param required:
                   Is the field required.
        """
        raise NotImplementedError


    def setRequiredError(self, requiredMessage):
        """Sets the error message to be displayed if a required field is
        empty.

        @param requiredMessage:
                   Error message.
        """
        raise NotImplementedError


    def getRequiredError(self):
        """Gets the error message that is to be displayed if a required
        field is empty.

        @return: Error message.
        """
        raise NotImplementedError


class ValueChangeEvent(ComponentEvent, prop.ValueChangeEvent):
    """An C{Event} object specifying the IField whose value has
    been changed.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, source):
        """Constructs a new event object with the specified source field
        object.

        @param source:
                   the field that caused the event.
        """
        super(ValueChangeEvent, self).__init__(source)


    def getProperty(self):
        """Gets the IProperty which triggered the event.

        @return: the Source IProperty of the event.
        """
        return self.getSource()
