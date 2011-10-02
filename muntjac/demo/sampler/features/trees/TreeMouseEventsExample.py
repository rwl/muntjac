# -*- coding: utf-8 -*-
from __pyjamas__ import (POSTINC,)
from com.vaadin.demo.sampler.ExampleUtil import (ExampleUtil,)


class TreeMouseEventsExample(VerticalLayout, ItemClickListener):
    _t = None
    _itemId = None

    def __init__(self):
        self.setSpacing(True)
        # Create new Tree object using a hierarchical container from
        # ExampleUtil class
        self._t = Tree('Hardware Inventory', ExampleUtil.getHardwareContainer())
        # Add ItemClickListener to the tree
        self._t.addListener(self)
        self._t.setImmediate(True)
        # Set tree to show the 'name' property as caption for items
        self._t.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        self._t.setItemCaptionMode(AbstractSelect.ITEM_CAPTION_MODE_PROPERTY)
        # Starting itemId # for new items
        self._itemId = len(self._t.getContainerDataSource())
        # Expand whole tree
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < self._itemId):
                break
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
        _0 = event.getButton()
        _1 = False
        while True:
            if _0 == ItemClickEvent.BUTTON_LEFT:
                _1 = True
                self.getWindow().showNotification('Selected item: ' + event.getItem(), modifiers)
                break
            if (_1 is True) or (_0 == ItemClickEvent.BUTTON_MIDDLE):
                _1 = True
                parent = self._t.getParent(event.getItemId())
                self.getWindow().showNotification('Removed item: ' + event.getItem(), modifiers)
                self._t.removeItem(event.getItemId())
                if parent is not None and len(self._t.getChildren(parent)) == 0:
                    self._t.setChildrenAllowed(parent, False)
                break
            if (_1 is True) or (_0 == ItemClickEvent.BUTTON_RIGHT):
                _1 = True
                self.getWindow().showNotification('Added item: New Item # ' + self._itemId, modifiers)
                self._t.setChildrenAllowed(event.getItemId(), True)
                i = self._t.addItem(self._itemId)
                self._t.setChildrenAllowed(self._itemId, False)
                newItemName = 'New Item # ' + self._itemId
                i.getItemProperty(ExampleUtil.hw_PROPERTY_NAME).setValue(newItemName)
                self._t.setParent(self._itemId, event.getItemId())
                self._t.expandItem(event.getItemId())
                POSTINC(globals(), locals(), 'self._itemId')
                break
            break
