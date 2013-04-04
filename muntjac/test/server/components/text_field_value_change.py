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

import mox
import unittest

from muntjac.test.server.components import abstract_test_field_value_change

from muntjac.ui.text_field import TextField
from muntjac.data.util.object_property import ObjectProperty
from muntjac.data.property import ValueChangeEvent, IValueChangeListener


class TestTextFieldValueChange(
            abstract_test_field_value_change.AbstractTestFieldValueChange):
    """Check that the value change listener for a text field is triggered
    exactly once when setting the value, at the correct time.
    """

    def setUp(self):
        super(TestTextFieldValueChange, self).setUp(TextField())


    def setValue(self, field):
        variables = dict()
        variables['text'] = 'newValue'
        field.changeVariables(field, variables)


    def testNoDataSource(self):
        """Case where the text field only uses its internal buffer, no
        external property data source.
        """
        self.getField().setPropertyDataSource(None)
        self.expectValueChangeFromSetValueNotCommit()


    def testValueChangeEventPropagationWithReadThrough(self):
        """Test that field propagates value change events originating from
        property, but don't fire value change events twice if value has only
        changed once.

        TODO: make test field type agnostic (eg. combobox)
        """
        prop = ObjectProperty('')
        self.getField().setPropertyDataSource(prop)

        # defaults, buffering off
        self.getField().setWriteThrough(True)
        self.getField().setReadThrough(True)

        # Expectations and start test
        self.getListener().valueChange(mox.IsA(ValueChangeEvent))
        mox.Replay(self.getListener())

        # Add listener and set the value -> should end up in listener once
        self.getField().addListener(self.getListener(), IValueChangeListener)
        prop.setValue('Foo')

        # Ensure listener was called once
        mox.Verify(self.getListener())

        # get value should not fire value change again
        value = self.getField().getValue()
        self.assertEquals('Foo', value)

        # Ensure listener still has been called only once
        mox.Verify(self.getListener())


    def testValueChangePropagationWithReadThroughWithModifiedValue(self):
        """If read through is on and value has been modified, but not
        committed, the value should not propagate similar to
        L{#testValueChangeEventPropagationWithReadThrough()}

        TODO: make test field type agnostic (eg. combobox)
        """
        initialValue = 'initial'
        prop = ObjectProperty(initialValue)
        self.getField().setPropertyDataSource(prop)

        # write buffering on, read buffering off
        self.getField().setWriteThrough(False)
        self.getField().setReadThrough(True)

        # Expect no value changes calls to listener
        mox.Replay(self.getListener())

        # first set the value (note, write through false -> not forwarded to
        # property)
        self.setValue(self.getField())
        self.assertTrue(self.getField().isModified())

        # Add listener and set the value -> should end up in listener once
        self.getField().addListener(self.getListener(), IValueChangeListener)

        # modify property value, should not fire value change in field as the
        # field has uncommitted value (aka isModified() == true)
        prop.setValue('Foo')

        # Ensure listener was called once
        mox.Verify(self.getListener())

        # get value should not fire value change again
        value = self.getField().getValue()

        # Ensure listener still has been called only once
        mox.Verify(self.getListener())

        # field value should be different from the original value and current
        # proeprty value
        isValueEqualToInitial = value == initialValue
        self.assertFalse(isValueEqualToInitial)
        isValueEqualToPropertyValue = value == prop.getValue()
        self.assertFalse(isValueEqualToPropertyValue)

        # Ensure listener has not been called
        mox.Verify(self.getListener())


    def testValueChangePropagationWithReadThroughOff(self):
        """Value change events from property should not propagate if read
        through is false. Execpt when the property is being set.

        TODO: make test field type agnostic (eg. combobox)
        """
        initialValue = 'initial'
        prop = ObjectProperty(initialValue)

        # set buffering
        self.getField().setWriteThrough(False)
        self.getField().setReadThrough(False)

        # Value change should only happen once, when setting the property,
        # further changes via property should not cause value change listener
        # in field to be notified
        self.getListener().valueChange(mox.IsA(ValueChangeEvent))
        mox.Replay(self.getListener())
        self.getField().addListener(self.getListener(), IValueChangeListener)
        self.getField().setPropertyDataSource(prop)

        # Ensure listener was called once
        mox.Verify(self.getListener())

        # modify property value, should not fire value change in field as the
        # read buffering is on (read through == false)
        prop.setValue('Foo')

        # Ensure listener still has been called only once
        mox.Verify(self.getListener())

        # get value should not fire value change again
        value = self.getField().getValue()

        # field value should be different from the original value and current
        # proeprty value
        isValueEqualToInitial = value == initialValue
        self.assertTrue(isValueEqualToInitial)

        # Ensure listener still has been called only once
        mox.Verify(self.getListener())


if __name__ == '__main__':
    unittest.main()
