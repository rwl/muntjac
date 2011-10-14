# -*- coding: utf-8 -*-
# from com.vaadin.data.Property.ValueChangeListener import (ValueChangeListener,)
# from com.vaadin.data.Property.ValueChangeNotifier import (ValueChangeNotifier,)
# from junit.framework.TestCase import (TestCase,)
# from org.easymock.EasyMock import (EasyMock,)


class AbstractTestFieldValueChange(TestCase):
    """Base class for tests for checking that value change listeners for fields are
    not called exactly once when they should be, and not at other times.
     *
    Does not check all cases (e.g. properties that do not implement
    {@link ValueChangeNotifier}).
     *
    Subclasses should implement {@link #setValue()} and call
    <code>super.setValue(AbstractField)</code>. Also, subclasses should typically
    override {@link #setValue(AbstractField)} to set the field value via
    <code>changeVariables()</code>.
    """
    _field = None
    _listener = None

    def setUp(self, field):
        self._field = field
        self._listener = EasyMock.createStrictMock(ValueChangeListener)

    def getListener(self):
        return self._listener

    def testRemoveListener(self):
        """Test that listeners are not called when they have been unregistered."""
        self.getFld().setPropertyDataSource(ObjectProperty(''))
        self.getFld().setWriteThrough(True)
        self.getFld().setReadThrough(True)
        # Expectations and start test
        self._listener.valueChange(EasyMock.isA(ValueChangeEvent))
        EasyMock.replay(self._listener)
        # Add listener and set the value -> should end up in listener once
        self.getFld().addListener(self._listener)
        self.setValue(self.getFld())
        # Ensure listener was called once
        EasyMock.verify(self._listener)
        # Remove the listener and set the value -> should not end up in
        # listener
        self.getFld().removeListener(self._listener)
        self.setValue(self.getFld())
        # Ensure listener still has been called only once
        EasyMock.verify(self._listener)

    def testWriteThroughReadThrough(self):
        """Common unbuffered case: both writeThrough (auto-commit) and readThrough
        are on. Calling commit() should not cause notifications.
             *
        Using the readThrough mode allows changes made to the property value to
        be seen in some cases also when there is no notification of value change
        from the property.
             *
        Field value change notifications closely mirror value changes of the data
        source behind the field.
        """
        self.getFld().setPropertyDataSource(ObjectProperty(''))
        self.getFld().setWriteThrough(True)
        self.getFld().setReadThrough(True)
        self.expectValueChangeFromSetValueNotCommit()

    def testNoWriteThroughNoReadThrough(self):
        """Fully buffered use where the data source is neither read nor modified
        during editing, and is updated at commit().
             *
        Field value change notifications reflect the buffered value in the field,
        not the original data source value changes.
        """
        self.getFld().setPropertyDataSource(ObjectProperty(''))
        self.getFld().setWriteThrough(False)
        self.getFld().setReadThrough(False)
        self.expectValueChangeFromSetValueNotCommit()

    def testWriteThroughNoReadThrough(self):
        """Less common partly buffered case: writeThrough (auto-commit) is on and
        readThrough is off. Calling commit() should not cause notifications.
             *
        Without readThrough activated, changes to the data source that do not
        cause notifications are not reflected by the field value.
             *
        Field value change notifications correspond to changes made to the data
        source value through the text field or the (notifying) property.
        """
        self.getFld().setPropertyDataSource(ObjectProperty(''))
        self.getFld().setWriteThrough(True)
        self.getFld().setReadThrough(False)
        self.expectValueChangeFromSetValueNotCommit()

    def testNoWriteThroughReadThrough(self):
        """Partly buffered use where the data source is read but not nor modified
        during editing, and is updated at commit().
             *
        When used like this, a field is updated from the data source if necessary
        when its value is requested and the property value has changed but the
        field has not been modified in its buffer.
             *
        Field value change notifications reflect the buffered value in the field,
        not the original data source value changes.
        """
        self.getFld().setPropertyDataSource(ObjectProperty(''))
        self.getFld().setWriteThrough(False)
        self.getFld().setReadThrough(True)
        self.expectValueChangeFromSetValueNotCommit()

    def expectValueChangeFromSetValueNotCommit(self):
        # Expectations and start test
        self._listener.valueChange(EasyMock.isA(ValueChangeEvent))
        EasyMock.replay(self._listener)
        # Add listener and set the value -> should end up in listener once
        self.getFld().addListener(self._listener)
        self.setValue(self.getFld())
        # Ensure listener was called once
        EasyMock.verify(self._listener)
        # commit
        self.getFld().commit()
        # Ensure listener was not called again
        EasyMock.verify(self._listener)

    def getFld(self):
        return self._field

    def setValue(self, field):
        """Override in subclasses to set value with changeVariables()."""
        field.setValue('newValue')
