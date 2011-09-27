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

from muntjac.data.Item import Editor, Item
from muntjac.ui.AbstractField import AbstractField
from muntjac.data.Buffered import Buffered, SourceException
from muntjac.ui.DefaultFieldFactory import DefaultFieldFactory
from muntjac.data.Validatable import Validatable
from muntjac.ui.FormLayout import FormLayout
from muntjac.ui.HorizontalLayout import HorizontalLayout
from muntjac.data.Validator import InvalidValueException
from muntjac.ui.Select import Select
from muntjac.event.Action import Action, Notifier
from muntjac.terminal.CompositeErrorMessage import CompositeErrorMessage
from muntjac.data.util.BeanItem import BeanItem
from muntjac.event.ActionManager import ActionManager
from muntjac.data.Property import ValueChangeListener
from muntjac.ui.AbstractComponent import AbstractComponent
from muntjac.ui.Field import Field
from muntjac.ui.CustomLayout import CustomLayout
from muntjac.ui.ComponentContainer import ComponentContainer
from muntjac.ui.GridLayout import GridLayout
from muntjac.ui.FieldFactory import FieldFactory


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

    def __init__(self, formLayout=None, fieldFactory=None):
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
        self._propertyValue = None

        # Layout of the form.
        self._layout = None

        # Item connected to this form as datasource.
        self._itemDatasource = None

        # Ordered list of property ids in this editor.
        self._propertyIds = list()

        # Current buffered source exception.
        self._currentBufferedSourceException = None

        # Is the form in write trough mode.
        self._writeThrough = True

        # Is the form in read trough mode.
        self._readThrough = True

        # Mapping from propertyName to corresponding field.
        self._fields = dict()

        # Form may act as an Item, its own properties are stored here.
        self._ownProperties = dict()

        # Field factory for this form.
        self._fieldFactory = None

        # Visible item properties.
        self._visibleItemProperties = None

        _formFooter = None

        # If this is true, commit implicitly calls setValidationVisible(true).
        self._validationVisibleOnCommit = True

        # special handling for gridlayout; remember initial cursor pos
        self._gridlayoutCursorX = -1
        self._gridlayoutCursorY = -1

        # Keeps track of the Actions added to this component, and manages the
        # painting and handling as well. Note that the extended AbstractField is a
        # {@link ShortcutNotifier} and has a actionManager that delegates actions
        # to the containing window. This one does not delegate.
        self._ownActionManager = ActionManager(self)

        if fieldFactory is None:
            fieldFactory = DefaultFieldFactory.get()

        super(Form, self)()
        self.setLayout(formLayout)
        self.setFormFieldFactory(fieldFactory)
        self.setValidationVisible(False)
        self.setWidth(100, self.UNITS_PERCENTAGE)


    # Form needs to repaint itself if child fields value changes due possible
    # change in form validity.
    #
    # TODO introduce ValidityChangeEvent (#6239) and start using it instead.
    # See e.g. DateField#notifyFormOfValidityChange().
    class fieldValueChangeListener(ValueChangeListener):

        def valueChange(self, event):
            self.requestRepaint()


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
            for i in self._propertyIds:
                f = self._fields.get(i)
                if isinstance(f, AbstractComponent):
                    field = f

                    validationError = field.getErrorMessage()
                    if validationError is not None:
                        # Show caption as error for fields with empty errors
                        if '' == str(validationError):
                            validationError = InvalidValueException(field.getCaption())
                        break
                    elif isinstance(f, Field) and not f.isValid():
                        # Something is wrong with the field, but no proper
                        # error is given. Generate one.
                        validationError = InvalidValueException(field.getCaption())
                        break

        # Return if there are no errors at all
        if self.getComponentError() is None and validationError is None \
                and self._currentBufferedSourceException is None:
            return None

        # Throw combination of the error types
        return CompositeErrorMessage([self.getComponentError(), validationError,
                                      self._currentBufferedSourceException])


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
        return self._validationVisibleOnCommit


    def commit(self):
        # Commit changes to the data source.
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
        for i in self._propertyIds:
            try:
                f = self._fields.get(i)
                # Commit only non-readonly fields.
                if not f.isReadOnly():
                    f.commit()
            except SourceException, e:
                if problems is None:
                    problems = list()
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
        for i in problems:
            causes[index] = i
            index += 1

        e = SourceException(self, causes)
        self._currentBufferedSourceException = e
        self.requestRepaint()
        raise e


    def discard(self):
        # Discards local changes and refresh values from the data source
        problems = None

        # Try to discard all changes
        for i in self._propertyIds:
            try:
                self._fields.get(i).discard()
            except SourceException, e:
                if problems is None:
                    problems = list()
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
        for i in problems:
            causes[index] = i
            index += 1

        e = SourceException(self, causes)
        self._currentBufferedSourceException = e
        self.requestRepaint()
        raise e


    def isModified(self):
        # Is the object modified but not committed?

        for i in self._propertyIds:
            f = self._fields.get(i)
            if f is not None and f.isModified():
                return True

        return False


    def isReadThrough(self):
        # Is the editor in a read-through mode?
        return self._readThrough


    def isWriteThrough(self):
        # Is the editor in a write-through mode?
        return self._writeThrough


    def setReadThrough(self, readThrough):
        # Sets the editor's read-through mode to the specified status.
        if readThrough != self._readThrough:
            self._readThrough = readThrough
            for i in self._propertyIds:
                self._fields.get(i).setReadThrough(readThrough)


    def setWriteThrough(self, writeThrough):
        # Sets the editor's read-through mode to the specified status.
        if writeThrough != self._writeThrough:
            self._writeThrough = writeThrough
            for i in self._propertyIds:
                self._fields.get(i).setWriteThrough(writeThrough)


    def addItemProperty(self, idd, prop):
        """Adds a new property to form and create corresponding field.

        @see com.vaadin.data.Item#addItemProperty(Object, Property)
        """
        # Checks inputs
        if (idd is None) or (prop is None):
            raise ValueError, 'Id and property must be non-null'
        # Checks that the property id is not reserved
        if self._propertyIds.contains(idd):
            return False
        self._propertyIds.add(idd)
        self._ownProperties.put(idd, prop)
        # Gets suitable field
        field = self._fieldFactory.createField(self, idd, self)
        if field is None:
            return False
        # Configures the field
        field.setPropertyDataSource(prop)
        # Register and attach the created field
        self.addField(idd, field)
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

        self._fields[propertyId] = field
        field.addListener(self.fieldValueChangeListener)
        if propertyId not in self._propertyIds:
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


    def getItemProperty(self, idd):
        """The property identified by the property id.

        <p>
        The property data source of the field specified with property id is
        returned. If there is a (with specified property id) having no data
        source, the field is returned instead of the data source.
        </p>

        @see com.vaadin.data.Item#getItemProperty(Object)
        """
        field = self._fields.get(idd)
        if field is None:
            # field does not exist or it is not (yet) created for this property
            return self._ownProperties.get(idd)

        prop = field.getPropertyDataSource()

        if prop is not None:
            return prop
        else:
            return field


    def getField(self, propertyId):
        """Gets the field identified by the propertyid.

        @param propertyId
                   the id of the property.
        """
        return self._fields.get(propertyId)


    def getItemPropertyIds(self):
        return list(self._propertyIds)


    def removeItemProperty(self, idd):
        """Removes the property and corresponding field from the form.

        @see com.vaadin.data.Item#removeItemProperty(Object)
        """
        self._ownProperties.remove(idd)
        field = self._fields.get(idd)
        if field is not None:
            del self._propertyIds[idd]
            del self._fields[idd]
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
        properties = list(self._propertyIds)
        success = True

        for i in range(len(properties)):
            if not self.removeItemProperty(properties[i]):
                success = False

        return success


    def getItemDataSource(self):
        return self._itemDatasource


    def setItemDataSource(self, newDataSource, propertyIds=None):
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
        if propertyIds is None:
            self.setItemDataSource(newDataSource, newDataSource.getItemPropertyIds() if newDataSource is not None else None)
        else:
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
            for idd in propertyIds:
                prop = self._itemDatasource.getItemProperty(idd)
                if idd is not None and prop is not None:
                    f = self._fieldFactory.createField(self._itemDatasource, idd, self)
                    if f is not None:
                        f.setPropertyDataSource(prop)
                        self.addField(idd, f)


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
            for i in range(len(properties)):
                f = self.getField(properties[i])
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
        if (propertyId is None) or (values is None) or (descriptions is None):
            raise ValueError, 'All parameters must be non-null'

        if len(values) != len(descriptions):
            raise ValueError, 'Value and description list are of different size'

        # Gets the old field
        oldField = self._fields.get(propertyId)
        if oldField is None:
            raise ValueError, 'Field with given propertyid \'' \
                    + str(propertyId) + '\' can not be found.'

        value = oldField.getValue() if oldField.getPropertyDataSource() is None else oldField.getPropertyDataSource().getValue()

        # Checks that the value exists and check if the select should
        # be forced in multiselect mode
        found = False
        isMultiselect = False
        i = 0
        while i < len(values) and not found:
            if (values[i] == value) \
                    or (value is not None and value == values[i]):
                found = True
                i += 1

        if value is not None and not found:
            if isinstance(value, list):
                for val in value:
                    found = False
                    i = 0
                    while i < len(values) and not found:
                        if (values[i] == val) or (val is not None and val == values[i]):
                            found = True
                        i += 1
                    if not found:
                        raise ValueError, 'Currently selected value \'' \
                            + val + '\' of property \'' \
                            + str(propertyId) + '\' was not found'

                isMultiselect = True
            else:
                raise ValueError, 'Current value \'' \
                        + value + '\' of property \'' \
                        + str(propertyId) + '\' was not found'

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
        for idd in values:
            if idd is None:
                idd = newField.addItem()
                item = newField.getItem(idd)
                newField.setNullSelectionItemId(idd)
            else:
                item = newField.addItem(idd)

            if item is not None:
                item.getItemProperty('desc').setValue(str(descriptions[i]))

        # Sets the property data source
        prop = oldField.getPropertyDataSource()
        oldField.setPropertyDataSource(None)
        newField.setPropertyDataSource(prop)

        # Replaces the old field with new one
        self._layout.replaceComponent(oldField, newField)
        self._fields[propertyId] = newField
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

        for i in self._propertyIds:
            valid &= self._fields[i].isValid()

        return valid and super(Form, self).isValid()


    def validate(self):
        """Checks the validity of the validatable.

        @see com.vaadin.data.Validatable#validate()
        """
        super(Form, self).validate()
        for i in self._propertyIds:
            self._fields[i].validate()


    def isInvalidAllowed(self):
        """Checks the validabtable object accept invalid values.

        @see com.vaadin.data.Validatable#isInvalidAllowed()
        """
        return True


    def setInvalidAllowed(self, invalidValueAllowed):
        """Should the validabtable object accept invalid values.

        @see com.vaadin.data.Validatable#setInvalidAllowed(boolean)
        """
        raise NotImplementedError


    def setReadOnly(self, readOnly):
        """Sets the component's to read-only mode to the specified state.

        @see com.vaadin.ui.Component#setReadOnly(boolean)
        """
        super(Form, self).setReadOnly(readOnly)
        for i in self._propertyIds:
            self._fields[i].setReadOnly(readOnly)


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
        raise DeprecationWarning, 'use setFormFieldFactory() instead'
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
        return object


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
            for idd in self.getItemPropertyIds():
                if idd is not None:
                    field = self.getField(idd)
                    if field.isEnabled() and not field.isReadOnly():
                        return field

            # fallback: first field if none of the fields is enabled and
            # writable
            idd = iter( self.getItemPropertyIds() ).next()  # FIXME: translate iterator
            if idd is not None:
                return self.getField(idd)

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


    def setVisibleItemProperties(self, visibleProperties):
        """Sets the visibleProperties.

        @param visibleProperties
                   the visibleProperties to set.
        """
        self._visibleItemProperties = visibleProperties
        value = self.getValue()
        if value is None:
            value = self._itemDatasource
        self.setFormDataSource(value, self.getVisibleItemProperties())


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
        for i in self.getItemPropertyIds():
            i.setTabIndex(tabIndex)


    def setImmediate(self, immediate):
        """Setting the form to be immediate also sets all the fields of the form to
        the same state.
        """
        super(Form, self).setImmediate(immediate)
        for f in self._fields.values():
            if isinstance(f, AbstractComponent):
                f.setImmediate(immediate)


    def isEmpty(self):
        """Form is empty if all of its fields are empty."""
        for f in self._fields.values():
            if isinstance(f, AbstractField):
                if not f.isEmpty():
                    return False
        return True


    def addValidator(self, validator):
        """Adding validators directly to form is not supported.

        Add the validators to form fields instead.
        """
        raise NotImplementedError


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
