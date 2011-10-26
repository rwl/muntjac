
from muntjac.demo.sampler.ExampleUtil import ExampleUtil

from muntjac.api import \
    (VerticalLayout, HorizontalLayout, Button, Alignment,
     Form, GridLayout, ComboBox, PasswordField)

from muntjac.ui import button

from muntjac.ui.themes import BaseTheme
from muntjac.ui.window import Notification

from muntjac.ui.default_field_factory import DefaultFieldFactory

from muntjac.data.validators.string_length_validator import \
    StringLengthValidator

from muntjac.data.validators.integer_validator import IntegerValidator


class FormAdvancedLayoutExample(VerticalLayout):

    _COMMON_FIELD_WIDTH = '12em'

    def __init__(self):
        super(FormAdvancedLayoutExample, self).__init__()

        # the 'POJO' we're editing.
        # The Person class is imported from the basic form example.
        self._person = Person()  # a person POJO
        personItem = BeanItem(self._person)  # item from POJO

        # Create the Form
        personForm = FormWithComplexLayout(personItem, self)

        # Add form to layout
        self.addComponent(personForm)

        # The cancel / apply buttons
        buttons = HorizontalLayout()
        buttons.setSpacing(True)

        discardChanges = Button('Discard changes', DiscardListener(personForm))
        discardChanges.setStyleName(BaseTheme.BUTTON_LINK)
        buttons.addComponent(discardChanges)
        buttons.setComponentAlignment(discardChanges, Alignment.MIDDLE_LEFT)

        aply = Button('Apply', ApplyListener(personForm))
        buttons.addComponent(aply)
        personForm.getFooter().setMargin(True)
        personForm.getFooter().addComponent(buttons)

        # button for showing the internal state of the POJO
        l = InternalStateListener(self)
        showPojoState = Button('Show POJO internal state', l)
        self.addComponent(showPojoState)


    def showPojoState(self):
        n = Notification('POJO state', Notification.TYPE_TRAY_NOTIFICATION)
        n.setPosition(Notification.POSITION_CENTERED)
        n.setDescription(('First name: ' + self._person.getFirstName()
                + '<br/>Last name: ' + self._person.getLastName()
                + '<br/>Country: ' + self._person.getCountryCode()
                + '<br/>Birthdate: ' + self._person.getBirthdate()
                + '<br/>Shoe size: ' + self._person.getShoesize()
                + '<br/>Password: ' + self._person.getPassword()))
        self.getWindow().showNotification(n)


class DiscardListener(button.IClickListener):

    def __init__(self, personForm):
        self._personForm = personForm

    def buttonClick(self, event):
        self._personForm.discard()


class ApplyListener(button.IClickListener):

    def __init__(self, personForm):
        self._personForm = personForm

    def buttonClick(self, event):
        try:
            self._personForm.commit()
        except Exception:
            pass  # Ignored, we'll let the Form handle the errors


class InternalStateListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c.showPojoState()


class FormWithComplexLayout(Form):

    def __init__(self, personItem, c):
        self._c = c

        super(FormWithComplexLayout, self).__init__()

        # Override to get control over where fields are placed.
        self.setCaption('Personal details')

        # Create our layout (3x3 GridLayout)
        self._ourLayout = GridLayout(3, 3)

        # Use top-left margin and spacing
        self._ourLayout.setMargin(True, False, False, True)
        self._ourLayout.setSpacing(True)

        self.setLayout(self._ourLayout)

        # Set up buffering
        self.setWriteThrough(False)  # we want explicit 'apply'
        self.setInvalidCommitted(False)  # no invalid values in datamodel

        # FieldFactory for customizing the fields and adding validators
        self.setFormFieldFactory(PersonFieldFactory(self))
        self.setItemDataSource(personItem)  # bind to POJO via BeanItem

        # Determines which properties are shown, and in which order:
        self.setVisibleItemProperties(['firstName', 'lastName',
                'countryCode', 'password', 'birthdate', 'shoesize'])


    def attachField(self, propertyId, field):
        if propertyId == 'firstName':
            self._c._ourLayout.addComponent(field, 0, 0)
        elif propertyId == 'lastName':
            self._c._ourLayout.addComponent(field, 1, 0, 2, 0)
        elif propertyId == 'password':
            self._c._ourLayout.addComponent(field, 0, 2)
        elif propertyId == 'countryCode':
            self._c._ourLayout.addComponent(field, 0, 1, 2, 1)
        elif propertyId == 'shoesize':
            self._c._ourLayout.addComponent(field, 1, 2)
        elif propertyId == 'birthdate':
            self._c._ourLayout.addComponent(field, 2, 2)


class PersonFieldFactory(DefaultFieldFactory):

    def __init__(self, c):
        self._c = c

        super(PersonFieldFactory, self).__init__()

        self.countries = ComboBox('Country')
        self.countries.setWidth('100%')
        self.countries.setContainerDataSource(
                ExampleUtil.getISO3166Container())
        self.countries.setItemCaptionPropertyId(
                ExampleUtil.iso3166_PROPERTY_NAME)
        self.countries.setItemIconPropertyId(
                ExampleUtil.iso3166_PROPERTY_FLAG)
        self.countries.setFilteringMode(
                ComboBox.FILTERINGMODE_STARTSWITH)


    def createField(self, item, propertyId, uiContext):
        if 'countryCode' == propertyId:
            # filtering ComboBox w/ country names
            return self.countries
        elif 'password' == propertyId:
            # Create a password field so the password is not shown
            f = self.createPasswordField(propertyId)
        else:
            # Use the super class to create a suitable field base
            # on the property type.
            f = super(PersonFieldFactory, self).createField(item,
                    propertyId, uiContext)

        if 'firstName' == propertyId:
            tf = f
            tf.setRequired(True)
            tf.setRequiredError('Please enter a First Name')
            tf.setWidth(self._c._COMMON_FIELD_WIDTH)
            tf.addValidator(StringLengthValidator(
                    'First Name must be 3-25 characters', 3, 25, False))
        elif 'lastName' == propertyId:
            tf = f
            tf.setRequired(True)
            tf.setRequiredError('Please enter a Last Name')
            tf.setWidth(self._c._COMMON_FIELD_WIDTH)
            tf.addValidator(StringLengthValidator(
                    'Last Name must be 3-50 characters', 3, 50, False))
        elif 'password' == propertyId:
            pf = f
            pf.setRequired(True)
            pf.setRequiredError('Please enter a password')
            pf.setWidth('10em')
            pf.addValidator(StringLengthValidator(
                    'Password must be 6-20 characters', 6, 20, False))
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


class Person(object):

    def __init__(self):
        self._uuid = '3856c3da-ea56-4717-9f58-85f6c5f560a5'

        self._firstName = ''
        self._lastName = ''
        self._birthdate = None
        self._shoesize = 42
        self._password = ''
        self._countryCode = ''

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
