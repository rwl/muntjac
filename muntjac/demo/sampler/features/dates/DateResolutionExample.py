# -*- coding: utf-8 -*-
# from com.vaadin.data.Item import (Item,)
# from com.vaadin.data.Property import (Property,)
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.data.util.IndexedContainer import (IndexedContainer,)
# from com.vaadin.ui.ComboBox import (ComboBox,)
# from com.vaadin.ui.InlineDateField import (InlineDateField,)
# from com.vaadin.ui.VerticalLayout import (VerticalLayout,)


class DateResolutionExample(VerticalLayout, Property.ValueChangeListener):
    resolution_PROPERTY_NAME = 'name'
    # Resolution fields from DateField
    _resolutions = [InlineDateField.RESOLUTION_YEAR, InlineDateField.RESOLUTION_MONTH, InlineDateField.RESOLUTION_DAY, InlineDateField.RESOLUTION_HOUR, InlineDateField.RESOLUTION_MIN, InlineDateField.RESOLUTION_SEC, InlineDateField.RESOLUTION_MSEC]
    _resolutionNames = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'Millisecond']
    _datetime = None
    _localeSelection = None

    def __init__(self):
        self.setSpacing(True)
        self._datetime = InlineDateField('Please select the starting time:')
        # Set the value of the PopupDateField to current date
        self._datetime.setValue(java.util.Date())
        # Set the correct resolution
        self._datetime.setResolution(InlineDateField.RESOLUTION_DAY)
        self._datetime.setImmediate(True)
        # Create selection
        self._localeSelection = ComboBox('Select resolution:')
        self._localeSelection.setNullSelectionAllowed(False)
        self._localeSelection.addListener(self)
        self._localeSelection.setImmediate(True)
        # Fill the selection with choices, set captions correctly
        self._localeSelection.setContainerDataSource(self.getResolutionContainer())
        self._localeSelection.setItemCaptionPropertyId(self.resolution_PROPERTY_NAME)
        self._localeSelection.setItemCaptionMode(ComboBox.ITEM_CAPTION_MODE_PROPERTY)
        self.addComponent(self._datetime)
        self.addComponent(self._localeSelection)

    def valueChange(self, event):
        self._datetime.setResolution(event.getProperty().getValue())
        self._datetime.requestRepaint()

    def getResolutionContainer(self):
        resolutionContainer = IndexedContainer()
        resolutionContainer.addContainerProperty(self.resolution_PROPERTY_NAME, str, None)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._resolutions)):
                break
            added = resolutionContainer.addItem(self._resolutions[i])
            added.getItemProperty(self.resolution_PROPERTY_NAME).setValue(self._resolutionNames[i])
        return resolutionContainer
