# -*- coding: utf-8 -*-
# from com.vaadin.data.Property.ValueChangeListener import (ValueChangeListener,)
# from java.util.Date import (Date,)


class DatePopupInputPromptExample(VerticalLayout, ValueChangeListener):
    _startDate = None

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
        dateFormatter = DateFormat.getDateInstance(DateFormat.SHORT)
        value = event.getProperty().getValue()
        if (value is None) or (not isinstance(value, Date)):
            self.getWindow().showNotification('Invalid date entered')
        else:
            dateOut = dateFormatter.format(value)
            # Show notification
            self.getWindow().showNotification('Starting date: ' + dateOut)
