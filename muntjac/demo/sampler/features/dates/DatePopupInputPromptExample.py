
from datetime import datetime
from babel.dates import format_date

from muntjac.api import VerticalLayout, PopupDateField
from muntjac.data.property import IValueChangeListener


class DatePopupInputPromptExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        super(DatePopupInputPromptExample, self).__init__()

        self.setSpacing(True)

        self._startDate = PopupDateField()
        self._startDate.setInputPrompt('Start date')

        # Set the correct resolution
        self._startDate.setResolution(PopupDateField.RESOLUTION_DAY)

        # Add valuechangelistener
        self._startDate.addListener(self, IValueChangeListener)
        self._startDate.setImmediate(True)

        self.addComponent(self._startDate)


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
