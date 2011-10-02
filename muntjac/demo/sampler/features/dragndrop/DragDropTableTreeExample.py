# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.ExampleUtil import (ExampleUtil,)
# from com.vaadin.data.Container import (Container,)
# from com.vaadin.data.util.BeanItemContainer import (BeanItemContainer,)
# from com.vaadin.event.dd.acceptcriteria.And import (And,)
# from com.vaadin.event.dd.acceptcriteria.ClientSideCriterion import (ClientSideCriterion,)
# from com.vaadin.event.dd.acceptcriteria.SourceIs import (SourceIs,)
# from com.vaadin.ui.AbstractSelect.AcceptItem import (AcceptItem,)
# from com.vaadin.ui.Tree.TargetItemAllowsChildren import (TargetItemAllowsChildren,)
# from java.io.Serializable import (Serializable,)
# from java.util.Collection import (Collection,)
# from java.util.LinkedHashMap import (LinkedHashMap,)


class DragDropTableTreeExample(HorizontalLayout):
    """Demonstrate moving data back and forth between a table and a tree using drag
    and drop.

    The tree and the table use different data structures: The category is a
    separate node in the tree and each item just has a String, whereas the table
    contains items with both a name and a category. Data conversions between
    these representations are made during drop processing.
    """
    _tree = None
    _table = None

    class Hardware(Serializable):
        _name = None
        _category = None

        def __init__(self, name, category):
            self._name = name
            self._category = category

        def setName(self, name):
            self._name = name

        def getName(self):
            return self._name

        def setCategory(self, category):
            self._category = category

        def getCategory(self):
            return self._category

    def __init__(self):
        self.setSpacing(True)
        # First create the components to be able to refer to them as allowed
        # drag sources
        self._tree = Tree('Drag from tree to table')
        self._table = Table('Drag from table to tree')
        self._table.setWidth('100%')
        # Populate the tree and set up drag & drop
        self.initializeTree(SourceIs(self._table))
        # Populate the table and set up drag & drop
        self.initializeTable(SourceIs(self._tree))
        # Add components
        self.addComponent(self._tree)
        self.addComponent(self._table)

    def initializeTree(self, acceptCriterion):
        self._tree.setContainerDataSource(ExampleUtil.getHardwareContainer())
        self._tree.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        # Expand all nodes
        _0 = True
        it = self._tree.rootItemIds()
        while True:
            if _0 is True:
                _0 = False
            if not it.hasNext():
                break
            self._tree.expandItemsRecursively(it.next())
        self._tree.setDragMode(TreeDragMode.NODE)

        class _0_(DropHandler):

            def drop(self, dropEvent):
                # criteria verify that this is safe
                t = dropEvent.getTransferable()
                sourceContainer = t.getSourceContainer()
                sourceItemId = t.getItemId()
                sourceItem = sourceContainer.getItem(sourceItemId)
                name = str(sourceItem.getItemProperty('name'))
                category = str(sourceItem.getItemProperty('category'))
                dropData = dropEvent.getTargetDetails()
                targetItemId = dropData.getItemIdOver()
                # find category in target: the target node itself or its parent
                if targetItemId is not None and name is not None and category is not None:
                    treeCategory = DragDropTableTreeExample_this.getTreeNodeName(DragDropTableTreeExample_this._tree, targetItemId)
                    if category == treeCategory:
                        # move item from table to category'
                        newItemId = DragDropTableTreeExample_this._tree.addItem()
                        DragDropTableTreeExample_this._tree.getItem(newItemId).getItemProperty(ExampleUtil.hw_PROPERTY_NAME).setValue(name)
                        DragDropTableTreeExample_this._tree.setParent(newItemId, targetItemId)
                        DragDropTableTreeExample_this._tree.setChildrenAllowed(newItemId, False)
                        sourceContainer.removeItem(sourceItemId)
                    else:
                        message = name + ' is not a ' + treeCategory.toLowerCase().replaceAll('s$', '')
                        self.getWindow().showNotification(message, Notification.TYPE_WARNING_MESSAGE)

            def getAcceptCriterion(self):
                # Only allow dropping of data bound transferables within
                # folders.
                # In this example, checking for the correct category in drop()
                # rather than in the criteria.
                return And(self.acceptCriterion, TargetItemAllowsChildren.get(), AcceptItem.ALL)

        _0_ = _0_()
        self._tree.setDropHandler(_0_)

    def initializeTable(self, acceptCriterion):
        tableContainer = BeanItemContainer(self.Hardware)
        tableContainer.addItem(self.Hardware('Dell OptiPlex 380', 'Desktops'))
        tableContainer.addItem(self.Hardware('Benq T900HD', 'Monitors'))
        tableContainer.addItem(self.Hardware('Lenovo ThinkPad T500', 'Laptops'))
        self._table.setContainerDataSource(tableContainer)
        self._table.setVisibleColumns(['category', 'name'])
        # Handle drop in table: move hardware item or subtree to the table
        self._table.setDragMode(TableDragMode.ROW)

        class _1_(DropHandler):

            def drop(self, dropEvent):
                # criteria verify that this is safe
                t = dropEvent.getTransferable()
                if not isinstance(t.getSourceContainer(), Container.Hierarchical):
                    return
                source = t.getSourceContainer()
                sourceItemId = t.getItemId()
                # find and convert the item(s) to move
                parentItemId = source.getParent(sourceItemId)
                # map from moved source item Id to the corresponding Hardware
                hardwareMap = LinkedHashMap()
                if parentItemId is None:
                    # move the whole subtree
                    category = DragDropTableTreeExample_this.getTreeNodeName(source, sourceItemId)
                    children = source.getChildren(sourceItemId)
                    if children is not None:
                        for childId in children:
                            name = DragDropTableTreeExample_this.getTreeNodeName(source, childId)
                            hardwareMap.put(childId, DragDropTableTreeExample_this.Hardware(name, category))
                else:
                    # move a single hardware item
                    category = DragDropTableTreeExample_this.getTreeNodeName(source, parentItemId)
                    name = DragDropTableTreeExample_this.getTreeNodeName(source, sourceItemId)
                    hardwareMap.put(sourceItemId, DragDropTableTreeExample_this.Hardware(name, category))
                # move item(s) to the correct location in the table
                dropData = dropEvent.getTargetDetails()
                targetItemId = dropData.getItemIdOver()
                for sourceId in hardwareMap.keys():
                    hardware = hardwareMap.get(sourceId)
                    if targetItemId is not None:
                        _0 = dropData.getDropLocation()
                        _1 = False
                        while True:
                            if _0 == self.BOTTOM:
                                _1 = True
                                self.tableContainer.addItemAfter(targetItemId, hardware)
                                break
                            if (_1 is True) or (_0 == self.MIDDLE):
                                _1 = True
                            if (_1 is True) or (_0 == self.TOP):
                                _1 = True
                                prevItemId = self.tableContainer.prevItemId(targetItemId)
                                self.tableContainer.addItemAfter(prevItemId, hardware)
                                break
                            break
                    else:
                        self.tableContainer.addItem(hardware)
                    source.removeItem(sourceId)

            def getAcceptCriterion(self):
                return And(self.acceptCriterion, AcceptItem.ALL)

        _1_ = _1_()
        self._table.setDropHandler(_1_)

    @classmethod
    def getTreeNodeName(cls, source, sourceId):
        return source.getItem(sourceId).getItemProperty(ExampleUtil.hw_PROPERTY_NAME).getValue()
