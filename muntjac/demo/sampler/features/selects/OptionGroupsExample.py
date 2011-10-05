
from muntjac.ui import VerticalLayout, OptionGroup, Label
from muntjac.data.property import IValueChangeListener


class OptionGroupsExample(VerticalLayout, IValueChangeListener):

    _cities = ['Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
            'Paris', 'Stockholm']

    def __init__(self):
        self.setSpacing(True)

        # 'Shorthand' constructor - also supports data binding using Containers
        citySelect = OptionGroup('Please select a city', self._cities)
        citySelect.setNullSelectionAllowed(False)  # user can not 'unselect'
        citySelect.select('Berlin')  # select this by default
        citySelect.setImmediate(True)  # send the change to the server at once
        citySelect.addListener(self)  # react when the user selects something
        self.addComponent(citySelect)

        self.addComponent(Label('<h3>Multi-selection</h3>',
                Label.CONTENT_XHTML))

        # Create the multiselect option group
        # 'Shorthand' constructor - also supports data binding using Containers
        citySelect = OptionGroup('Please select cities', self._cities)
        citySelect.setMultiSelect(True)
        citySelect.setNullSelectionAllowed(False)  # user can not 'unselect'
        citySelect.select('Berlin')  # select this by default
        citySelect.setImmediate(True)  # send the change to the server at once
        citySelect.addListener(self)  # react when the user selects something
        self.addComponent(citySelect)

    # Shows a notification when a selection is made. The listener will be
    # called whenever the value of the component changes, i.e when the user
    # makes a new selection.
    def valueChange(self, event):
        self.getWindow().showNotification('Selected city: '
                + event.getProperty())
