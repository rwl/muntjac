# -*- coding: utf-8 -*-
from com.vaadin.tests.server.components.AbstractTestFieldValueChange import (AbstractTestFieldValueChange,)
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.data.util.ObjectProperty import (ObjectProperty,)
# from com.vaadin.ui.AbstractField import (AbstractField,)
# from com.vaadin.ui.TextField import (TextField,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)
# from junit.framework.Assert import (Assert,)
# from org.easymock.EasyMock import (EasyMock,)


class TestTextFieldValueChange(AbstractTestFieldValueChange):
    """Check that the value change listener for a text field is triggered exactly
    once when setting the value, at the correct time.
     *
    See <a href="http://dev.vaadin.com/ticket/4394">Ticket 4394</a>.
    """

    def setUp(self):
        super(TestTextFieldValueChange, self).setUp(TextField())

    def testNoDataSource(self):
        """Case where the text field only uses its internal buffer, no external
        property data source.
        """
        self.getFld().setPropertyDataSource(None)
        self.expectValueChangeFromSetValueNotCommit()

    def setValue(self, field):
        variables = dict()
        variables.put('text', 'newValue')
        field.changeVariables(field, variables)

    def testValueChangeEventPropagationWithReadThrough(self):
        """Test that field propagates value change events originating from property,
        but don't fire value change events twice if value has only changed once.
             *
             *
        TODO make test field type agnostic (eg. combobox)
        """
        property = ObjectProperty('')
        self.getFld().setPropertyDataSource(property)
        # defaults, buffering off
        self.getFld().setWriteThrough(True)
        self.getFld().setReadThrough(True)
        # Expectations and start test
        self.getListener().valueChange(EasyMock.isA(ValueChangeEvent))
        EasyMock.replay(self.getListener())
        # Add listener and set the value -> should end up in listener once
        self.getFld().addListener(self.getListener())
        property.setValue('Foo')
        # Ensure listener was called once
        EasyMock.verify(self.getListener())
        # get value should not fire value change again
        value = self.getFld().getValue()
        Assert.assertEquals('Foo', value)
        # Ensure listener still has been called only once
        EasyMock.verify(self.getListener())

    def testValueChangePropagationWithReadThroughWithModifiedValue(self):
        """If read through is on and value has been modified, but not committed, the
        value should not propagate similar to
        {@link #testValueChangeEventPropagationWithReadThrough()}
             *
        TODO make test field type agnostic (eg. combobox)
        """
        initialValue = 'initial'
        property = ObjectProperty(initialValue)
        self.getFld().setPropertyDataSource(property)
        # write buffering on, read buffering off
        self.getFld().setWriteThrough(False)
        self.getFld().setReadThrough(True)
        # Expect no value changes calls to listener
        EasyMock.replay(self.getListener())
        # first set the value (note, write through false -> not forwarded to
        # property)
        self.setValue(self.getFld())
        Assert.assertTrue(self.getFld().isModified())
        # Add listener and set the value -> should end up in listener once
        self.getFld().addListener(self.getListener())
        # modify property value, should not fire value change in field as the
        # field has uncommitted value (aka isModified() == true)
        property.setValue('Foo')
        # Ensure listener was called once
        EasyMock.verify(self.getListener())
        # get value should not fire value change again
        value = self.getFld().getValue()
        # Ensure listener still has been called only once
        EasyMock.verify(self.getListener())
        # field value should be different from the original value and current
        # proeprty value
        isValueEqualToInitial = value == initialValue
        Assert.assertFalse(isValueEqualToInitial)
        isValueEqualToPropertyValue = value == property.getValue()
        Assert.assertFalse(isValueEqualToPropertyValue)
        # Ensure listener has not been called
        EasyMock.verify(self.getListener())

    def testValueChangePropagationWithReadThroughOff(self):
        """Value change events from property should not propagate if read through is
        false. Execpt when the property is being set.
             *
        TODO make test field type agnostic (eg. combobox)
        """
        initialValue = 'initial'
        property = ObjectProperty(initialValue)
        # set buffering
        self.getFld().setWriteThrough(False)
        self.getFld().setReadThrough(False)
        # Value change should only happen once, when setting the property,
        # further changes via property should not cause value change listener
        # in field to be notified
        self.getListener().valueChange(EasyMock.isA(ValueChangeEvent))
        EasyMock.replay(self.getListener())
        self.getFld().addListener(self.getListener())
        self.getFld().setPropertyDataSource(property)
        # Ensure listener was called once
        EasyMock.verify(self.getListener())
        # modify property value, should not fire value change in field as the
        # read buffering is on (read through == false)
        property.setValue('Foo')
        # Ensure listener still has been called only once
        EasyMock.verify(self.getListener())
        # get value should not fire value change again
        value = self.getFld().getValue()
        # field value should be different from the original value and current
        # proeprty value
        isValueEqualToInitial = value == initialValue
        Assert.assertTrue(isValueEqualToInitial)
        # Ensure listener still has been called only once
        EasyMock.verify(self.getListener())
