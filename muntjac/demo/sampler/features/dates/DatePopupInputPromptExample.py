
import locale
from datetime import datetime

from muntjac.ui import VerticalLayout, PopupDateField
from muntjac.data.property import IValueChangeListener


class DatePopupInputPromptExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        self.setSpacing(True)

        self._startDate = PopupDateField()
        self._startDate.setInputPrompt('Start date')

        # Set the correct resolution
        self._startDate.setResolution(PopupDateField.RESOLUTION_DAY)

        # Add valuechangelistener
        self._startDate.addListener(self)
        self._startDate.setImmediate(True)

        self.addComponent(self._startDate)


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
