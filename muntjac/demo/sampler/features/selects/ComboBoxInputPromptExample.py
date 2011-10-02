# -*- coding: utf-8 -*-


class ComboBoxInputPromptExample(VerticalLayout, Property.ValueChangeListener):
    _cities = ['Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo', 'Paris', 'Stockholm']

    def __init__(self):
        # Shows a notification when a selection is made.
        self.setMargin(True, False, False, False)
        # for looks: more 'air'
        # Create & set input prompt
        l = ComboBox()
        l.setInputPrompt('Please select a city')
        # configure & load content
        l.setImmediate(True)
        l.addListener(self)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._cities)):
                break
            l.addItem(self._cities[i])
        # add to the layout
        self.addComponent(l)

    def valueChange(self, event):
        self.getWindow().showNotification('Selected city: ' + event.getProperty())
