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

from warnings import warn

from muntjac.event.shortcut_listener import ShortcutListener
from muntjac.event.action_manager import ActionManager

from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.component import Event as ComponentEvent

from muntjac.event import action
from muntjac.ui import field
from muntjac.data import property as prop

from muntjac.data.validator import EmptyValueException
from muntjac.data.buffered import SourceException
from muntjac.data.validator import InvalidValueException
from muntjac.data.validatable import IValidatable

from muntjac.terminal.composite_error_message import CompositeErrorMessage


_VALUE_CHANGE_METHOD = getattr(prop.IValueChangeListener, 'valueChange')

_READ_ONLY_STATUS_CHANGE_METHOD = getattr(prop.IReadOnlyStatusChangeListener,
        'readOnlyStatusChange')


class AbstractField(AbstractComponent, field.IField,
            action.IShortcutNotifier, prop.IReadOnlyStatusChangeNotifier,
            prop.IReadOnlyStatusChangeListener):
    """Abstract field component for implementing buffered property editors.
    The field may hold an internal value, or it may be connected to any data
    source that implements the {@link com.vaadin.data.IProperty}interface.
    <code>AbstractField</code> implements that interface itself, too, so
    accessing the IProperty value represented by it is straightforward.

    AbstractField also provides the {@link com.vaadin.data.Buffered}
    interface for buffering the data source value. By default the IField is
    in write through-mode and {@link #setWriteThrough(boolean)}should be
    called to enable buffering.

    The class also supports {@link com.vaadin.data.Validator validators} to
    make sure the value contained in the field is valid.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self):
        super(AbstractField, self).__init__()

        # Value of the abstract field.
        self._value = None

        # Connected data-source.
        self._dataSource = None

        # The list of validators.
        self._validators = None

        # Auto commit mode.
        self._writeThroughMode = True

        # Reads the value from data-source, when it is not modified.
        self._readThroughMode = True

        # Is the field modified but not committed.
        self._modified = False

        # Should value change event propagation from property data source
        # to listeners of the field be suppressed. This is used internally
        # while the field makes changes to the property value.
        self._suppressValueChangePropagation = False

        # Current source exception.
        self._currentBufferedSourceException = None

        # Are the invalid values allowed in fields ?
        self._invalidAllowed = True

        # Are the invalid values committed ?
        self._invalidCommitted = False

        # The tab order number of this field.
        self._tabIndex = 0

        # Required field.
        self._required = False

        # The error message for the exception that is thrown when the field
        # is required but empty.
        self._requiredError = ''

        # Is automatic validation enabled.
        self._validationVisible = True

        # Keeps track of the Actions added to this component; the actual
        # handling/notifying is delegated, usually to the containing window.
        self._actionManager = None


    def paintContent(self, target):

        # The tab ordering number
        if self.getTabIndex() != 0:
            target.addAttribute('tabindex', self.getTabIndex())

        # If the field is modified, but not committed, set modified attribute
        if self.isModified():
            target.addAttribute('modified', True)

        # Adds the required attribute
        if not self.isReadOnly() and self.isRequired():
            target.addAttribute('required', True)

        # Hide the error indicator if needed
        if self.isRequired() and self.isEmpty() \
                and self.getComponentError() is None \
                and self.getErrorMessage() is not None:
            target.addAttribute('hideErrors', True)


    def getType(self):
        # Gets the field type
        raise NotImplementedError


    def isReadOnly(self):
        """The abstract field is read only also if the data source is in
        read only mode.
        """
        return (super(AbstractField, self).isReadOnly()
                or (self._dataSource is not None
                    and self._dataSource.isReadOnly()))


    def setReadOnly(self, readOnly):
        """Changes the readonly state and throw read-only status change
        events.

        @see com.vaadin.ui.Component#setReadOnly(boolean)
        """
        super(AbstractField, self).setReadOnly(readOnly)
        self.fireReadOnlyStatusChange()


    def isInvalidCommitted(self):
        """Tests if the invalid data is committed to datasource.

        @see com.vaadin.data.BufferedValidatable#isInvalidCommitted()
        """
        return self._invalidCommitted


    def setInvalidCommitted(self, isCommitted):
        """Sets if the invalid data should be committed to datasource.

        @see muntjac.data.BufferedValidatable#setInvalidCommitted(boolean)
        """
        self._invalidCommitted = isCommitted


    def commit(self):
        # Saves the current value to the data source.
        if (self._dataSource is not None
                and not self._dataSource.isReadOnly()):

            if self.isInvalidCommitted() or self.isValid():
                newValue = self.getValue()
                try:
                    # Commits the value to datasource.
                    self._suppressValueChangePropagation = True
                    self._dataSource.setValue(newValue)

                except Exception, e:
                    # Sets the buffering state.
                    exception = SourceException(self, e)
                    self._currentBufferedSourceException = exception
                    self.requestRepaint()

                    # Throws the source exception.
                    raise self._currentBufferedSourceException
                finally:
                    self._suppressValueChangePropagation = False

            else:
                # An invalid value and we don't allow
                # them, throw the exception
                self.validate()

        repaintNeeded = False

        # The abstract field is not modified anymore
        if self._modified:
            self._modified = False
            repaintNeeded = True

        # If successful, remove set the buffering state to be ok
        if self._currentBufferedSourceException is not None:
            self._currentBufferedSourceException = None
            repaintNeeded = True

        if repaintNeeded:
            self.requestRepaint()


    def discard(self):
        # Updates the value from the data source.
        if self._dataSource is not None:

            # Gets the correct value from datasource
            try:
                # Discards buffer by overwriting from datasource
                if self.getType() == str:
                    newValue = str(self._dataSource)
                else:
                    self._dataSource.getValue()

                # If successful, remove set the buffering state to be ok
                if self._currentBufferedSourceException is not None:
                    self._currentBufferedSourceException = None
                    self.requestRepaint()

            except Exception, e:
                # Sets the buffering state
                exception = SourceException(self, e)
                self._currentBufferedSourceException = exception
                self.requestRepaint()

                # Throws the source exception
                raise self._currentBufferedSourceException

            wasModified = self.isModified()
            self._modified = False

            # If the new value differs from the previous one
            if ((newValue is None and self._value is not None)
                    or (newValue is not None
                        and not (newValue == self._value))):
                self.setInternalValue(newValue)
                self.fireValueChange(False)

            elif wasModified:
                # If the value did not change, but
                # the modification status did
                self.requestRepaint()


    def isModified(self):
        # Has the field been modified since the last commit()?
        return self._modified


    def isWriteThrough(self):
        # Tests if the field is in write-through mode.
        return self._writeThroughMode


    def setWriteThrough(self, writeThrough):
        # Sets the field's write-through mode to the specified status
        if self._writeThroughMode == writeThrough:
            return

        self._writeThroughMode = writeThrough

        if self._writeThroughMode:
            self.commit()


    def isReadThrough(self):
        # Tests if the field is in read-through mode.
        return self._readThroughMode


    def setReadThrough(self, readThrough):
        # Sets the field's read-through mode to the specified status
        if self._readThroughMode == readThrough:
            return

        self._readThroughMode = readThrough

        if (not self.isModified() and self._readThroughMode
                and (self._dataSource is not None)):
            if self.getType() == str:
                self.setInternalValue( str(self._dataSource) )
            else:
                self.setInternalValue(self._dataSource.getValue())

            self.fireValueChange(False)


    def __str__(self):
        """Returns the value of the IProperty in human readable textual
        format.
        """
        value = self.getValue()
        if value is None:
            return None
        return str( self.getValue() )


    def getValue(self):
        """Gets the current value of the field.

        This is the visible, modified and possible invalid value the user
        have entered to the field. In the read-through mode, the abstract
        buffer is also updated and validation is performed.

        Note that the object returned is compatible with getType(). For
        example, if the type is String, this returns Strings even when the
        underlying datasource is of some other type. In order to access the
        datasources native type, use getPropertyDatasource().getValue()
        instead.

        Note that when you extend AbstractField, you must reimplement this
        method if datasource.getValue() is not assignable to class returned
        by getType() AND getType() is not String. In case of Strings,
        getValue() calls datasource.toString() instead of
        datasource.getValue().

        @return the current value of the field.
        """
        # Give the value from abstract buffers if the field if possible
        if (self._dataSource is None or (not self.isReadThrough())
                or self.isModified()):
            return self._value

        if self.getType() == str:
            newValue = str(self._dataSource)
        else:
            newValue = self._dataSource.getValue()

        return newValue


    def setValue(self, newValue, repaintIsNotNeeded=False):
        """Sets the value of the field.

        @param newValue
                   the New value of the field.
        @param repaintIsNotNeeded
                   True iff caller is sure that repaint is not needed.
        @throws property.ReadOnlyException
        @throws property.ConversionException
        """
        if ((newValue is None and self._value is not None)
                or (newValue is not None
                    and not (newValue == self._value))):

            # Read only fields can not be changed
            if self.isReadOnly():
                raise prop.ReadOnlyException()

            # Repaint is needed even when the client thinks that it knows
            # the new state if validity of the component may change
            if (repaintIsNotNeeded and self.isRequired()
                    or (self.getValidators() is not None)):
                repaintIsNotNeeded = False

            # If invalid values are not allowed, the value must be checked
            if not self.isInvalidAllowed():
                for v in self.getValidators():
                    v.validate(newValue)

            # Changes the value
            self.setInternalValue(newValue)
            self._modified = self._dataSource is not None

            # In write through mode , try to commit
            if (self.isWriteThrough() and (self._dataSource is not None)
                    and (self.isInvalidCommitted() or self.isValid())):
                try:

                    # Commits the value to datasource
                    self._suppressValueChangePropagation = True
                    self._dataSource.setValue(newValue)

                    # The buffer is now unmodified
                    self._modified = False

                except Exception, e:
                    # Sets the buffering state
                    exception = SourceException(self, e)
                    self._currentBufferedSourceException = exception
                    self.requestRepaint()

                    # Throws the source exception
                    raise self._currentBufferedSourceException
                finally:
                    self._suppressValueChangePropagation = False

            # If successful, remove set the buffering state to be ok
            if self._currentBufferedSourceException is not None:
                self._currentBufferedSourceException = None
                self.requestRepaint()

            # Fires the value change
            self.fireValueChange(repaintIsNotNeeded)


    def getPropertyDataSource(self):
        """Gets the current data source of the field, if any.

        @return the current data source as a IProperty, or <code>null</code>
                if none defined.
        """
        return self._dataSource


    def setPropertyDataSource(self, newDataSource):
        """Sets the specified IProperty as the data source for the field.
        All uncommitted changes are replaced with a value from the new data
        source.

        If the datasource has any validators, the same validators are added
        to the field. Because the default behavior of the field is to allow
        invalid values, but not to allow committing them, this only adds
        visual error messages to fields and do not allow committing them as
        long as the value is invalid. After the value is valid, the error
        message is not shown and the commit can be done normally.

        Note: before 6.5 we actually called discard() method in the beginning
        of the method. This was removed to simplify implementation, avoid
        excess calls to backing property and to avoid odd value change events
        that were previously fired (developer expects 0-1 value change events
        if this method is called). Some complex field implementations might
        now need to override this method to do housekeeping similar to
        discard().

        @param newDataSource
                   the new data source property.
        """
        # Saves the old value
        oldValue = self._value

        # Stops listening the old data source changes
        if (self._dataSource is not None \
                and issubclass(self._dataSource,
                        prop.IValueChangeNotifier)):

            self._dataSource.removeListener(self)


        if (self._dataSource is not None \
                and issubclass(self._dataSource,
                        prop.IReadOnlyStatusChangeNotifier)):

            self._dataSource.removeListener(self)


        # Sets the new data source
        self._dataSource = newDataSource

        # Gets the value from source
        try:
            if self._dataSource is not None:
                if self.getType() == str:
                    self.setInternalValue( str(self._dataSource) )
                else:
                    self.setInternalValue(self._dataSource.getValue())
            self._modified = False
        except Exception, e:
            exception = SourceException(self, e)
            self._currentBufferedSourceException = exception
            self._modified = True

        # Listens the new data source if possible
        if isinstance(self._dataSource, prop.IValueChangeNotifier):
            self._dataSource.addListener(self)

        if isinstance(self._dataSource,
                prop.IReadOnlyStatusChangeNotifier):
            self._dataSource.addListener(self)

        # Copy the validators from the data source
        if isinstance(self._dataSource, IValidatable):
            validators = self._dataSource.getValidators()
            if validators is not None:
                for v in validators:
                    self.addValidator(v)

        # Fires value change if the value has changed
        if ((self._value != oldValue)
                and (self._value is not None
                     and not (self._value == oldValue))
                or (self._value is None)):

            self.fireValueChange(False)


    def addValidator(self, validator):
        """Adds a new validator for the field's value. All validators added
        to a field are checked each time the its value changes.

        @param validator
                   the new validator to be added.
        """
        if self._validators is None:
            self._validators = list()
        self._validators.append(validator)
        self.requestRepaint()


    def getValidators(self):
        """Gets the validators of the field.

        @return the Unmodifiable collection that holds all validators for
                the field.
        """
        if self._validators is None or len(self._validators) == 0:
            return None

        return self._validators


    def removeValidator(self, validator):
        """Removes the validator from the field.

        @param validator
                   the validator to remove.
        """
        if self._validators is not None:
            self._validators.remove(validator)

        self.requestRepaint()


    def isValid(self):
        """Tests the current value against registered validators if the
        field is not empty. If the field is empty it is considered valid
        if it is not required and invalid otherwise. Validators are never
        checked for empty fields.

        @return <code>true</code> if all registered validators claim that
                the current value is valid or if the field is empty and
                not required, <code>false</code> otherwise.
        """
        if self.isEmpty():
            if self.isRequired():
                return False
            else:
                return True

        if self._validators is None:
            return True

        value = self.getValue()
        for v in self._validators:
            if not v.isValid(value):
                return False

        return True


    def validate(self):
        """Checks the validity of the IValidatable by validating the field
        with all attached validators except when the field is empty. An
        empty field is invalid if it is required and valid otherwise.

        The "required" validation is a built-in validation feature. If
        the field is required, but empty, validation will throw an
        EmptyValueException with the error message set with
        setRequiredError().

        @see com.vaadin.data.IValidatable#validate()
        """
        if self.isEmpty():
            if self.isRequired():
                raise EmptyValueException(self._requiredError)
            else:
                return

        # If there is no validator, there can not be any errors
        if self._validators is None:
            return

        # Initialize temps
        firstError = None
        errors = None
        value = self.getValue()

        # Gets all the validation errors
        for v in self._validators:
            try:
                v.validate(value)
            except InvalidValueException, e:
                if firstError is None:
                    firstError = e
                else:
                    if errors is None:
                        errors = list()
                        errors.append(firstError)
                    errors.append(e)

        # If there were no error
        if firstError is None:
            return

        # If only one error occurred, throw it forwards
        if errors is None:
            raise firstError

        # Creates composite validator
        exceptions = [None] * len(errors)
        index = 0
        for e in errors:
            exceptions[index] = e
            index += 1

        raise InvalidValueException(None, exceptions)


    def isInvalidAllowed(self):
        """Fields allow invalid values by default. In most cases this is
        wanted, because the field otherwise visually forget the user input
        immediately.

        @return true iff the invalid values are allowed.
        @see com.vaadin.data.IValidatable#isInvalidAllowed()
        """
        return self._invalidAllowed


    def setInvalidAllowed(self, invalidAllowed):
        """Fields allow invalid values by default. In most cases this is
        wanted, because the field otherwise visually forget the user input
        immediately.

        In common setting where the user wants to assure the correctness of
        the datasource, but allow temporarily invalid contents in the field,
        the user should add the validators to datasource, that should not
        allow invalid values. The validators are automatically copied to the
        field when the datasource is set.

        @see com.vaadin.data.IValidatable#setInvalidAllowed(boolean)
        """
        self._invalidAllowed = invalidAllowed


    def getErrorMessage(self):
        """Error messages shown by the fields are composites of the error
        message thrown by the superclasses (that is the component error
        message), validation errors and buffered source errors.

        @see com.vaadin.ui.AbstractComponent#getErrorMessage()
        """
        # Check validation errors only if automatic validation is enabled.
        # Empty, required fields will generate a validation error containing
        # the requiredError string. For these fields the exclamation mark
        # will be hidden but the error must still be sent to the client.
        validationError = None
        if self.isValidationVisible():
            try:
                self.validate()
            except InvalidValueException, e:
                if not e.isInvisible():
                    validationError = e

        # Check if there are any systems errors
        superError = super(AbstractField, self).getErrorMessage()

        # Return if there are no errors at all
        if (superError is None and validationError is None
                and self._currentBufferedSourceException is None):
            return None

        # Throw combination of the error types
        return CompositeErrorMessage([superError, validationError,
                self._currentBufferedSourceException])


    def addListener(self, listener):
        # Adds a value change listener for the field.
        if isinstance(listener, prop.IReadOnlyStatusChangeListener):
            AbstractComponent.addListener(self,
                    prop.IReadOnlyStatusChangeEvent, listener,
                    _READ_ONLY_STATUS_CHANGE_METHOD)
        else:
            AbstractComponent.addListener(self, field.ValueChangeEvent,
                    listener, _VALUE_CHANGE_METHOD)


    def removeListener(self, listener):
        # Removes a value change listener from the field.
        if isinstance(listener, prop.IReadOnlyStatusChangeListener):
            AbstractComponent.removeListener(self,
                    prop.IReadOnlyStatusChangeEvent, listener,
                    _READ_ONLY_STATUS_CHANGE_METHOD)
        else:
            AbstractComponent.removeListener(self, field.ValueChangeEvent,
                    listener, _VALUE_CHANGE_METHOD)


    def fireValueChange(self, repaintIsNotNeeded):
        """Emits the value change event. The value contained in the
        field is validated before the event is created.
        """
        self.fireEvent( field.ValueChangeEvent(self) )
        if not repaintIsNotNeeded:
            self.requestRepaint()


    def readOnlyStatusChange(self, event):
        """React to read only status changes of the property by
        requesting a repaint.

        @see property.IReadOnlyStatusChangeListener
        """
        self.requestRepaint()


    def fireReadOnlyStatusChange(self):
        """Emits the read-only status change event. The value contained
        in the field is validated before the event is created.
        """
        self.fireEvent( IReadOnlyStatusChangeEvent(self) )


    def valueChange(self, event):
        """This method listens to data source value changes and passes
        the changes forwards.

        Changes are not forwarded to the listeners of the field during
        internal operations of the field to avoid duplicate notifications.

        @param event
                   the value change event telling the data source
                   contents have changed.
        """
        if (not self._suppressValueChangePropagation
                and (self.isReadThrough() and not self.isModified())):
            self.setInternalValue( event.getProperty().getValue() )
            self.fireValueChange(False)


    def changeVariables(self, source, variables):
        super(AbstractField, self).changeVariables(source, variables)


    def focus(self):
        super(AbstractField, self).focus()


    @classmethod
    def constructField(cls, propertyType):
        """Creates abstract field by the type of the property.

        This returns most suitable field type for editing property of
        given type.

        @param propertyType
                   the Type of the property, that needs to be edited.
        @deprecated use e.g.
                {@link DefaultFieldFactory#createFieldByPropertyType(Class)}
                instead
        """
        warn('use createFieldByPropertyType() instead', DeprecationWarning)

        # FIXME: circular import
        from muntjac.ui.default_field_factory import DefaultFieldFactory

        return DefaultFieldFactory.createFieldByPropertyType(propertyType)


    def getTabIndex(self):
        return self._tabIndex


    def setTabIndex(self, tabIndex):
        self._tabIndex = tabIndex
        self.requestRepaint()


    def setInternalValue(self, newValue):
        """Sets the internal field value. This is purely used by
        AbstractField to change the internal IField value. It does not
        trigger valuechange events. It can be overridden by the inheriting
        classes to update all dependent variables.

        @param newValue
                   the new value to be set.
        """
        self._value = newValue
        if self._validators is not None and len(self._validators) > 0:
            self.requestRepaint()


    def attach(self):
        """Notifies the component that it is connected to an application.

        @see com.vaadin.ui.Component#attach()
        """
        super(AbstractField, self).attach()
        if self._actionManager is not None:
            self._actionManager.setViewer(self.getWindow())


    def detach(self):
        super(AbstractField, self).detach()
        if self._actionManager is not None:
            self._actionManager.setViewer(None)


    def isRequired(self):
        """Is this field required. Required fields must filled by the user.

        If the field is required, it is visually indicated in the user
        interface. Furthermore, setting field to be required implicitly
        adds "non-empty" validator and thus isValid() == false or any
        isEmpty() fields. In those cases validation errors are not painted
        as it is obvious that the user must fill in the required fields.

        On the other hand, for the non-required fields isValid() == true
        if the field isEmpty() regardless of any attached validators.

        @return <code>true</code> if the field is required .otherwise
                <code>false</code>.
        """
        return self._required


    def setRequired(self, required):
        """Sets the field required. Required fields must filled by the user.

        If the field is required, it is visually indicated in the user
        interface. Furthermore, setting field to be required implicitly adds
        "non-empty" validator and thus isValid() == false or any isEmpty()
        fields. In those cases validation errors are not painted as it is
        obvious that the user must fill in the required fields.

        On the other hand, for the non-required fields isValid() == true if
        the field isEmpty() regardless of any attached validators.

        @param required
                   Is the field required.
        """
        self._required = required
        self.requestRepaint()


    def setRequiredError(self, requiredMessage):
        """Set the error that is show if this field is required, but empty.
        When setting requiredMessage to be "" or null, no error pop-up or
        exclamation mark is shown for a empty required field. This faults
        to "". Even in those cases isValid() returns false for empty
        required fields.

        @param requiredMessage
                   Message to be shown when this field is required, but
                   empty.
        """
        self._requiredError = requiredMessage
        self.requestRepaint()


    def getRequiredError(self):
        return self._requiredError


    def isEmpty(self):
        """Is the field empty?

        In general, "empty" state is same as null. As an exception,
        TextField also treats empty string as "empty".
        """
        return self.getValue() is None


    def isValidationVisible(self):
        """Is automatic, visible validation enabled?

        If automatic validation is enabled, any validators connected to
        this component are evaluated while painting the component and
        potential error messages are sent to client. If the automatic
        validation is turned off, isValid() and validate() methods still
        work, but one must show the validation in their own code.

        @return True, if automatic validation is enabled.
        """
        return self._validationVisible


    def setValidationVisible(self, validateAutomatically):
        """Enable or disable automatic, visible validation.

        If automatic validation is enabled, any validators connected to
        this component are evaluated while painting the component and
        potential error messages are sent to client. If the automatic
        validation is turned off, isValid() and validate() methods still
        work, but one must show the validation in their own code.

        @param validateAutomatically
                   True, if automatic validation is enabled.
        """
        if self._validationVisible != validateAutomatically:
            self.requestRepaint()
            self._validationVisible = validateAutomatically


    def setCurrentBufferedSourceException(self,
                currentBufferedSourceException):
        """Sets the current buffered source exception.

        @param currentBufferedSourceException
        """
        self._currentBufferedSourceException = currentBufferedSourceException
        self.requestRepaint()


    def getActionManager(self):
        """Gets the {@link ActionManager} used to manage the
        {@link ShortcutListener}s added to this {@link IField}.

        @return the ActionManager in use
        """
        if self._actionManager is None:
            self._actionManager = ActionManager()
            if self.getWindow() is not None:
                self._actionManager.setViewer(self.getWindow())
        return self._actionManager


    def addShortcutListener(self, shortcut):
        self.getActionManager().addAction(shortcut)


    def removeShortcutListener(self, shortcut):
        if self._actionManager is not None:
            self._actionManager.removeAction(shortcut)


class FocusShortcut(ShortcutListener):
    """A ready-made {@link ShortcutListener} that focuses the given
    {@link Focusable} (usually a {@link IField}) when the keyboard
    shortcut is invoked.
    """

    def __init__(self, *args):
        """Creates a keyboard shortcut for focusing the given
        {@link Focusable} using the shorthand notation defined in
        {@link ShortcutAction}.

        @param focusable
                   to focused when the shortcut is invoked
        @param shorthandCaption
                   caption with keycode and modifiers indicated
        ---
        Creates a keyboard shortcut for focusing the given
        {@link Focusable}.

        @param focusable
                   to focused when the shortcut is invoked
        @param keyCode
                   keycode that invokes the shortcut
        @param modifiers
                   modifiers required to invoke the shortcut
        ---
        Creates a keyboard shortcut for focusing the given
        {@link Focusable}.

        @param focusable
                   to focused when the shortcut is invoked
        @param keyCode
                   keycode that invokes the shortcut
        """
        self.focusable = None

        nargs = len(args)
        if nargs == 2:
            if isinstance(args[1], int):
                focusable, keyCode = args
                FocusShortcut.__init__(self, focusable, keyCode, None)
            else:
                focusable, shorthandCaption = args
                super(FocusShortcut, self).__init__(shorthandCaption)
                self.focusable = focusable
        else:
            focusable, keyCode = args[:2]
            modifiers = args[2:]
            super(FocusShortcut, self).__init__(None, keyCode, modifiers)
            self.focusable = focusable


    def handleAction(self, sender, target):
        self.focusable.focus()


class IReadOnlyStatusChangeEvent(ComponentEvent, prop.IProperty,
            prop.IReadOnlyStatusChangeEvent):
    """An <code>Event</code> object specifying the IProperty whose
    read-only status has changed.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, source):
        """New instance of text change event.

        @param source
                   the Source of the event.
        """
        super(IReadOnlyStatusChangeEvent, self).__init__(source)


    def getProperty(self):
        """IProperty where the event occurred.

        @return the Source of the event.
        """
        return self.getSource()
