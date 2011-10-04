
import locale
from datetime import datetime

from muntjac.ui import VerticalLayout, InlineDateField
from muntjac.data.property import IValueChangeListener


class DateInlineExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        self.setSpacing(True)

        self._datetime = InlineDateField('Please select the starting time:')

        # Set the value of the PopupDateField to current date
        self._datetime.setValue(datetime.today())

        # Set the correct resolution
        self._datetime.setResolution(InlineDateField.RESOLUTION_DAY)

        # Add valuechangelistener
        self._datetime.addListener(self)
        self._datetime.setImmediate(True)

        self.addComponent(self._datetime)


    def valueChange(self, event):
        # Get the new value and format it to the current locale
        dateFormatter = locale.D_FMT
        dateOut = event.getProperty().getValue().strftime(dateFormatter)
        # Show notification
        self.getWindow().showNotification('Starting date: ' + dateOut)
