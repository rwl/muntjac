
from babel.dates import format_date
from datetime import datetime

from muntjac.api import VerticalLayout, PopupDateField
from muntjac.data.property import IValueChangeListener


class DatePopupExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        super(DatePopupExample, self).__init__()

        self.setSpacing(True)

        self._datetime = PopupDateField('Please select the starting time:')

        # Set the value of the PopupDateField to current date
        self._datetime.setValue(datetime.today())

        # Set the correct resolution
        self._datetime.setResolution(PopupDateField.RESOLUTION_DAY)

        # Add value change listener
        self._datetime.addListener(self, IValueChangeListener)
        self._datetime.setImmediate(True)

        self.addComponent(self._datetime)


    def valueChange(self, event):
        app = self.getApplication()
        if app is not None:
            l = app.getLocale()

        # Get the new value and format it to the current locale
        value = event.getProperty().getValue()
        if (value is None) or (not isinstance(value, datetime)):
            self.getWindow().showNotification('Invalid date entered')
        else:
            dateOut = format_date(value, locale=l).encode('utf-8')
            # Show notification
            self.getWindow().showNotification('Starting date: ' + dateOut)
