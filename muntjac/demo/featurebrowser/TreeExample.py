# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.vaadin.ui.TextField import (TextField,)


class TreeExample(CustomComponent, Action.Handler, Tree.ValueChangeListener):
    """Demonstrates basic Tree -functionality. Actions are used for add/remove item
    functionality, and a ValueChangeListener reacts to both the Tree and the
    TextField.
    """
    _ADD = Action('Add item')
    _DELETE = Action('Delete item')
    _actions = [_ADD, _DELETE]
    # Id for the caption property
    _CAPTION_PROPERTY = 'caption'
    _desc = 'Try both right- and left-click!'
    _tree = None
    _editor = None

    def __init__(self):
        main = HorizontalLayout()
        main.setWidth('100%')
        main.setMargin(True)
        self.setCompositionRoot(main)
        # Panel w/ Tree
        p = Panel('Select item')
        p.setStyleName(Reindeer.PANEL_LIGHT)
        p.setWidth('250px')
        # Description
        p.addComponent(Label(self._desc))
        # Tree with a few items
        self._tree = Tree()
        self._tree.setImmediate(True)
        # we'll use a property for caption instead of the item id ("value"),
        # so that multiple items can have the same caption
        self._tree.addContainerProperty(self._CAPTION_PROPERTY, str, '')
        self._tree.setItemCaptionMode(AbstractSelect.ITEM_CAPTION_MODE_PROPERTY)
        self._tree.setItemCaptionPropertyId(self._CAPTION_PROPERTY)
        _0 = True
        i = 1
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i <= 3):
                break
            id = self.addCaptionedItem('Section ' + i, None)
            self._tree.expandItem(id)
            self.addCaptionedItem('Team A', id)
            self.addCaptionedItem('Team B', id)
        # listen for selections
        self._tree.addListener(self)
        # "context menu"
        self._tree.addActionHandler(self)
        p.addComponent(self._tree)
        main.addComponent(p)
        # Panel w/ TextField ("editor")
        p = Panel('Edit item caption')
        p.setStyleName(Reindeer.PANEL_LIGHT)
        self._editor = TextField()
        # make immediate, instead of adding an "apply" button
        self._editor.setImmediate(True)
        self._editor.setEnabled(False)
        self._editor.setColumns(15)
        p.addComponent(self._editor)
        main.addComponent(p)
        main.setExpandRatio(p, 1)

    def getActions(self, target, sender):
        # We can provide different actions for each target (item), but we'll
        # use the same actions all the time.
        return self._actions

    def handleAction(self, action, sender, target):
        if action == self._DELETE:
            self._tree.removeItem(target)
        else:
            # Add
            id = self.addCaptionedItem('New Item', target)
            self._tree.expandItem(target)
            self._tree.setValue(id)
            self._editor.focus()

    def valueChange(self, event):
        id = self._tree.getValue()
        # selected item id
        if event.getProperty() == self._tree:
            # a Tree item was (un) selected
            if id is None:
                # no selecteion, disable TextField
                self._editor.removeListener(self)
                self._editor.setValue('')
                self._editor.setEnabled(False)
            else:
                # item selected
                # first remove previous listener
                self._editor.removeListener(self)
                # enable TextField and update value
                self._editor.setEnabled(True)
                item = self._tree.getItem(id)
                self._editor.setValue(item.getItemProperty(self._CAPTION_PROPERTY).getValue())
                # listen for TextField changes
                self._editor.addListener(self)
                self._editor.focus()
        elif id is not None:
            item = self._tree.getItem(id)
            p = item.getItemProperty(self._CAPTION_PROPERTY)
            p.setValue(self._editor.getValue())
            self._tree.requestRepaint()
        # TextField

    def addCaptionedItem(self, caption, parent):
        """Helper to add an item with specified caption and (optional) parent.

        @param caption
                   The item caption
        @param parent
                   The (optional) parent item id
        @return the created item's id
        """
        # add item, let tree decide id
        id = self._tree.addItem()
        # get the created item
        item = self._tree.getItem(id)
        # set our "caption" property
        p = item.getItemProperty(self._CAPTION_PROPERTY)
        p.setValue(caption)
        if parent is not None:
            self._tree.setChildrenAllowed(parent, True)
            self._tree.setParent(id, parent)
            self._tree.setChildrenAllowed(id, False)
        return id
