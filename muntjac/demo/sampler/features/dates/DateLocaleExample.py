# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.ExampleUtil import (ExampleUtil,)
# from java.util.Locale import (Locale,)


class DateLocaleExample(VerticalLayout, Property.ValueChangeListener):
    _datetime = None
    _localeSelection = None

    def __init__(self):
        self.setSpacing(True)
        self._datetime = InlineDateField('Please select the starting time:')
        # Set the value of the PopupDateField to current date
        self._datetime.setValue(java.util.Date())
        # Set the correct resolution
        self._datetime.setResolution(InlineDateField.RESOLUTION_MIN)
        self._datetime.setImmediate(True)
        self._datetime.setShowISOWeekNumbers(True)
        # Create selection and fill it with locales
        self._localeSelection = ComboBox('Select date format:')
        self._localeSelection.addListener(self)
        self._localeSelection.setImmediate(True)
        self._localeSelection.setContainerDataSource(ExampleUtil.getLocaleContainer())
        self._localeSelection.setNullSelectionAllowed(False)
        self.addComponent(self._datetime)
        self.addComponent(self._localeSelection)

    def valueChange(self, event):
        selected = self._localeSelection.getItem(event.getProperty().getValue())
        self._datetime.setLocale(selected.getItemProperty(ExampleUtil.locale_PROPERTY_LOCALE).getValue())
        self._datetime.requestRepaint()
