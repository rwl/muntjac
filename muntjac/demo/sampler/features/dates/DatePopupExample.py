# -*- coding: utf-8 -*-


class DatePopupExample(VerticalLayout, Property.ValueChangeListener):
    _datetime = None

    def __init__(self):
        self.setSpacing(True)
        self._datetime = PopupDateField('Please select the starting time:')
        # Set the value of the PopupDateField to current date
        self._datetime.setValue(java.util.Date())
        # Set the correct resolution
        self._datetime.setResolution(PopupDateField.RESOLUTION_DAY)
        # Add valuechangelistener
        self._datetime.addListener(self)
        self._datetime.setImmediate(True)
        self.addComponent(self._datetime)

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
