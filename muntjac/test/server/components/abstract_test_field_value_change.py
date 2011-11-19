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

import mox

from unittest import TestCase

from muntjac.data.property import IValueChangeListener, ValueChangeEvent
from muntjac.data.util.object_property import ObjectProperty


class AbstractTestFieldValueChange(TestCase):
    """Base class for tests for checking that value change listeners for
    fields are not called exactly once when they should be, and not at
    other times.

    Does not check all cases (e.g. properties that do not implement
    L{ValueChangeNotifier}).

    Subclasses should implement L{#setValue()} and call super C{setValue}.
    Also, subclasses should typically override L{setValue} to set the field
    value via C{changeVariables()}.
    """

    def setUp(self, field):
        TestCase.setUp(self)

        self._field = field
        self.mox = mox.Mox()
        self._listener = self.mox.CreateMock(IValueChangeListener)


    def getListener(self):
        return self._listener


    def testRemoveListener(self):
        """Test that listeners are not called when they have been
        unregistered."""
        self.getField().setPropertyDataSource(ObjectProperty(''))
        self.getField().setWriteThrough(True)
        self.getField().setReadThrough(True)

        # Expectations and start test
        self._listener.valueChange(mox.IsA(ValueChangeEvent))
        mox.Replay(self._listener)

        # Add listener and set the value -> should end up in listener once
        self.getField().addListener(self._listener, IValueChangeListener)
        self.setValue(self.getField())

        # Ensure listener was called once
        mox.Verify(self._listener)

        # Remove the listener and set the value -> should not end up in
        # listener
        self.getField().removeListener(self._listener, IValueChangeListener)
        self.setValue(self.getField())

        # Ensure listener still has been called only once
        mox.Verify(self._listener)


    def testWriteThroughReadThrough(self):
        """Common unbuffered case: both writeThrough (auto-commit) and
        readThrough are on. Calling commit() should not cause notifications.

        Using the readThrough mode allows changes made to the property value
        to be seen in some cases also when there is no notification of value
        change from the property.

        Field value change notifications closely mirror value changes of the
        data source behind the field.
        """
        self.getField().setPropertyDataSource(ObjectProperty(''))
        self.getField().setWriteThrough(True)
        self.getField().setReadThrough(True)
        self.expectValueChangeFromSetValueNotCommit()


    def testNoWriteThroughNoReadThrough(self):
        """Fully buffered use where the data source is neither read nor
        modified during editing, and is updated at commit().

        Field value change notifications reflect the buffered value in the
        field, not the original data source value changes.
        """
        self.getField().setPropertyDataSource(ObjectProperty(''))
        self.getField().setWriteThrough(False)
        self.getField().setReadThrough(False)
        self.expectValueChangeFromSetValueNotCommit()


    def testWriteThroughNoReadThrough(self):
        """Less common partly buffered case: writeThrough (auto-commit) is
        on and readThrough is off. Calling commit() should not cause
        notifications.

        Without readThrough activated, changes to the data source that do
        not cause notifications are not reflected by the field value.

        Field value change notifications correspond to changes made to the
        data source value through the text field or the (notifying) property.
        """
        self.getField().setPropertyDataSource(ObjectProperty(''))
        self.getField().setWriteThrough(True)
        self.getField().setReadThrough(False)
        self.expectValueChangeFromSetValueNotCommit()


    def testNoWriteThroughReadThrough(self):
        """Partly buffered use where the data source is read but not nor
        modified during editing, and is updated at commit().

        When used like this, a field is updated from the data source if
        necessary when its value is requested and the property value has
        changed but the field has not been modified in its buffer.

        Field value change notifications reflect the buffered value in the
        field, not the original data source value changes.
        """
        self.getField().setPropertyDataSource(ObjectProperty(''))
        self.getField().setWriteThrough(False)
        self.getField().setReadThrough(True)
        self.expectValueChangeFromSetValueNotCommit()


    def expectValueChangeFromSetValueNotCommit(self):
        # Expectations and start test
        self._listener.valueChange(mox.IsA(ValueChangeEvent))
        mox.Replay(self._listener)

        # Add listener and set the value -> should end up in listener once
        self.getField().addListener(self._listener, IValueChangeListener)
        self.setValue(self.getField())

        # Ensure listener was called once
        mox.Verify(self._listener)

        # commit
        self.getField().commit()

        # Ensure listener was not called again
        mox.Verify(self._listener)


    def getField(self):
        return self._field


    def setValue(self, field):
        """Override in subclasses to set value with changeVariables()."""
        field.setValue('newValue')
