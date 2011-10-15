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

from muntjac.test.server.components.AbstractTestFieldValueChange import \
    AbstractTestFieldValueChange

from muntjac.ui.text_field import TextField
from muntjac.data.util.object_property import ObjectProperty


class TestTextFieldValueChange(AbstractTestFieldValueChange):
    """Check that the value change listener for a text field is triggered
    exactly once when setting the value, at the correct time.
    """

    def setUp(self):
        super(TestTextFieldValueChange, self).setUp(TextField())


    def testNoDataSource(self):
        """Case where the text field only uses its internal buffer, no
        external property data source.
        """
        self.getField().setPropertyDataSource(None)
        self.expectValueChangeFromSetValueNotCommit()


    def setValue(self, field):
        variables = dict()
        variables['text'] = 'newValue'
        field.changeVariables(field, variables)


    def testValueChangeEventPropagationWithReadThrough(self):
        """Test that field propagates value change events originating from
        property, but don't fire value change events twice if value has only
        changed once.

        TODO make test field type agnostic (eg. combobox)
        """
        prop = ObjectProperty('')
        self.getField().setPropertyDataSource(prop)

        # defaults, buffering off
        self.getField().setWriteThrough(True)
        self.getField().setReadThrough(True)

        # Expectations and start test
        self.getListener().valueChange(EasyMock.isA(ValueChangeEvent))
        EasyMock.replay(self.getListener())

        # Add listener and set the value -> should end up in listener once
        self.getField().addListener(self.getListener())
        prop.setValue('Foo')

        # Ensure listener was called once
        EasyMock.verify(self.getListener())

        # get value should not fire value change again
        value = self.getField().getValue()
        self.assertEquals('Foo', value)

        # Ensure listener still has been called only once
        EasyMock.verify(self.getListener())


    def testValueChangePropagationWithReadThroughWithModifiedValue(self):
        """If read through is on and value has been modified, but not
        committed, the value should not propagate similar to
        {@link #testValueChangeEventPropagationWithReadThrough()}

        TODO make test field type agnostic (eg. combobox)
        """
        initialValue = 'initial'
        prop = ObjectProperty(initialValue)
        self.getField().setPropertyDataSource(prop)

        # write buffering on, read buffering off
        self.getField().setWriteThrough(False)
        self.getField().setReadThrough(True)

        # Expect no value changes calls to listener
        EasyMock.replay(self.getListener())

        # first set the value (note, write through false -> not forwarded to
        # property)
        self.setValue(self.getField())
        self.assertTrue(self.getField().isModified())

        # Add listener and set the value -> should end up in listener once
        self.getField().addListener(self.getListener())

        # modify property value, should not fire value change in field as the
        # field has uncommitted value (aka isModified() == true)
        prop.setValue('Foo')

        # Ensure listener was called once
        EasyMock.verify(self.getListener())

        # get value should not fire value change again
        value = self.getField().getValue()

        # Ensure listener still has been called only once
        EasyMock.verify(self.getListener())

        # field value should be different from the original value and current
        # proeprty value
        isValueEqualToInitial = value == initialValue
        self.assertFalse(isValueEqualToInitial)
        isValueEqualToPropertyValue = value == prop.getValue()
        self.assertFalse(isValueEqualToPropertyValue)

        # Ensure listener has not been called
        EasyMock.verify(self.getListener())


    def testValueChangePropagationWithReadThroughOff(self):
        """Value change events from property should not propagate if read
        through is false. Execpt when the property is being set.

        TODO make test field type agnostic (eg. combobox)
        """
        initialValue = 'initial'
        prop = ObjectProperty(initialValue)

        # set buffering
        self.getField().setWriteThrough(False)
        self.getField().setReadThrough(False)

        # Value change should only happen once, when setting the property,
        # further changes via property should not cause value change listener
        # in field to be notified
        self.getListener().valueChange(EasyMock.isA(ValueChangeEvent))
        EasyMock.replay(self.getListener())
        self.getField().addListener(self.getListener())
        self.getField().setPropertyDataSource(prop)

        # Ensure listener was called once
        EasyMock.verify(self.getListener())

        # modify property value, should not fire value change in field as the
        # read buffering is on (read through == false)
        prop.setValue('Foo')

        # Ensure listener still has been called only once
        EasyMock.verify(self.getListener())

        # get value should not fire value change again
        value = self.getField().getValue()

        # field value should be different from the original value and current
        # proeprty value
        isValueEqualToInitial = value == initialValue
        self.assertTrue(isValueEqualToInitial)

        # Ensure listener still has been called only once
        EasyMock.verify(self.getListener())
