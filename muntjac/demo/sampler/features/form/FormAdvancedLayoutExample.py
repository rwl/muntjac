# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.form.FormPojoExample import (FormPojoExample,)
from muntjac.demo.sampler.ExampleUtil import (ExampleUtil,)
# from com.vaadin.data.Item import (Item,)
# from com.vaadin.data.util.BeanItem import (BeanItem,)
# from com.vaadin.data.validator.IntegerValidator import (IntegerValidator,)
# from com.vaadin.data.validator.StringLengthValidator import (StringLengthValidator,)
# from com.vaadin.ui.Alignment import (Alignment,)
# from com.vaadin.ui.Button import (Button,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.ComboBox import (ComboBox,)
# from com.vaadin.ui.DefaultFieldFactory import (DefaultFieldFactory,)
# from com.vaadin.ui.Field import (Field,)
# from com.vaadin.ui.GridLayout import (GridLayout,)
# from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
# from com.vaadin.ui.PasswordField import (PasswordField,)
# from com.vaadin.ui.TextField import (TextField,)
# from com.vaadin.ui.Window import (Window,)
# from com.vaadin.ui.themes.BaseTheme import (BaseTheme,)
# from java.io.Serializable import (Serializable,)
# from java.util.Arrays import (Arrays,)
# from java.util.Date import (Date,)
# from java.util.UUID import (UUID,)
IntegerValidator = FormPojoExample.IntegerValidator
Person = FormPojoExample.Person


