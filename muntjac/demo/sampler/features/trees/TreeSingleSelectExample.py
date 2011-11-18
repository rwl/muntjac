
from muntjac.demo.sampler.ExampleUtil import ExampleUtil

from muntjac.api import \
    HorizontalLayout, Button, Tree, TextField, Alignment

from muntjac.ui import button

from muntjac.data.property import IValueChangeListener
from muntjac.event.action import Action
from muntjac.event import action
from muntjac.ui.abstract_select import AbstractSelect


class TreeSingleSelectExample(HorizontalLayout, IValueChangeListener,
            button.IClickListener, action.IHandler):

    # Actions for the context menu
    _ACTION_ADD = Action('Add child item')
    _ACTION_DELETE = Action('Delete')

    def __init__(self):
        super(TreeSingleSelectExample, self).__init__()

        self.setSpacing(True)

        # Create the Tree,a dd to layout
        self._tree = Tree('Hardware Inventory')
        self.addComponent(self._tree)

        # Contents from a (prefilled example) hierarchical container:
        self._tree.setContainerDataSource(ExampleUtil.getHardwareContainer())

        # Add Valuechangelistener and Actionhandler
        self._tree.addListener(self, IValueChangeListener)

        # Add actions (context menu)
        self._tree.addActionHandler(self)

        # Cause valueChange immediately when the user selects
        self._tree.setImmediate(True)

        # Set tree to show the 'name' property as caption for items
        self._tree.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        self._tree.setItemCaptionMode(AbstractSelect.ITEM_CAPTION_MODE_PROPERTY)

        # Expand whole tree
        for idd in self._tree.rootItemIds():
            self._tree.expandItemsRecursively(idd)

        # Create the 'editor bar' (textfield and button in a horizontallayout)
        self._editBar = HorizontalLayout()
        self._editBar.setMargin(False, False, False, True)
        self._editBar.setEnabled(False)
        self.addComponent(self._editBar)

        # textfield
        self._editor = TextField('Item name')
        self._editor.setImmediate(True)
        self._editBar.addComponent(self._editor)

        # apply-button
        self._change = Button('Apply', self)#, 'buttonClick') FIXME: listener
        self._editBar.addComponent(self._change)
        self._editBar.setComponentAlignment(self._change, Alignment.BOTTOM_LEFT)


    def valueChange(self, event):
        if event.getProperty().getValue() is not None:
            # If something is selected from the tree, get it's 'name' and
            # insert it into the textfield
            val = self._tree.getItem(
                    event.getProperty().getValue()).getItemProperty(
                            ExampleUtil.hw_PROPERTY_NAME)
            self._editor.setValue(val)
            self._editor.requestRepaint()
            self._editBar.setEnabled(True)
        else:
            self._editor.setValue('')
            self._editBar.setEnabled(False)


    def buttonClick(self, event):
        # If the edited value contains something, set it to be the item's new
        # 'name' property
        if not (self._editor.getValue() == ''):
            item = self._tree.getItem(self._tree.getValue())
            name = item.getItemProperty(ExampleUtil.hw_PROPERTY_NAME)
            name.setValue(self._editor.getValue())


    # Returns the set of available actions
    def getActions(self, target, sender):
        return [self._ACTION_ADD, self._ACTION_DELETE]


    # Handle actions
    def handleAction(self, a, sender, target):
        if a == self._ACTION_ADD:
            # Allow children for the target item, and expand it
            self._tree.setChildrenAllowed(target, True)
            self._tree.expandItem(target)
            # Create new item, set parent, disallow children (= leaf node)
            itemId = self._tree.addItem()
            self._tree.setParent(itemId, target)
            self._tree.setChildrenAllowed(itemId, False)
            # Set the name for this item (we use it as item caption)
            item = self._tree.getItem(itemId)
            name = item.getItemProperty(ExampleUtil.hw_PROPERTY_NAME)
            name.setValue('New Item')
        elif a == self._ACTION_DELETE:
            parent = self._tree.getParent(target)
            self._tree.removeItem(target)
            # If the deleted object's parent has no more children, set it's
            # childrenallowed property to false (= leaf node)
            if parent is not None and len(self._tree.getChildren(parent)) == 0:
                self._tree.setChildrenAllowed(parent, False)
