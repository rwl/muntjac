# -*- coding: utf-8 -*-
# from com.vaadin.data.Validator import (Validator,)
# from com.vaadin.data.Validator.InvalidValueException import (InvalidValueException,)
# from com.vaadin.ui.Form import (Form,)


class FormExample(CustomComponent):
    """This example demonstrates the most important features of the Form component:
    binding Form to a JavaBean so that form fields are automatically generated
    from the bean properties, creation of custom field editors using a
    FieldFactory, customizing the form without FieldFactory, buffering
    (commit/discard) and validation. Please note that the example is quite a bit
    more complex than real use, as it tries to demonstrate more features than
    needed in general case.
    """
    cities = ['Amsterdam', 'Berlin', 'Helsinki', 'Hong Kong', 'London', 'Luxemburg', 'New York', 'Oslo', 'Paris', 'Rome', 'Stockholm', 'Tokyo', 'Turku']

    def __init__(self):
        """Compose the demo."""
        # Example data model
        dataModel = self.Address()

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                self.getWindow().showNotification(self.dataModel.getAddressAsText())

        _0_ = _0_()
        peekDataModelState = Button('Show the data model state', _0_)
        # Example form
        form = self.AddressForm('Contact Information')
        form.setDataSource(dataModel)
        form.setDescription('Please enter valid name and address. Fields marked with * are required. ' + 'If you try to commit with invalid values, a form error message is displayed. ' + '(Address is required but failing to give it a value does not display an error.)')
        # Layout the example
        root = VerticalLayout()
        root.setMargin(True)
        root.setSpacing(True)
        root.addComponent(form)
        root.addComponent(peekDataModelState)
        self.setCompositionRoot(root)

    def AddressForm(FormExample_this, *args, **kwargs):

        class AddressForm(Form):

            def __init__(self, caption):
                self.setCaption(caption)
                # Use custom field factory to modify the defaults on how the
                # components are created
                self.setFormFieldFactory(FormExample_this.MyFieldFactory())
                # Add Commit and Discard controls to the form.

                class _0_(ClickListener):

                    def buttonClick(self, event):
                        # Failed to commit. The validation errors are
                        # automatically shown to the user.
                        try:
                            self.commit()
                        except InvalidValueException, e:
                            pass # astStmt: [Stmt([]), None]

                _0_ = _0_()
                commit = Button('Save', _0_)
                discard = Button('Reset', self, 'discard')
                footer = HorizontalLayout()
                footer.addComponent(commit)
                footer.addComponent(discard)
                self.setFooter(footer)

            def setDataSource(self, dataModel):
                # Set the form to edit given datamodel by converting pojo used as
                # the datamodel to Item
                self.setItemDataSource(BeanItem(dataModel))
                # Ensure that the fields are shown in correct order as the
                # datamodel does not force any specific order.
                self.setVisibleItemProperties(['name', 'streetAddress', 'postalCode', 'city'])
                # For examples sake, customize some of the form fields directly
                # here. The alternative way is to use custom field factory as shown
                # above.
                'name'.setRequired(True)
                'name'.setDescription('Please enter name')
                'name'.setRequiredError('Name is missing')
                'streetAddress'.setRequired(True)
                # No error message
                'streetAddress'.setDescription('Please enter street adderss.')
                'postalCode'.setRequired(True)
                # No error message
                'postalCode'.setDescription('Please enter postal code. Example: 12345.')
                self.replaceWithSelect('city', FormExample_this.cities, FormExample_this.cities).setNewItemsAllowed(True)
                'city'.setDescription('Select city from list or type it. City field is not required.')
                # Set the form to act immediately on user input. This is
                # automatically transports data between the client and the server
                # to do server-side validation.
                self.setImmediate(True)
                # Enable buffering so that commit() must be called for the form
                # before input is written to the data. (Form input is not written
                # immediately through to the underlying object.)
                self.setWriteThrough(False)

        return AddressForm(*args, **kwargs)

    def MyFieldFactory(FormExample_this, *args, **kwargs):

        class MyFieldFactory(DefaultFieldFactory):
            """This is example on how to customize field creation. Any kind of field
            components could be created on the fly.
            """

            def createField(self, item, propertyId, uiContext):
                field = super(MyFieldFactory, self).createField(item, propertyId, uiContext)
                if 'postalCode' == propertyId:
                    field.setColumns(5)
                    field.addValidator(FormExample_this.PostalCodeValidator())
                return field

        return MyFieldFactory(*args, **kwargs)

    class PostalCodeValidator(Validator):
        """This is an example of how to create a custom validator for automatic
        input validation.
        """

        def isValid(self, value):
            if (value is None) or (not isinstance(value, str)):
                return False
            return value.matches('[0-9]{5}')

        def validate(self, value):
            if not self.isValid(value):
                raise InvalidValueException('Postal code must be a five digit number.')

    class Address(object):
        """Contact information data model created as POJO. Note that in many cases
        it would be a good idea to implement Item -interface for the datamodel to
        make it directly bindable to form (without BeanItem wrapper)
        """
        _name = ''
        _streetAddress = ''
        _postalCode = ''
        _city = None

        def getAddressAsText(self):
            return self._name + '\n' + self._streetAddress + '\n' + self._postalCode + ' ' + ('' if self._city is None else self._city)

        def setName(self, name):
            self._name = name

        def getName(self):
            return self._name

        def setStreetAddress(self, address):
            self._streetAddress = address

        def getStreetAddress(self):
            return self._streetAddress

        def setPostalCode(self, postalCode):
            self._postalCode = postalCode

        def getPostalCode(self):
            return self._postalCode

        def setCity(self, city):
            self._city = city

        def getCity(self):
            return self._city
