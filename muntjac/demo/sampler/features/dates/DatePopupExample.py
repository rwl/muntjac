
import locale
from datetime import datetime

from muntjac.ui import VerticalLayout, PopupDateField
from muntjac.data.property import IValueChangeListener


class DatePopupExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        self.setSpacing(True)

        self._datetime = PopupDateField('Please select the starting time:')

        # Set the value of the PopupDateField to current date
        self._datetime.setValue(datetime.today())

        # Set the correct resolution
        self._datetime.setResolution(PopupDateField.RESOLUTION_DAY)

        # Add value change listener
        self._datetime.addListener(self)
        self._datetime.setImmediate(True)

        self.addComponent(self._datetime)


    def valueChange(self, event):
        # Get the new value and format it to the current locale
        dateFormatter = locale.D_FMT
        value = event.getProperty().getValue()
        if (value is None) or (not isinstance(value, datetime)):
            self.getWindow().showNotification('Invalid date entered')
        else:
            dateOut = value.strftime(dateFormatter)
            # Show notification
            self.getWindow().showNotification('Starting date: ' + dateOut)