class FormAdvancedLayoutExample(VerticalLayout):
    # the 'POJO' we're editing.
    # The Person class is imported from the basic form example.
    _person = None
    _COMMON_FIELD_WIDTH = '12em'

    def __init__(self):
        self._person = self.Person()
        # a person POJO
        personItem = BeanItem(self._person)
        # item from
        # POJO
        # Create the Form
        personForm = self.FormWithComplexLayout(personItem)
        # Add form to layout
        self.addComponent(personForm)
        # The cancel / apply buttons
        buttons = HorizontalLayout()
        buttons.setSpacing(True)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                self.personForm.discard()

        _0_ = _0_()
        discardChanges = Button('Discard changes', _0_)
        discardChanges.setStyleName(BaseTheme.BUTTON_LINK)
        buttons.addComponent(discardChanges)
        buttons.setComponentAlignment(discardChanges, Alignment.MIDDLE_LEFT)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                # Ingnored, we'll let the Form handle the errors
                try:
                    self.personForm.commit()
                except Exception, e:
                    pass # astStmt: [Stmt([]), None]

        _0_ = _0_()
        apply = Button('Apply', _0_)
        buttons.addComponent(apply)
        personForm.getFooter().setMargin(True)
        personForm.getFooter().addComponent(buttons)
        # button for showing the internal state of the POJO

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                FormAdvancedLayoutExample_this.showPojoState()

        _0_ = _0_()
        showPojoState = Button('Show POJO internal state', _0_)
        self.addComponent(showPojoState)

    def FormWithComplexLayout(FormAdvancedLayoutExample_this, *args, **kwargs):

        class FormWithComplexLayout(Form):
            _ourLayout = None

            def __init__(self, personItem):
                # Override to get control over where fields are placed.
                self.setCaption('Personal details')
                # Create our layout (3x3 GridLayout)
                self._ourLayout = GridLayout(3, 3)
                # Use top-left margin and spacing
                self._ourLayout.setMargin(True, False, False, True)
                self._ourLayout.setSpacing(True)
                self.setLayout(self._ourLayout)
                # Set up buffering
                self.setWriteThrough(False)
                # we want explicit 'apply'
                self.setInvalidCommitted(False)
                # no invalid values in datamodel
                # FieldFactory for customizing the fields and adding validators
                self.setFormFieldFactory(FormAdvancedLayoutExample_this.PersonFieldFactory())
                self.setItemDataSource(personItem)
                # bind to POJO via BeanItem
                # Determines which properties are shown, and in which order:
                self.setVisibleItemProperties(Arrays.asList(['firstName', 'lastName', 'countryCode', 'password', 'birthdate', 'shoesize']))

            def attachField(self, propertyId, field):
                if propertyId == 'firstName':
                    self._ourLayout.addComponent(field, 0, 0)
                elif propertyId == 'lastName':
                    self._ourLayout.addComponent(field, 1, 0, 2, 0)
                elif propertyId == 'password':
                    self._ourLayout.addComponent(field, 0, 2)
                elif propertyId == 'countryCode':
                    self._ourLayout.addComponent(field, 0, 1, 2, 1)
                elif propertyId == 'shoesize':
                    self._ourLayout.addComponent(field, 1, 2)
                elif propertyId == 'birthdate':
                    self._ourLayout.addComponent(field, 2, 2)

        return FormWithComplexLayout(*args, **kwargs)

    def showPojoState(self):
        n = Window.Notification('POJO state', Window.Notification.TYPE_TRAY_NOTIFICATION)
        n.setPosition(Window.Notification.POSITION_CENTERED)
        n.setDescription('First name: ' + self._person.getFirstName() + '<br/>Last name: ' + self._person.getLastName() + '<br/>Country: ' + self._person.getCountryCode() + '<br/>Birthdate: ' + self._person.getBirthdate() + '<br/>Shoe size: ' + self._person.getShoesize() + '<br/>Password: ' + self._person.getPassword())
        self.getWindow().showNotification(n)

    def PersonFieldFactory(FormAdvancedLayoutExample_this, *args, **kwargs):

        class PersonFieldFactory(DefaultFieldFactory):
            countries = ComboBox('Country')

            def __init__(self):
                self.countries.setWidth('100%')
                self.countries.setContainerDataSource(ExampleUtil.getISO3166Container())
                self.countries.setItemCaptionPropertyId(ExampleUtil.iso3166_PROPERTY_NAME)
                self.countries.setItemIconPropertyId(ExampleUtil.iso3166_PROPERTY_FLAG)
                self.countries.setFilteringMode(ComboBox.FILTERINGMODE_STARTSWITH)

            def createField(self, item, propertyId, uiContext):
                if 'countryCode' == propertyId:
                    # filtering ComboBox w/ country names
                    return self.countries
                elif 'password' == propertyId:
                    # Create a password field so the password is not shown
                    f = self.createPasswordField(propertyId)
                else:
                    # Use the super class to create a suitable field base on the
                    # property type.
                    f = super(PersonFieldFactory, self).createField(item, propertyId, uiContext)
                if 'firstName' == propertyId:
                    tf = f
                    tf.setRequired(True)
                    tf.setRequiredError('Please enter a First Name')
                    tf.setWidth(FormAdvancedLayoutExample_this._COMMON_FIELD_WIDTH)
                    tf.addValidator(StringLengthValidator('First Name must be 3-25 characters', 3, 25, False))
                elif 'lastName' == propertyId:
                    tf = f
                    tf.setRequired(True)
                    tf.setRequiredError('Please enter a Last Name')
                    tf.setWidth(FormAdvancedLayoutExample_this._COMMON_FIELD_WIDTH)
                    tf.addValidator(StringLengthValidator('Last Name must be 3-50 characters', 3, 50, False))
                elif 'password' == propertyId:
                    pf = f
                    pf.setRequired(True)
                    pf.setRequiredError('Please enter a password')
                    pf.setWidth('10em')
                    pf.addValidator(StringLengthValidator('Password must be 6-20 characters', 6, 20, False))
                elif 'shoesize' == propertyId:
                    tf = f
                    tf.setNullRepresentation('')
                    tf.setNullSettingAllowed(True)
                    tf.addValidator(IntegerValidator('Shoe size must be an Integer'))
                    tf.setWidth('4em')
                return f

            def createPasswordField(self, propertyId):
                pf = PasswordField()
                pf.setCaption(DefaultFieldFactory.createCaptionByPropertyId(propertyId))
                return pf

        return PersonFieldFactory(*args, **kwargs)

    class Person(Serializable):
        _firstName = ''
        _lastName = ''
        _birthdate = None
        _shoesize = 42
        _password = ''
        _uuid = None
        _countryCode = ''

        def __init__(self):
            self._uuid = UUID.fromString('3856c3da-ea56-4717-9f58-85f6c5f560a5')

        def getFirstName(self):
            return self._firstName

        def setFirstName(self, firstName):
            self._firstName = firstName

        def getLastName(self):
            return self._lastName

        def setLastName(self, lastName):
            self._lastName = lastName

        def getBirthdate(self):
            return self._birthdate

        def setBirthdate(self, birthdate):
            self._birthdate = birthdate

        def getShoesize(self):
            return self._shoesize

        def setShoesize(self, shoesize):
            self._shoesize = shoesize

        def getPassword(self):
            return self._password

        def setPassword(self, password):
            self._password = password

        def getUuid(self):
            return self._uuid

        def getCountryCode(self):
            return self._countryCode

        def setCountryCode(self, countryCode):
            self._countryCode = countryCode
