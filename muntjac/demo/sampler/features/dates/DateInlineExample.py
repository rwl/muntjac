
from datetime import datetime
from babel.dates import format_date

from muntjac.api import VerticalLayout, InlineDateField
from muntjac.data.property import IValueChangeListener


class DateInlineExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        super(DateInlineExample, self).__init__()

        self.setSpacing(True)

        self._datetime = InlineDateField('Please select the starting time:')

        # Set the value of the PopupDateField to current date
        self._datetime.setValue(datetime.today())

        # Set the correct resolution
        self._datetime.setResolution(InlineDateField.RESOLUTION_DAY)

        # Add valuechangelistener
        self._datetime.addListener(self, IValueChangeListener)
        self._datetime.setImmediate(True)

        self.addComponent(self._datetime)


    def valueChange(self, event):
        app = self.getApplication()
        if app is not None:
            l = app.getLocale()

        # Get the new value and format it to the current locale
        dateOut = format_date(event.getProperty().getValue(),
                locale=l).encode('utf-8')

        # Show notification
        self.getWindow().showNotification('Starting date: ' + dateOut)
