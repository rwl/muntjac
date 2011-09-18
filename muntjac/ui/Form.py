# Copyright (C) 2011 Vaadin Ltd
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

from __pyjamas__ import (ARGERROR, POSTINC,)
from com.vaadin.data.Item import (Editor, Item,)
from com.vaadin.ui.AbstractField import (AbstractField,)
from com.vaadin.data.Buffered import (Buffered,)
from com.vaadin.ui.DefaultFieldFactory import (DefaultFieldFactory,)
from com.vaadin.data.Validatable import (Validatable,)
from com.vaadin.ui.FormLayout import (FormLayout,)
from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
from com.vaadin.data.Validator import (Validator,)
from com.vaadin.ui.Select import (Select,)
from com.vaadin.event.Action import (Action, Notifier,)
from com.vaadin.terminal.CompositeErrorMessage import (CompositeErrorMessage,)
from com.vaadin.data.util.BeanItem import (BeanItem,)
from com.vaadin.event.ActionManager import (ActionManager,)
# from com.vaadin.event.Action.Handler import (Handler,)
# from com.vaadin.event.Action.ShortcutNotifier import (ShortcutNotifier,)
# from java.util.Collection import (Collection,)
# from java.util.Collections import (Collections,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.Map import (Map,)


class Form(AbstractField, Item, Editor, Buffered, Item, Validatable, Action, Notifier):
    """Form component provides easy way of creating and managing sets fields.

    <p>
    <code>Form</code> is a container for fields implementing {@link Field}
    interface. It provides support for any layouts and provides buffering
    interface for easy connection of commit and discard buttons. All the form
    fields can be customized by adding validators, setting captions and icons,
    setting immediateness, etc. Also direct mechanism for replacing existing
    fields with selections is given.
    </p>

    <p>
    <code>Form</code> provides customizable editor for classes implementing
    {@link com.vaadin.data.Item} interface. Also the form itself implements this
    interface for easier connectivity to other items. To use the form as editor
    for an item, just connect the item to form with
    {@link Form#setItemDataSource(Item)}. If only a part of the item needs to be
    edited, {@link Form#setItemDataSource(Item,Collection)} can be used instead.
    After the item has been connected to the form, the automatically created
    fields can be customized and new fields can be added. If you need to connect
    a class that does not implement {@link com.vaadin.data.Item} interface, most
    properties of any class following bean pattern, can be accessed trough
    {@link com.vaadin.data.util.BeanItem}.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    _propertyValue = None
    # Layout of the form.
    _layout = None
    # Item connected to this form as datasource.
    _itemDatasource = None
    # Ordered list of property ids in this editor.
    _propertyIds = LinkedList()
    # Current buffered source exception.
    _currentBufferedSourceException = None
    # Is the form in write trough mode.
    _writeThrough = True
    # Is the form in read trough mode.
    _readThrough = True
    # Mapping from propertyName to corresponding field.
    _fields = dict()
    # Form may act as an Item, its own properties are stored here.
    _ownProperties = dict()
    # Field factory for this form.
    _fieldFactory = None
    # Visible item properties.
    _visibleItemProperties = None
    # Form needs to repaint itself if child fields value changes due possible
    # change in form validity.
    # 
    # TODO introduce ValidityChangeEvent (#6239) and start using it instead.
    # See e.g. DateField#notifyFormOfValidityChange().

    class fieldValueChangeListener(ValueChangeListener):

        def valueChange(self, event):
            self.requestRepaint()

    _formFooter = None
    # If this is true, commit implicitly calls setValidationVisible(true).
    _validationVisibleOnCommit = True
    # special handling for gridlayout; remember initial cursor pos
    _gridlayoutCursorX = -1
    _gridlayoutCursorY = -1
    # Keeps track of the Actions added to this component, and manages the
    # painting and handling as well. Note that the extended AbstractField is a
    # {@link ShortcutNotifier} and has a actionManager that delegates actions
    # to the containing window. This one does not delegate.

    def __init__(self, *args):
        """Constructs a new form with default layout.

        <p>
        By default the form uses {@link FormLayout}.
        </p>
        ---
        Constructs a new form with given {@link Layout}.

        @param formLayout
                   the layout of the form.
        ---
        Constructs a new form with given {@link Layout} and
        {@link FormFieldFactory}.

        @param formLayout
                   the layout of the form.
        @param fieldFactory
                   the FieldFactory of the form.
        """
        self._ownActionManager = ActionManager(self)
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__(None)
            self.setValidationVisible(False)
        elif _1 == 1:
            formLayout, = _0
            self.__init__(formLayout, DefaultFieldFactory.get())
        elif _1 == 2:
            formLayout, fieldFactory = _0
            super(Form, self)()
            self.setLayout(formLayout)
            self.setFormFieldFactory(fieldFactory)
            self.setValidationVisible(False)
            self.setWidth(100, self.UNITS_PERCENTAGE)
        else:
            raise ARGERROR(0, 2)

    # Documented in interface

    def paintContent(self, target):
        super(Form, self).paintContent(target)
        self._layout.paint(target)
        if self._formFooter is not None:
            self._formFooter.paint(target)
        if self._ownActionManager is not None:
            self._ownActionManager.paintActions(None, target)

    def changeVariables(self, source, variables):
        super(Form, self).changeVariables(source, variables)
        # Actions
        if self._ownActionManager is not None:
            self._ownActionManager.handleActions(variables, self)

    def getErrorMessage(self):
        """The error message of a Form is the error of the first field with a
        non-empty error.

        Empty error messages of the contained fields are skipped, because an
        empty error indicator would be confusing to the user, especially if there
        are errors that have something to display. This is also the reason why
        the calculation of the error message is separate from validation, because
        validation fails also on empty errors.
        """
        # Reimplement the checking of validation error by using
        # getErrorMessage() recursively instead of validate().
        validationError = None
        if self.isValidationVisible():
            _0 = True
            i = self._propertyIds
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                f = self._fields[i.next()]
                if isinstance(f, AbstractComponent):
                    field = f
                    validationError = field.getErrorMessage()
                    if validationError is not None:
                        # Show caption as error for fields with empty errors
                        if '' == str(validationError):
                            validationError = Validator.InvalidValueException(field.getCaption())
                        break
                    elif isinstance(f, Field) and not f.isValid():
                        # Something is wrong with the field, but no proper
                        # error is given. Generate one.
                        validationError = Validator.InvalidValueException(field.getCaption())
                        break
        # Return if there are no errors at all
        if (
            self.getComponentError() is None and validationError is None and self._currentBufferedSourceException is None
        ):
            return None
        # Throw combination of the error types
        return CompositeErrorMessage([self.getComponentError(), validationError, self._currentBufferedSourceException])

    def setValidationVisibleOnCommit(self, makeVisible):
        """Controls the making validation visible implicitly on commit.

        Having commit() call setValidationVisible(true) implicitly is the default
        behaviour. You can disable the implicit setting by setting this property
        as false.

        It is useful, because you usually want to start with the form free of
        errors and only display them after the user clicks Ok. You can disable
        the implicit setting by setting this property as false.

        @param makeVisible
                   If true (default), validation is made visible when commit() is
                   called. If false, the visibility is left as it is.
        """
        self._validationVisibleOnCommit = makeVisible

    def isValidationVisibleOnCommit(self):
        """Is validation made automatically visible on commit?

        See setValidationVisibleOnCommit().

        @return true if validation is made automatically visible on commit.
        """
        # Commit changes to the data source Don't add a JavaDoc comment here, we
        # use the default one from the interface.

        return self._validationVisibleOnCommit

    def commit(self):
        # Discards local changes and refresh values from the data source Don't add
        # a JavaDoc comment here, we use the default one from the interface.

        problems = None
        # Only commit on valid state if so requested
        if not self.isInvalidCommitted() and not self.isValid():
            # The values are not ok and we are told not to commit invalid
            # values

            if self._validationVisibleOnCommit:
                self.setValidationVisible(True)
            # Find the first invalid value and throw the exception
            self.validate()
        # Try to commit all
        _0 = True
        i = self._propertyIds
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            try:
                f = self._fields[i.next()]
                # Commit only non-readonly fields.
                if not f.isReadOnly():
                    f.commit()
            except Buffered.SourceException, e:
                if problems is None:
                    problems = LinkedList()
                problems.add(e)
        # No problems occurred
        if problems is None:
            if self._currentBufferedSourceException is not None:
                self._currentBufferedSourceException = None
                self.requestRepaint()
            return
        # Commit problems
        causes = [None] * len(problems)
        index = 0
        _1 = True
        i = problems
        while True:
            if _1 is True:
                _1 = False
            if not i.hasNext():
                break
            causes[POSTINC(globals(), locals(), 'index')] = i.next()
        e = Buffered.SourceException(self, causes)
        self._currentBufferedSourceException = e
        self.requestRepaint()
        raise e

    def discard(self):
        # Is the object modified but not committed? Don't add a JavaDoc comment
        # here, we use the default one from the interface.

        problems = None
        # Try to discard all changes
        _0 = True
        i = self._propertyIds
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            try:
                self._fields[i.next()].discard()
            except Buffered.SourceException, e:
                if problems is None:
                    problems = LinkedList()
                problems.add(e)
        # No problems occurred
        if problems is None:
            if self._currentBufferedSourceException is not None:
                self._currentBufferedSourceException = None
                self.requestRepaint()
            return
        # Discards problems occurred
        causes = [None] * len(problems)
        index = 0
        _1 = True
        i = problems
        while True:
            if _1 is True:
                _1 = False
            if not i.hasNext():
                break
            causes[POSTINC(globals(), locals(), 'index')] = i.next()
        e = Buffered.SourceException(self, causes)
        self._currentBufferedSourceException = e
        self.requestRepaint()
        raise e

    def isModified(self):
        # Is the editor in a read-through mode? Don't add a JavaDoc comment here,
        # we use the default one from the interface.

        _0 = True
        i = self._propertyIds
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            f = self._fields[i.next()]
            if f is not None and f.isModified():
                return True
        return False

    def isReadThrough(self):
        # Is the editor in a write-through mode? Don't add a JavaDoc comment here,
        # we use the default one from the interface.

        return self._readThrough

    def isWriteThrough(self):
        # Sets the editor's read-through mode to the specified status. Don't add a
        # JavaDoc comment here, we use the default one from the interface.

        return self._writeThrough

    def setReadThrough(self, readThrough):
        # Sets the editor's read-through mode to the specified status. Don't add a
        # JavaDoc comment here, we use the default one from the interface.

        if readThrough != self._readThrough:
            self._readThrough = readThrough
            _0 = True
            i = self._propertyIds
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                self._fields[i.next()].setReadThrough(readThrough)

    def setWriteThrough(self, writeThrough):
        if writeThrough != self._writeThrough:
            self._writeThrough = writeThrough
            _0 = True
            i = self._propertyIds
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                self._fields[i.next()].setWriteThrough(writeThrough)

    def addItemProperty(self, id, property):
        """Adds a new property to form and create corresponding field.

        @see com.vaadin.data.Item#addItemProperty(Object, Property)
        """
        # Checks inputs
        if (id is None) or (property is None):
            raise self.NullPointerException('Id and property must be non-null')
        # Checks that the property id is not reserved
        if self._propertyIds.contains(id):
            return False
        self._propertyIds.add(id)
        self._ownProperties.put(id, property)
        # Gets suitable field
        field = self._fieldFactory.createField(self, id, self)
        if field is None:
            return False
        # Configures the field
        field.setPropertyDataSource(property)
        # Register and attach the created field
        self.addField(id, field)
        return True

    def addField(self, propertyId, field):
        """Registers the field with the form and adds the field to the form layout.

        <p>
        The property id must not be already used in the form.
        </p>

        <p>
        This field is added to the layout using the
        {@link #attachField(Object, Field)} method.
        </p>

        @param propertyId
                   the Property id the the field.
        @param field
                   the field which should be added to the form.
        """
        self.registerField(propertyId, field)
        self.attachField(propertyId, field)
        self.requestRepaint()

    def registerField(self, propertyId, field):
        """Register the field with the form. All registered fields are validated
        when the form is validated and also committed when the form is committed.

        <p>
        The property id must not be already used in the form.
        </p>


        @param propertyId
                   the Property id of the field.
        @param field
                   the Field that should be registered
        """
        if (propertyId is None) or (field is None):
            return
        self._fields.put(propertyId, field)
        field.addListener(self.fieldValueChangeListener)
        if not self._propertyIds.contains(propertyId):
            # adding a field directly
            self._propertyIds.addLast(propertyId)
        # Update the read and write through status and immediate to match the
        # form.
        # Should this also include invalidCommitted (#3993)?
        field.setReadThrough(self._readThrough)
        field.setWriteThrough(self._writeThrough)
        if self.isImmediate() and isinstance(field, AbstractComponent):
            field.setImmediate(True)

    def attachField(self, propertyId, field):
        """Adds the field to the form layout.
        <p>
        The field is added to the form layout in the default position (the
        position used by {@link Layout#addComponent(Component)}. If the
        underlying layout is a {@link CustomLayout} the field is added to the
        CustomLayout location given by the string representation of the property
        id using {@link CustomLayout#addComponent(Component, String)}.
        </p>

        <p>
        Override this method to control how the fields are added to the layout.
        </p>

        @param propertyId
        @param field
        """
        if (propertyId is None) or (field is None):
            return
        if isinstance(self._layout, CustomLayout):
            self._layout.addComponent(field, str(propertyId))
        else:
            self._layout.addComponent(field)

    def getItemProperty(self, id):
        """The property identified by the property id.

        <p>
        The property data source of the field specified with property id is
        returned. If there is a (with specified property id) having no data
        source, the field is returned instead of the data source.
        </p>

        @see com.vaadin.data.Item#getItemProperty(Object)
        """
        field = self._fields[id]
        if field is None:
            # field does not exist or it is not (yet) created for this property
            return self._ownProperties[id]
        property = field.getPropertyDataSource()
        if property is not None:
            return property
        else:
            return field

    def getField(self, propertyId):
        """Gets the field identified by the propertyid.

        @param propertyId
                   the id of the property.
        """
        # Documented in interface
        return self._fields[propertyId]

    def getItemPropertyIds(self):
        return Collections.unmodifiableCollection(self._propertyIds)

    def removeItemProperty(self, id):
        """Removes the property and corresponding field from the form.

        @see com.vaadin.data.Item#removeItemProperty(Object)
        """
        self._ownProperties.remove(id)
        field = self._fields[id]
        if field is not None:
            self._propertyIds.remove(id)
            self._fields.remove(id)
            self.detachField(field)
            field.removeListener(self.fieldValueChangeListener)
            return True
        return False

    def detachField(self, field):
        """Called when a form field is detached from a Form. Typically when a new
        Item is assigned to Form via {@link #setItemDataSource(Item)}.
        <p>
        Override this method to control how the fields are removed from the
        layout.
        </p>

        @param field
                   the field to be detached from the forms layout.
        """
        p = field.getParent()
        if isinstance(p, ComponentContainer):
            p.removeComponent(field)

    def removeAllProperties(self):
        """Removes all properties and fields from the form.

        @return the Success of the operation. Removal of all fields succeeded if
                (and only if) the return value is <code>true</code>.
        """
        # Documented in the interface
        properties = list(self._propertyIds)
        success = True
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(properties)):
                break
            if not self.removeItemProperty(properties[i]):
                success = False
        return success

    def getItemDataSource(self):
        return self._itemDatasource

    def setItemDataSource(self, *args):
        """Sets the item datasource for the form.

        <p>
        Setting item datasource clears any fields, the form might contain and
        adds all the properties as fields to the form.
        </p>

        @see com.vaadin.data.Item.Viewer#setItemDataSource(Item)
        ---
        Set the item datasource for the form, but limit the form contents to
        specified properties of the item.

        <p>
        Setting item datasource clears any fields, the form might contain and
        adds the specified the properties as fields to the form, in the specified
        order.
        </p>

        @see com.vaadin.data.Item.Viewer#setItemDataSource(Item)
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            newDataSource, = _0
            self.setItemDataSource(newDataSource, newDataSource.getItemPropertyIds() if newDataSource is not None else None)
        elif _1 == 2:
            newDataSource, propertyIds = _0
            if isinstance(self._layout, GridLayout):
                gl = self._layout
                if self._gridlayoutCursorX == -1:
                    # first setItemDataSource, remember initial cursor
                    self._gridlayoutCursorX = gl.getCursorX()
                    self._gridlayoutCursorY = gl.getCursorY()
                else:
                    # restore initial cursor
                    gl.setCursorX(self._gridlayoutCursorX)
                    gl.setCursorY(self._gridlayoutCursorY)
            # Removes all fields first from the form
            self.removeAllProperties()
            # Sets the datasource
            self._itemDatasource = newDataSource
            # If the new datasource is null, just set null datasource
            if self._itemDatasource is None:
                return
            # Adds all the properties to this form
            _0 = True
            i = propertyIds
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                id = i.next()
                property = self._itemDatasource.getItemProperty(id)
                if id is not None and property is not None:
                    f = self._fieldFactory.createField(self._itemDatasource, id, self)
                    if f is not None:
                        f.setPropertyDataSource(property)
                        self.addField(id, f)
        else:
            raise ARGERROR(1, 2)

    def getLayout(self):
        """Gets the layout of the form.

        <p>
        By default form uses <code>OrderedLayout</code> with <code>form</code>
        -style.
        </p>

        @return the Layout of the form.
        """
        return self._layout

    def setLayout(self, newLayout):
        """Sets the layout of the form.

        <p>
        By default form uses <code>OrderedLayout</code> with <code>form</code>
        -style.
        </p>

        @param newLayout
                   the Layout of the form.
        """
        # Use orderedlayout by default
        if newLayout is None:
            newLayout = FormLayout()
        # reset cursor memory
        self._gridlayoutCursorX = -1
        self._gridlayoutCursorY = -1
        # Move fields from previous layout
        if self._layout is not None:
            properties = list(self._propertyIds)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(properties)):
                    break
                f = properties[i]
                self.detachField(f)
                if isinstance(newLayout, CustomLayout):
                    newLayout.addComponent(f, str(properties[i]))
                else:
                    newLayout.addComponent(f)
            self._layout.setParent(None)
        # Replace the previous layout
        newLayout.setParent(self)
        self._layout = newLayout

    def replaceWithSelect(self, propertyId, values, descriptions):
        """Sets the form field to be selectable from static list of changes.

        <p>
        The list values and descriptions are given as array. The value-array must
        contain the current value of the field and the lengths of the arrays must
        match. Null values are not supported.
        </p>

        @param propertyId
                   the id of the property.
        @param values
        @param descriptions
        @return the select property generated
        """
        # Checks the parameters
        if ((propertyId is None) or (values is None)) or (descriptions is None):
            raise self.NullPointerException('All parameters must be non-null')
        if len(values) != len(descriptions):
            raise self.IllegalArgumentException('Value and description list are of different size')
        # Gets the old field
        oldField = self._fields[propertyId]
        if oldField is None:
            raise self.IllegalArgumentException('Field with given propertyid \'' + str(propertyId) + '\' can not be found.')
        value = oldField.getValue() if oldField.getPropertyDataSource() is None else oldField.getPropertyDataSource().getValue()
        # Checks that the value exists and check if the select should
        # be forced in multiselect mode
        found = False
        isMultiselect = False
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(values) and not found):
                break
            if (values[i] == value) or (value is not None and value == values[i]):
                found = True
        if value is not None and not found:
            if isinstance(value, Collection):
                _1 = True
                it = value
                while True:
                    if _1 is True:
                        _1 = False
                    if not it.hasNext():
                        break
                    val = it.next()
                    found = False
                    _2 = True
                    i = 0
                    while True:
                        if _2 is True:
                            _2 = False
                        else:
                            i += 1
                        if not (i < len(values) and not found):
                            break
                        if (values[i] == val) or (val is not None and val == values[i]):
                            found = True
                    if not found:
                        raise self.IllegalArgumentException('Currently selected value \'' + val + '\' of property \'' + str(propertyId) + '\' was not found')
                isMultiselect = True
            else:
                raise self.IllegalArgumentException('Current value \'' + value + '\' of property \'' + str(propertyId) + '\' was not found')
        # Creates the new field matching to old field parameters
        newField = Select()
        if isMultiselect:
            newField.setMultiSelect(True)
        newField.setCaption(oldField.getCaption())
        newField.setReadOnly(oldField.isReadOnly())
        newField.setReadThrough(oldField.isReadThrough())
        newField.setWriteThrough(oldField.isWriteThrough())
        # Creates the options list
        newField.addContainerProperty('desc', str, '')
        newField.setItemCaptionPropertyId('desc')
        _3 = True
        i = 0
        while True:
            if _3 is True:
                _3 = False
            else:
                i += 1
            if not (i < len(values)):
                break
            id = values[i]
            if id is None:
                id = newField.addItem()
                item = newField.getItem(id)
                newField.setNullSelectionItemId(id)
            else:
                item = newField.addItem(id)
            if item is not None:
                item.getItemProperty('desc').setValue(str(descriptions[i]))
        # Sets the property data source
        property = oldField.getPropertyDataSource()
        oldField.setPropertyDataSource(None)
        newField.setPropertyDataSource(property)
        # Replaces the old field with new one
        self._layout.replaceComponent(oldField, newField)
        self._fields.put(propertyId, newField)
        newField.addListener(self.fieldValueChangeListener)
        oldField.removeListener(self.fieldValueChangeListener)
        return newField

    def attach(self):
        """Notifies the component that it is connected to an application

        @see com.vaadin.ui.Component#attach()
        """
        super(Form, self).attach()
        self._layout.attach()
        if self._formFooter is not None:
            self._formFooter.attach()

    def detach(self):
        """Notifies the component that it is detached from the application.

        @see com.vaadin.ui.Component#detach()
        """
        super(Form, self).detach()
        self._layout.detach()
        if self._formFooter is not None:
            self._formFooter.detach()

    def isValid(self):
        """Tests the current value of the object against all registered validators

        @see com.vaadin.data.Validatable#isValid()
        """
        valid = True
        _0 = True
        i = self._propertyIds
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            valid &= self._fields[i.next()].isValid()
        return valid and super(Form, self).isValid()

    def validate(self):
        """Checks the validity of the validatable.

        @see com.vaadin.data.Validatable#validate()
        """
        super(Form, self).validate()
        _0 = True
        i = self._propertyIds
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            self._fields[i.next()].validate()

    def isInvalidAllowed(self):
        """Checks the validabtable object accept invalid values.

        @see com.vaadin.data.Validatable#isInvalidAllowed()
        """
        return True

    def setInvalidAllowed(self, invalidValueAllowed):
        """Should the validabtable object accept invalid values.

        @see com.vaadin.data.Validatable#setInvalidAllowed(boolean)
        """
        raise self.UnsupportedOperationException()

    def setReadOnly(self, readOnly):
        """Sets the component's to read-only mode to the specified state.

        @see com.vaadin.ui.Component#setReadOnly(boolean)
        """
        super(Form, self).setReadOnly(readOnly)
        _0 = True
        i = self._propertyIds
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            self._fields[i.next()].setReadOnly(readOnly)

    def setFieldFactory(self, fieldFactory):
        """Sets the field factory of Form.

        <code>FieldFactory</code> is used to create fields for form properties.
        By default the form uses BaseFieldFactory to create Field instances.

        @param fieldFactory
                   the New factory used to create the fields.
        @see Field
        @see FormFieldFactory
        @deprecated use {@link #setFormFieldFactory(FormFieldFactory)} instead
        """
        self._fieldFactory = fieldFactory

    def setFormFieldFactory(self, fieldFactory):
        """Sets the field factory used by this Form to genarate Fields for
        properties.

        {@link FormFieldFactory} is used to create fields for form properties.
        {@link DefaultFieldFactory} is used by default.

        @param fieldFactory
                   the new factory used to create the fields.
        @see Field
        @see FormFieldFactory
        """
        self._fieldFactory = fieldFactory

    def getFormFieldFactory(self):
        """Get the field factory of the form.

        @return the FormFieldFactory Factory used to create the fields.
        """
        return self._fieldFactory

    def getFieldFactory(self):
        """Get the field factory of the form.

        @return the FieldFactory Factory used to create the fields.
        @deprecated Use {@link #getFormFieldFactory()} instead. Set the
                    FormFieldFactory using
                    {@link #setFormFieldFactory(FormFieldFactory)}.
        """
        if isinstance(self._fieldFactory, FieldFactory):
            return self._fieldFactory
        return None

    def getType(self):
        """Gets the field type.

        @see com.vaadin.ui.AbstractField#getType()
        """
        if self.getPropertyDataSource() is not None:
            return self.getPropertyDataSource().getType()
        return self.Object

    def setInternalValue(self, newValue):
        """Sets the internal value.

        This is relevant when the Form is used as Field.

        @see com.vaadin.ui.AbstractField#setInternalValue(java.lang.Object)
        """
        # Stores the old value
        oldValue = self._propertyValue
        # Sets the current Value
        super(Form, self).setInternalValue(newValue)
        self._propertyValue = newValue
        # Ignores form updating if data object has not changed.
        if oldValue != newValue:
            self.setFormDataSource(newValue, self.getVisibleItemProperties())

    def getFirstFocusableField(self):
        """Gets the first focusable field in form. If there are enabled,
        non-read-only fields, the first one of them is returned. Otherwise, the
        field for the first property (or null if none) is returned.

        @return the Field.
        """
        if self.getItemPropertyIds() is not None:
            for id in self.getItemPropertyIds():
                if id is not None:
                    field = id
                    if field.isEnabled() and not field.isReadOnly():
                        return field
            # fallback: first field if none of the fields is enabled and
            # writable
            id = self.getItemPropertyIds().next()
            if id is not None:
                return id
        return None

    def setFormDataSource(self, data, properties):
        """Updates the internal form datasource.

        Method setFormDataSource.

        @param data
        @param properties
        """
        # If data is an item use it.
        item = None
        if isinstance(data, Item):
            item = data
        elif data is not None:
            item = BeanItem(data)
        # Sets the datasource to form
        if item is not None and properties is not None:
            # Shows only given properties
            self.setItemDataSource(item, properties)
        else:
            # Shows all properties
            self.setItemDataSource(item)

    def getVisibleItemProperties(self):
        """Returns the visibleProperties.

        @return the Collection of visible Item properites.
        """
        return self._visibleItemProperties

    def setVisibleItemProperties(self, *args):
        """Sets the visibleProperties.

        @param visibleProperties
                   the visibleProperties to set.
        ---
        Sets the visibleProperties.

        @param visibleProperties
                   the visibleProperties to set.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Collection):
                visibleProperties, = _0
                self._visibleItemProperties = visibleProperties
                value = self.getValue()
                if value is None:
                    value = self._itemDatasource
                self.setFormDataSource(value, self.getVisibleItemProperties())
            else:
                visibleProperties, = _0
                v = LinkedList()
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < visibleProperties.length):
                        break
                    v.add(visibleProperties[i])
                self.setVisibleItemProperties(v)
        else:
            raise ARGERROR(1, 1)

    def focus(self):
        """Focuses the first field in the form.

        @see com.vaadin.ui.Component.Focusable#focus()
        """
        f = self.getFirstFocusableField()
        if f is not None:
            f.focus()

    def setTabIndex(self, tabIndex):
        """Sets the Tabulator index of this Focusable component.

        @see com.vaadin.ui.Component.Focusable#setTabIndex(int)
        """
        super(Form, self).setTabIndex(tabIndex)
        _0 = True
        i = self.getItemPropertyIds()
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            i.next().setTabIndex(tabIndex)

    def setImmediate(self, immediate):
        """Setting the form to be immediate also sets all the fields of the form to
        the same state.
        """
        super(Form, self).setImmediate(immediate)
        _0 = True
        i = self._fields.values()
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            f = i.next()
            if isinstance(f, AbstractComponent):
                f.setImmediate(immediate)

    def isEmpty(self):
        """Form is empty if all of its fields are empty."""
        _0 = True
        i = self._fields.values()
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            f = i.next()
            if isinstance(f, AbstractField):
                if not f.isEmpty():
                    return False
        return True

    def addValidator(self, validator):
        """Adding validators directly to form is not supported.

        Add the validators to form fields instead.
        """
        raise self.UnsupportedOperationException()

    def getFooter(self):
        """Returns a layout that is rendered below normal form contents. This area
        can be used for example to include buttons related to form contents.

        @return layout rendered below normal form contents.
        """
        if self._formFooter is None:
            self._formFooter = HorizontalLayout()
            self._formFooter.setParent(self)
        return self._formFooter

    def setFooter(self, newFormFooter):
        """Sets the layout that is rendered below normal form contens.

        @param newFormFooter
                   the new Layout
        """
        if self._formFooter is not None:
            self._formFooter.setParent(None)
        self._formFooter = newFormFooter
        self._formFooter.setParent(self)

    def setEnabled(self, enabled):
        # ACTIONS
        super(Form, self).setEnabled(enabled)
        if self.getParent() is not None and not self.getParent().isEnabled():
            # some ancestor still disabled, don't update children
            return
        else:
            self.getLayout().requestRepaintAll()

    def getOwnActionManager(self):
        """Gets the {@link ActionManager} responsible for handling {@link Action}s
        added to this Form.<br/>
        Note that Form has another ActionManager inherited from
        {@link AbstractField}. The ownActionManager handles Actions attached to
        this Form specifically, while the ActionManager in AbstractField
        delegates to the containing Window (i.e global Actions).

        @return
        """
        if self._ownActionManager is None:
            self._ownActionManager = ActionManager(self)
        return self._ownActionManager

    def addActionHandler(self, actionHandler):
        self.getOwnActionManager().addActionHandler(actionHandler)

    def removeActionHandler(self, actionHandler):
        if self._ownActionManager is not None:
            self._ownActionManager.removeActionHandler(actionHandler)

    def removeAllActionHandlers(self):
        """Removes all action handlers"""
        if self._ownActionManager is not None:
            self._ownActionManager.removeAllActionHandlers()

    def addAction(self, action):
        self.getOwnActionManager().addAction(action)

    def removeAction(self, action):
        if self._ownActionManager is not None:
            self._ownActionManager.removeAction(action)
