# -*- coding: utf-8 -*-
from muntjac.demo.sampler.ExampleUtil import (ExampleUtil,)


class TreeMultiSelectExample(VerticalLayout, Action.Handler):
    _ACTION_ADD = Action('Add child item')
    _ACTION_DELETE = Action('Delete')
    _ACTIONS = [_ACTION_ADD, _ACTION_DELETE]
    _tree = None
    _deleteButton = None

    def __init__(self):
        # Returns the set of available actions
        self.setSpacing(True)
        # Create new Tree object using a hierarchical container from
        # ExampleUtil class
        self._tree = Tree('Hardware Inventory', ExampleUtil.getHardwareContainer())
        # Set multiselect mode
        self._tree.setMultiSelect(True)
        self._tree.setImmediate(True)

        class _0_(ValueChangeListener):

            def valueChange(self, event):
                t = event.getProperty()
                # enable if something is selected, returns a set
                TreeMultiSelectExample_this._deleteButton.setEnabled(t.getValue() is not None and len(t.getValue()) > 0)

        _0_ = _0_()
        self._tree.addListener(_0_)
        # Add Actionhandler
        self._tree.addActionHandler(self)
        # Set tree to show the 'name' property as caption for items
        self._tree.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        self._tree.setItemCaptionMode(AbstractSelect.ITEM_CAPTION_MODE_PROPERTY)
        # Expand whole tree
        _0 = True
        it = self._tree.rootItemIds()
        while True:
            if _0 is True:
                _0 = False
            if not it.hasNext():
                break
            self._tree.expandItemsRecursively(it.next())
        # Create the 'delete button', inline click-listener

        class _1_(Button.ClickListener):

            def buttonClick(self, event):
                # Delete all the selected objects
                toDelete = list(TreeMultiSelectExample_this._tree.getValue())
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(toDelete)):
                        break
                    TreeMultiSelectExample_this.handleAction(TreeMultiSelectExample_this._ACTION_DELETE, TreeMultiSelectExample_this._tree, toDelete[i])

        _1_ = _1_()
        Button('Delete', _1_)
        self._deleteButton = _1_
        self._deleteButton.setEnabled(False)
        self.addComponent(self._deleteButton)
        self.addComponent(self._tree)

    def getActions(self, target, sender):
        # Handle actions
        return self._ACTIONS

    def handleAction(self, action, sender, target):
        if action == self._ACTION_ADD:
            # Allow children for the target item
            self._tree.setChildrenAllowed(target, True)
            # Create new item, disallow children, add name, set parent
            itemId = self._tree.addItem()
            self._tree.setChildrenAllowed(itemId, False)
            newItemName = 'New Item # ' + itemId
            item = self._tree.getItem(itemId)
            item.getItemProperty(ExampleUtil.hw_PROPERTY_NAME).setValue(newItemName)
            self._tree.setParent(itemId, target)
            self._tree.expandItem(target)
        elif action == self._ACTION_DELETE:
            parent = self._tree.getParent(target)
            self._tree.removeItem(target)
            # If the deleted object's parent has no more children, set it's
            # childrenallowed property to false
            if parent is not None and len(self._tree.getChildren(parent)) == 0:
                self._tree.setChildrenAllowed(parent, False)
