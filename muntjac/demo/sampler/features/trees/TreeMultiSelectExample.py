
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import VerticalLayout, Tree, Button
from muntjac.ui import button
from muntjac.event.action import Action
from muntjac.event import action
from muntjac.data.property import IValueChangeListener
from muntjac.ui.abstract_select import AbstractSelect


class TreeMultiSelectExample(VerticalLayout, action.IHandler):

    _ACTION_ADD = Action('Add child item')
    _ACTION_DELETE = Action('Delete')
    _ACTIONS = [_ACTION_ADD, _ACTION_DELETE]

    def __init__(self):
        super(TreeMultiSelectExample, self).__init__()

        self.setSpacing(True)

        # Create new Tree object using a hierarchical container from
        # ExampleUtil class
        self._tree = Tree('Hardware Inventory',
                ExampleUtil.getHardwareContainer())

        # Set multiselect mode
        self._tree.setMultiSelect(True)
        self._tree.setImmediate(True)

        self._tree.addListener(TreeListener(self), IValueChangeListener)

        # Add Actionhandler
        self._tree.addActionHandler(self)

        # Set tree to show the 'name' property as caption for items
        self._tree.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        self._tree.setItemCaptionMode(AbstractSelect.ITEM_CAPTION_MODE_PROPERTY)

        # Expand whole tree
        for idd in self._tree.rootItemIds():
            self._tree.expandItemsRecursively(idd)

        # Create the 'delete button', inline click-listener
        self._deleteButton = Button('Delete', DeleteListener(self))
        self._deleteButton.setEnabled(False)
        self.addComponent(self._deleteButton)
        self.addComponent(self._tree)


    # Returns the set of available actions
    def getActions(self, target, sender):
        return self._ACTIONS


    # Handle actions
    def handleAction(self, a, sender, target):
        if a == self._ACTION_ADD:
            # Allow children for the target item
            self._tree.setChildrenAllowed(target, True)
            # Create new item, disallow children, add name, set parent
            itemId = self._tree.addItem()
            self._tree.setChildrenAllowed(itemId, False)
            newItemName = 'New Item # %d' % itemId
            item = self._tree.getItem(itemId)
            p = item.getItemProperty(ExampleUtil.hw_PROPERTY_NAME)
            p.setValue(newItemName)
            self._tree.setParent(itemId, target)
            self._tree.expandItem(target)
        elif a == self._ACTION_DELETE:
            parent = self._tree.getParent(target)
            self._tree.removeItem(target)
            # If the deleted object's parent has no more children, set it's
            # childrenallowed property to false
            if parent is not None and len(self._tree.getChildren(parent)) == 0:
                self._tree.setChildrenAllowed(parent, False)


class TreeListener(IValueChangeListener):

    def __init__(self, c):
        self._c = c

    def valueChange(self, event):
        t = event.getProperty()
        # enable if something is selected, returns a set
        enabled = t.getValue() is not None and len(t.getValue()) > 0
        self._c._deleteButton.setEnabled(enabled)


class DeleteListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        # Delete all the selected objects
        toDelete = list(self._c._tree.getValue())
        for i in range(len(toDelete)):
            self._c.handleAction(self._c._ACTION_DELETE,
                    self._c._tree, toDelete[i])
