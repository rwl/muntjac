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

from muntjac.ui.IComponent import IComponent, IFocusable, Event as ComponentEvent
from muntjac.data.BufferedValidatable import BufferedValidatable
from muntjac.data.Property import Property, ValueChangeEvent,\
    ValueChangeNotifier, ValueChangeListener, Editor


class IField(IComponent, BufferedValidatable, Property, ValueChangeNotifier,
            ValueChangeListener, Editor, IFocusable):
    """@author IT Mill Ltd."""

    def setCaption(self, caption):
        """Sets the Caption.

        @param caption
        """
        raise NotImplementedError


    def getDescription(self):
        raise NotImplementedError


    def setDescription(self, caption):
        """Sets the Description.

        @param caption
        """
        raise NotImplementedError


    def isRequired(self):
        """Is this field required.

        Required fields must filled by the user.

        @return <code>true</code> if the field is required,otherwise
                <code>false</code>.
        @since 3.1
        """
        raise NotImplementedError


    def setRequired(self, required):
        """Sets the field required. Required fields must filled by the user.

        @param required
                   Is the field required.
        @since 3.1
        """
        raise NotImplementedError


    def setRequiredError(self, requiredMessage):
        """Sets the error message to be displayed if a required field is empty.

        @param requiredMessage
                   Error message.
        @since 5.2.6
        """
        raise NotImplementedError


    def getRequiredError(self):
        """Gets the error message that is to be displayed if a required field is
        empty.

        @return Error message.
        @since 5.2.6
        """
        raise NotImplementedError


class ValueChangeEvent(ComponentEvent, Property, ValueChangeEvent):
    """An <code>Event</code> object specifying the IField whose value has been
    changed.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, source):
        """Constructs a new event object with the specified source field object.

        @param source
                   the field that caused the event.
        """
        super(ValueChangeEvent, self)(source)


    def getProperty(self):
        """Gets the Property which triggered the event.

        @return the Source Property of the event.
        """
        return self.getSource()
