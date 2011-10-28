
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import VerticalLayout, Tree
from muntjac.event.item_click_event import IItemClickListener, ItemClickEvent
from muntjac.ui.abstract_select import AbstractSelect


class TreeMouseEventsExample(VerticalLayout, IItemClickListener):

    def __init__(self):
        super(TreeMouseEventsExample, self).__init__()

        self.setSpacing(True)

        # Create new Tree object using a hierarchical container from
        # ExampleUtil class
        self._t = Tree('Hardware Inventory', ExampleUtil.getHardwareContainer())

        # Add ItemClickListener to the tree
        self._t.addListener(self, IItemClickListener)
        self._t.setImmediate(True)

        # Set tree to show the 'name' property as caption for items
        self._t.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        self._t.setItemCaptionMode(AbstractSelect.ITEM_CAPTION_MODE_PROPERTY)

        # Starting itemId # for new items
        self._itemId = len(self._t.getContainerDataSource())

        # Expand whole tree
        for i in range(self._itemId):
            self._t.expandItemsRecursively(i)

        # Disallow selecting items from the tree
        self._t.setSelectable(False)

        self.addComponent(self._t)


    def itemClick(self, event):
        # Indicate which modifier keys are pressed
        modifiers = ''
        if event.isAltKey():
            modifiers += 'Alt '
        if event.isCtrlKey():
            modifiers += 'Ctrl '
        if event.isMetaKey():
            modifiers += 'Meta '
        if event.isShiftKey():
            modifiers += 'Shift '
        if len(modifiers) > 0:
            modifiers = 'Modifiers: ' + modifiers
        else:
            modifiers = 'Modifiers: none'

        b = event.getButton()
        if b == ItemClickEvent.BUTTON_LEFT:
            self.getWindow().showNotification('Selected item: '
                    + str(event.getItem()), modifiers)
        elif b == ItemClickEvent.BUTTON_MIDDLE:
            parent = self._t.getParent(event.getItemId())
            self.getWindow().showNotification('Removed item: '
                    + str(event.getItem()), modifiers)
            self._t.removeItem(event.getItemId())  # FIXME: refresh
            if (parent is not None) and \
                    (self._t.getChildren(parent) == None  # FIXME: null children
                     or len(self._t.getChildren(parent)) == 0):
                self._t.setChildrenAllowed(parent, False)
        elif b == ItemClickEvent.BUTTON_RIGHT:
            self.getWindow().showNotification('Added item: New Item # '
                    + str(self._itemId), modifiers)
            self._t.setChildrenAllowed(event.getItemId(), True)
            i = self._t.addItem(self._itemId)
            self._t.setChildrenAllowed(self._itemId, False)
            newItemName = 'New Item # ' + str(self._itemId)
            i.getItemProperty(ExampleUtil.hw_PROPERTY_NAME).setValue(newItemName)
            self._t.setParent(self._itemId, event.getItemId())
            self._t.expandItem(event.getItemId())
            self._itemId += 1
