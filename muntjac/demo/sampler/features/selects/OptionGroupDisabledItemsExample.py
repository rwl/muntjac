
from muntjac.api import VerticalLayout, OptionGroup, Label
from muntjac.data.property import IValueChangeListener


class OptionGroupDisabledItemsExample(VerticalLayout, IValueChangeListener):

    _cities = ['Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
            'Paris', 'Stockholm']

    def __init__(self):
        super(OptionGroupDisabledItemsExample, self).__init__()

        self.setSpacing(True)

        # 'Shorthand' constructor - also supports data binding using Containers
        citySelect = OptionGroup('Please select a city', self._cities)

        # Set disabled items
        citySelect.setItemEnabled('Helsinki', False)
        citySelect.setItemEnabled('Oslo', False)
        # user can not 'unselect'
        citySelect.setNullSelectionAllowed(False)
        # select this by default
        citySelect.select('Berlin')
        # send the change to the server at once
        citySelect.setImmediate(True)
        # react when the user selects something
        citySelect.addListener(self, IValueChangeListener)
        self.addComponent(citySelect)

        self.addComponent(Label('<h3>Multi-selection</h3>',
                Label.CONTENT_XHTML))

        # Create the multiselect option group
        # 'Shorthand' constructor - also supports data binding using Containers
        citySelect = OptionGroup('Please select cities', self._cities)

        # Set disabled items
        citySelect.setItemEnabled('Helsinki', False)
        citySelect.setItemEnabled('Oslo', False)
        citySelect.setMultiSelect(True)  # FIXME: multi-select
        # user can not 'unselect'
        citySelect.setNullSelectionAllowed(False)
        # select this by default
        citySelect.select('Berlin')
        # send the change to the server at once
        citySelect.setImmediate(True)
        # react when the user selects something
        citySelect.addListener(self, IValueChangeListener)
        self.addComponent(citySelect)

    # Shows a notification when a selection is made. The listener will be
    # called whenever the value of the component changes, i.e when the user
    # makes a new selection.
    def valueChange(self, event):
        v = event.getProperty().getValue()
        if isinstance(v, set):
            v = list(v)
        self.getWindow().showNotification('Selected city: %s' % v)
