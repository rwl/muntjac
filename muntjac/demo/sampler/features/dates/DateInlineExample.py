# -*- coding: utf-8 -*-
# from java.text.DateFormat import (DateFormat,)


class DateInlineExample(VerticalLayout, Property.ValueChangeListener):
    _datetime = None

    def __init__(self):
        self.setSpacing(True)
        self._datetime = InlineDateField('Please select the starting time:')
        # Set the value of the PopupDateField to current date
        self._datetime.setValue(java.util.Date())
        # Set the correct resolution
        self._datetime.setResolution(InlineDateField.RESOLUTION_DAY)
        # Add valuechangelistener
        self._datetime.addListener(self)
        self._datetime.setImmediate(True)
        self.addComponent(self._datetime)

    def valueChange(self, event):
        # Get the new value and format it to the current locale
        dateFormatter = DateFormat.getDateInstance(DateFormat.SHORT)
        dateOut = dateFormatter.format(event.getProperty().getValue())
        # Show notification
        self.getWindow().showNotification('Starting date: ' + dateOut)
