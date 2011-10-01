# Copyright (C) 2010 IT Mill Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import deque
from Queue import LifoQueue

from muntjac.terminal import clsname
from muntjac.terminal.KeyMapper import KeyMapper
from muntjac.terminal.gwt.client.MouseEventDetails import MouseEventDetails

from muntjac.data import IContainer

from muntjac.ui.AbstractComponent import AbstractComponent

from muntjac.event import Action
from muntjac.event.DataBoundTransferable import DataBoundTransferable
from muntjac.event.dd.acceptcriteria.TargetDetailIs import TargetDetailIs
from muntjac.event.dd.IDropTarget import IDropTarget
from muntjac.event.dd.IDragSource import IDragSource

from muntjac.event.dd.acceptcriteria.ServerSideCriterion import \
    ServerSideCriterion

from muntjac.event.dd.acceptcriteria.ClientSideCriterion import \
    ClientSideCriterion

from muntjac.event.ItemClickEvent import \
    ItemClickEvent, IItemClickNotifier, IItemClickSource

from muntjac.ui.IComponent import Event as ComponentEvent

from muntjac.ui.AbstractSelect import \
    AbstractSelect, MultiSelectMode, AbstractSelectTargetDetails

from muntjac.terminal.gwt.client.ui.VTree import \
    VTree

from muntjac.terminal.gwt.client.ui.dd.VerticalDropLocation import \
    VerticalDropLocation


class Tree(AbstractSelect, IContainer.IHierarchical, Action.IContainer,
           IItemClickSource, IItemClickNotifier, IDragSource, IDropTarget):
    """Tree component. A Tree can be used to select an item (or multiple
    items) from a hierarchical set of items.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    #CLIENT_WIDGET = ClientWidget(VTree, LoadStyle.EAGER)

    def __init__(self, caption=None, dataSource=None):
        """Creates a new tree with caption and connect it to a IContainer.

        @param caption
        @param dataSource
        """
        # Set of expanded nodes.
        self._expanded = set()

        # List of action handlers.
        self._actionHandlers = None

        # Action mapper.
        self._actionMapper = None

        # Is the tree selectable on the client side.
        self._selectable = True

        # Flag to indicate sub-tree loading
        self._partialUpdate = False

        # Holds a itemId which was recently expanded
        self._expandedItemId = None

        # a flag which indicates initial paint. After this flag set
        # true partial updates are allowed.
        self._initialPaint = True

        self._dragMode = TreeDragMode.NONE
        self._multiSelectMode = MultiSelectMode.DEFAULT

        if caption is not None:
            self.setCaption(caption)

        if dataSource is not None:
            self.setContainerDataSource(dataSource)

        self._itemStyleGenerator = None
        self._dropHandler = None

    # Expanding and collapsing

    def isExpanded(self, itemId):
        """Check is an item is expanded

        @param itemId
                   the item id.
        @return true iff the item is expanded.
        """
        return itemId in self._expanded


    def expandItem(self, itemId, sendChildTree=None):
        """Expands an item.

        @param itemId
                   the item id.
        @return True iff the expand operation succeeded
        ---
        Expands an item.

        @param itemId
                   the item id.
        @param sendChildTree
                   flag to indicate if client needs subtree or not (may
                   be cached)
        @return True iff the expand operation succeeded
        """
        if sendChildTree is None:
            success = self.expandItem(itemId, True)
            self.requestRepaint()
            return success
        else:
            # Succeeds if the node is already expanded
            if self.isExpanded(itemId):
                return True

            # Nodes that can not have children are not expandable
            if not self.areChildrenAllowed(itemId):
                return False

            # Expands
            self._expanded.add(itemId)

            self._expandedItemId = itemId
            if self._initialPaint:
                self.requestRepaint()
            elif sendChildTree:
                self.requestPartialRepaint()

            self.fireExpandEvent(itemId)

            return True


    def requestRepaint(self):
        super(Tree, self).requestRepaint()
        self._partialUpdate = False


    def requestPartialRepaint(self):
        super(Tree, self).requestRepaint()
        self._partialUpdate = True


    def expandItemsRecursively(self, startItemId):
        """Expands the items recursively

        Expands all the children recursively starting from an item.
        Operation succeeds only if all expandable items are expanded.

        @param startItemId
        @return True iff the expand operation succeeded
        """
        result = True

        # Initial stack
        todo = LifoQueue
        todo.put(startItemId)
        # Expands recursively
        while not todo.empty():
            idd = todo.get()
            if (self.areChildrenAllowed(idd)
                    and not self.expandItem(idd, False)):
                result = False
            if self.hasChildren(idd):
                for c in self.getChildren(idd):
                    todo.put(c)

        self.requestRepaint()
        return result


    def collapseItem(self, itemId):
        """Collapses an item.

        @param itemId
                   the item id.
        @return True iff the collapse operation succeeded
        """
        # Succeeds if the node is already collapsed
        if not self.isExpanded(itemId):
            return True

        # Collapse
        self._expanded.remove(itemId)
        self.requestRepaint()
        self.fireCollapseEvent(itemId)
        return True


    def collapseItemsRecursively(self, startItemId):
        """Collapses the items recursively.

        Collapse all the children recursively starting from an item.
        Operation succeeds only if all expandable items are collapsed.

        @param startItemId
        @return True iff the collapse operation succeeded
        """
        result = True

        # Initial stack
        todo = LifoQueue
        todo.put(startItemId)

        # Collapse recursively
        while not todo.isEmpty():
            idd = todo.get()
            if self.areChildrenAllowed(idd) and not self.collapseItem(idd):
                result = False
            if self.hasChildren(idd):
                for c in self.getChildren(idd):
                    todo.put(c)

        return result


    def isSelectable(self):
        """Returns the current selectable state. Selectable determines if the
        a node can be selected on the client side. Selectable does not affect
        {@link #setValue(Object)} or {@link #select(Object)}.

        The tree is selectable by default.

        @return the current selectable state.
        """
        return self._selectable


    def setSelectable(self, selectable):
        """Sets the selectable state. Selectable determines if the a node can
        be selected on the client side. Selectable does not affect
        {@link #setValue(Object)} or {@link #select(Object)}.

        The tree is selectable by default.

        @param selectable
                   The new selectable state.
        """
        if self._selectable != selectable:
            self._selectable = selectable
            self.requestRepaint()


    def setMultiselectMode(self, mode):
        """Sets the behavior of the multiselect mode

        @param mode
                   The mode to set
        """
        if self._multiSelectMode != mode and mode is not None:
            self._multiSelectMode = mode
            self.requestRepaint()


    def getMultiselectMode(self):
        """Returns the mode the multiselect is in. The mode controls
        how multiselection can be done.

        @return The mode
        """
        return self._multiSelectMode


    def changeVariables(self, source, variables):
        if 'clickedKey' in variables:
            key = variables.get('clickedKey')

            idd = self.itemIdMapper.get(key)
            evt = variables.get('clickEvent')
            details = MouseEventDetails.deSerialize(evt)
            item = self.getItem(idd)
            if item is not None:
                event = ItemClickEvent(self, item, idd, None, details)
                self.fireEvent(event)

        if not self.isSelectable() and 'selected' in variables:
            # Not-selectable is a special case, AbstractSelect does not
            # support. TODO: could be optimized.
            variables = dict(variables)
            del variables['selected']

        # Collapses the nodes
        if 'collapse' in variables:
            keys = variables.get('collapse')
            for key in keys:
                idd = self.itemIdMapper.get(key)
                if idd is not None and self.isExpanded(idd):
                    self._expanded.remove(idd)
                    self.fireCollapseEvent(idd)

        # Expands the nodes
        if 'expand' in variables:
            sendChildTree = False
            if 'requestChildTree' in variables:
                sendChildTree = True

            keys = variables.get('expand')
            for key in keys:
                idd = self.itemIdMapper.get(key)
                if idd is not None:
                    self.expandItem(idd, sendChildTree)

        # AbstractSelect cannot handle multiselection so we
        # handle it ourself
        if ('selected' in variables
                and self.isMultiSelect()
                and self._multiSelectMode == MultiSelectMode.DEFAULT):
            self.handleSelectedItems(variables)
            variables = dict(variables)
            del variables['selected']

        # Selections are handled by the select component
        super(Tree, self).changeVariables(source, variables)

        # Actions
        if 'action' in variables:
            st = variables.get('action').split(',')  # FIXME: StringTokenizer
            if len(st) == 2:
                itemId = self.itemIdMapper.get(st[0].strip())
                action = self._actionMapper.get(st[1].strip())
                if (action is not None
                        and (itemId is None)
                        or self.containsId(itemId)
                        and self._actionHandlers is not None):
                    for ah in self._actionHandlers:
                        ah.handleAction(action, self, itemId)


    def handleSelectedItems(self, variables):
        """Handles the selection

        @param variables
                   The variables sent to the server from the client
        """
        ka = variables.get('selected')

        # Converts the key-array to id-set
        s = list()
        for i in range(len(ka)):
            idd = self.itemIdMapper.get(ka[i])
            if (not self.isNullSelectionAllowed()
                    and (idd is None)
                    or (idd == self.getNullSelectionItemId())):
                # skip empty selection if null selection is not allowed
                self.requestRepaint()
            elif idd is not None and self.containsId(idd):
                s.append(idd)

        if not self.isNullSelectionAllowed() and len(s) < 1:
            # empty selection not allowed, keep old value
            self.requestRepaint()
            return

        self.setValue(s, True)


    def paintContent(self, target):
        """Paints any needed component-specific things to the given UIDL
        stream.

        @see com.vaadin.ui.AbstractComponent#paintContent(PaintTarget)
        """
        self._initialPaint = False

        if self._partialUpdate:
            target.addAttribute('partialUpdate', True)
            target.addAttribute('rootKey',
                    self.itemIdMapper.key(self._expandedItemId))
        else:
            self.getCaptionChangeListener().clear()

            # The tab ordering number
            if self.getTabIndex() > 0:
                target.addAttribute('tabindex', self.getTabIndex())

            # Paint tree attributes
            if self.isSelectable():
                if self.isMultiSelect():
                    target.addAttribute('selectmode', 'multi')
                else:
                    target.addAttribute('selectmode', 'single')

                if self.isMultiSelect():
                    target.addAttribute('multiselectmode',
                        MultiSelectMode.values().index(self._multiSelectMode))
            else:
                target.addAttribute('selectmode', 'none')

            if self.isNewItemsAllowed():
                target.addAttribute('allownewitem', True)

            if self.isNullSelectionAllowed():
                target.addAttribute('nullselect', True)

            if self._dragMode != TreeDragMode.NONE:
                target.addAttribute('dragMode', self._dragMode)

        # Initialize variables
        actionSet = set()

        # rendered selectedKeys
        selectedKeys = list()
        expandedKeys = list()

        # Iterates through hierarchical tree using a stack of iterators
        iteratorStack = deque()
        if self._partialUpdate:
            ids = self.getChildren(self._expandedItemId)
        else:
            ids = self.rootItemIds()

        if ids is not None:
            iteratorStack.append(ids)

        # Body actions - Actions which has the target null and can be invoked
        # by right clicking on the Tree body
        if self._actionHandlers is not None:
            keys = list()
            for ah in self._actionHandlers:

                # Getting action for the null item, which in this case
                # means the body item
                aa = ah.getActions(None, self)
                if aa is not None:
                    for ai in range(len(aa)):
                        akey = self._actionMapper.key(aa[ai])
                        actionSet.add(aa[ai])
                        keys.append(akey)

            target.addAttribute('alb', keys)

        while len(iteratorStack) > 0:

            # Gets the iterator for current tree level
            i = iteratorStack[-1]

            # If the level is finished, back to previous tree level
            try:
                # Adds the item on current level
                itemId = i.next()

                # Starts the item / node
                isNode = self.areChildrenAllowed(itemId)
                if isNode:
                    target.startTag('node')
                else:
                    target.startTag('leaf')

                if self._itemStyleGenerator is not None:
                    stylename = self._itemStyleGenerator.getStyle(itemId)
                    if stylename is not None:
                        target.addAttribute('style', stylename)

                # Adds the attributes
                target.addAttribute('caption', self.getItemCaption(itemId))
                icon = self.getItemIcon(itemId)
                if icon is not None:
                    target.addAttribute('icon', self.getItemIcon(itemId))

                key = self.itemIdMapper.key(itemId)
                target.addAttribute('key', key)
                if self.isSelected(itemId):
                    target.addAttribute('selected', True)
                    selectedKeys.append(key)

                if self.areChildrenAllowed(itemId) and self.isExpanded(itemId):
                    target.addAttribute('expanded', True)
                    expandedKeys.append(key)

                # Add caption change listener
                self.getCaptionChangeListener().addNotifierForItem(itemId)

                # Actions
                if self._actionHandlers is not None:
                    keys = list()
                    ahi = iter(self._actionHandlers)
                    while True:
                        try:
                            aa = ahi.next().getActions(itemId, self)
                            if aa is not None:
                                for ai in range(len(aa)):
                                    akey = self._actionMapper.key(aa[ai])
                                    actionSet.add(aa[ai])
                                    keys.append(akey)
                        except StopIteration:
                            break
                    target.addAttribute('al', keys)

                # Adds the children if expanded, or close the tag
                if (self.isExpanded(itemId)
                        and self.hasChildren(itemId)
                        and self.areChildrenAllowed(itemId)):
                    iteratorStack.append(self.getChildren(itemId))
                elif isNode:
                    target.endTag('node')
                else:
                    target.endTag('leaf')

            except StopIteration:
                # Removes used iterator from the stack
                iteratorStack.pop()

                # Closes node
                if len(iteratorStack) > 0:
                    target.endTag('node')

        # Actions
        if len(actionSet) > 0:
            target.addVariable(self, 'action', '')
            target.startTag('actions')
            i = actionSet
            for a in actionSet:
                target.startTag('action')
                if a.getCaption() is not None:
                    target.addAttribute('caption', a.getCaption())

                if a.getIcon() is not None:
                    target.addAttribute('icon', a.getIcon())

                target.addAttribute('key', self._actionMapper.key(a))
                target.endTag('action')

            target.endTag('actions')

        if self._partialUpdate:
            self._partialUpdate = False
        else:
            # Selected
            target.addVariable(self, 'selected', selectedKeys)

            # Expand and collapse
            target.addVariable(self, 'expand', list())
            target.addVariable(self, 'collapse', list())

            # New items
            target.addVariable(self, 'newitem', list())
            if self._dropHandler is not None:
                self._dropHandler.getAcceptCriterion().paint(target)


    def areChildrenAllowed(self, itemId):
        """Tests if the Item with given ID can have any children.

        @see IContainer.IHierarchical.areChildrenAllowed(Object)
        """
        return self.items.areChildrenAllowed(itemId)


    def getChildren(self, itemId):
        """Gets the IDs of all Items that are children of the specified Item.

        @see IContainer.IHierarchical.getChildren(Object)
        """
        return self.items.getChildren(itemId)


    def getParent(self, itemId):
        """Gets the ID of the parent Item of the specified Item.

        @see IContainer.IHierarchical.getParent(Object)
        """
        return self.items.getParent(itemId)


    def hasChildren(self, itemId):
        """Tests if the Item specified with <code>itemId</code> has child
        Items.

        @see IContainer.IHierarchical.hasChildren(Object)
        """
        return self.items.hasChildren(itemId)


    def isRoot(self, itemId):
        """Tests if the Item specified with <code>itemId</code> is a root
        Item.

        @see com.vaadin.data.IContainer.IHierarchical#isRoot(Object)
        """
        return self.items.isRoot(itemId)


    def rootItemIds(self):
        """Gets the IDs of all Items in the container that don't have a
        parent.

        @see com.vaadin.data.IContainer.IHierarchical#rootItemIds()
        """
        return self.items.rootItemIds()


    def setChildrenAllowed(self, itemId, areChildrenAllowed):
        """Sets the given Item's capability to have children.

        @see com.vaadin.data.IContainer.IHierarchical#setChildrenAllowed()
        """
        success = self.items.setChildrenAllowed(itemId, areChildrenAllowed)
        if success:
            self.requestRepaint()

        return success


    def setParent(self, itemId, newParentId):
        success = self.items.setParent(itemId, newParentId)
        if success:
            self.requestRepaint()

        return success


    def setContainerDataSource(self, newDataSource):
        """Sets the IContainer that serves as the data source of the viewer.

        @see IContainer.Viewer#setContainerDataSource(IContainer)
        """
        if newDataSource is None:
            # Note: using wrapped IndexedContainer to match constructor
            # (super creates an IndexedContainer, which is then wrapped).
            raise NotImplementedError
            #newDataSource = ContainerHierarchicalWrapper(IndexedContainer())

        # Assure that the data source is ordered by making unordered
        # containers ordered by wrapping them
        if issubclass(newDataSource.__class__, IContainer.IHierarchical):
            super(Tree, self).setContainerDataSource(newDataSource)
        else:
            raise NotImplementedError
            #super(Tree, self).setContainerDataSource(
            #    ContainerHierarchicalWrapper(newDataSource))


    def addListener(self, listener):
        """Adds the expand listener.

        @param listener
                   the Listener to be added.
        ---
        Adds the collapse listener.

        @param listener
                   the Listener to be added.
        """
        if isinstance(listener, ICollapseListener):
            AbstractComponent.addListener(self, CollapseEvent, listener,
                    ICollapseListener.COLLAPSE_METHOD)
        elif isinstance(listener, IExpandListener):
            AbstractComponent.addListener(self, ExpandEvent, listener,
                    IExpandListener.EXPAND_METHOD)
        else:
            AbstractComponent.addListener(self, VTree.ITEM_CLICK_EVENT_ID,
                    ItemClickEvent, listener,
                    ItemClickEvent.ITEM_CLICK_METHOD)


    def removeListener(self, listener):
        """Removes the expand listener.

        @param listener
                   the Listener to be removed.
        ---
        Removes the collapse listener.

        @param listener
                   the Listener to be removed.
        """
        if isinstance(listener, ICollapseListener):
            AbstractComponent.removeListener(self, CollapseEvent, listener,
                    ICollapseListener.COLLAPSE_METHOD)
        elif isinstance(listener, IExpandListener):
            AbstractComponent.removeListener(self, ExpandEvent, listener,
                    IExpandListener.EXPAND_METHOD)
        else:
            AbstractComponent.removeListener(self, VTree.ITEM_CLICK_EVENT_ID,
                    ItemClickEvent, listener)


    def fireExpandEvent(self, itemId):
        """Emits the expand event.

        @param itemId
                   the item id.
        """
        self.fireEvent( ExpandEvent(self, itemId) )


    def fireCollapseEvent(self, itemId):
        """Emits collapse event.

        @param itemId
                   the item id.
        """
        self.fireEvent( CollapseEvent(self, itemId) )


    def addActionHandler(self, actionHandler):
        """Adds an action handler.

        @see Action.IContainer#addActionHandler(Action.Handler)
        """
        if actionHandler is not None:
            if self._actionHandlers is None:
                self._actionHandlers = list()
                self._actionMapper = KeyMapper()
            if actionHandler not in self._actionHandlers:
                self._actionHandlers.append(actionHandler)
                self.requestRepaint()


    def removeActionHandler(self, actionHandler):
        """Removes an action handler.

        @see Action.IContainer#removeActionHandler(Action.Handler)
        """
        if (self._actionHandlers is not None
                and actionHandler in self._actionHandlers):
            self._actionHandlers.remove(actionHandler)
            if len(self._actionHandlers) > 0:
                self._actionHandlers = None
                self._actionMapper = None
            self.requestRepaint()


    def removeAllActionHandlers(self):
        """Removes all action handlers"""
        self._actionHandlers = None
        self._actionMapper = None
        self.requestRepaint()


    def getVisibleItemIds(self):
        """Gets the visible item ids.

        @see com.vaadin.ui.Select#getVisibleItemIds()
        """
        visible = list()
        # Iterates trough hierarchical tree using a stack of iterators
        iteratorStack = deque()
        ids = self.rootItemIds()
        if ids is not None:
            iteratorStack.append(ids)
        while len(iteratorStack) > 0:
            # Gets the iterator for current tree level
            i = iter( iteratorStack[-1] )

            # If the level is finished, back to previous tree level
            try:
                itemId = i.next()
                visible.append(itemId)
                # Adds children if expanded, or close the tag
                if self.isExpanded(itemId) and self.hasChildren(itemId):
                    iteratorStack.append( self.getChildren(itemId) )
            except StopIteration:
                # Removes used iterator from the stack
                # Adds the item on current level
                iteratorStack.pop()

        return visible


    def setNullSelectionItemId(self, nullSelectionItemId):
        """Tree does not support <code>setNullSelectionItemId</code>.

        @see AbstractSelect#setNullSelectionItemId(java.lang.Object)
        """
        if nullSelectionItemId is not None:
            raise NotImplementedError


    def setNewItemsAllowed(self, allowNewOptions):
        """Adding new items is not supported.

        @throws UnsupportedOperationException
                    if set to true.
        @see com.vaadin.ui.Select#setNewItemsAllowed(boolean)
        """
        if allowNewOptions:
            raise NotImplementedError


    def setLazyLoading(self, useLazyLoading):
        """Tree does not support lazy options loading mode. Setting this
        true will throw UnsupportedOperationException.

        @see com.vaadin.ui.Select#setLazyLoading(boolean)
        """
        if useLazyLoading:
            raise NotImplementedError, \
                    'Lazy options loading is not supported by Tree.'


    def setItemStyleGenerator(self, itemStyleGenerator):
        """Sets the {@link IItemStyleGenerator} to be used with this tree.

        @param itemStyleGenerator
                   item style generator or null to remove generator
        """
        if self._itemStyleGenerator != itemStyleGenerator:
            self._itemStyleGenerator = itemStyleGenerator
            self.requestRepaint()


    def getItemStyleGenerator(self):
        """@return the current {@link IItemStyleGenerator} for this tree.
                   Null if {@link IItemStyleGenerator} is not set.
        """
        return self._itemStyleGenerator


    def removeItem(self, itemId):
        return super(Tree, self).removeItem(itemId)


    def getDropHandler(self):
        return self._dropHandler


    def setDropHandler(self, dropHandler):
        self._dropHandler = dropHandler


    def translateDropTargetDetails(self, clientVariables):
        return TreeTargetDetails(clientVariables)


    def key(self, itemId):
        """Helper API for {@link TreeDropCriterion}

        @param itemId
        @return
        """
        return self.itemIdMapper.key(itemId)


    def setDragMode(self, dragMode):
        """Sets the drag mode that controls how Tree behaves as a
        {@link IDragSource}.

        @param dragMode
        """
        self._dragMode = dragMode
        self.requestRepaint()


    def getDragMode(self):
        """@return the drag mode that controls how Tree behaves as a
                   {@link IDragSource}.

        @see TreeDragMode
        """
        return self._dragMode


    def getTransferable(self, payload):
        transferable = TreeTransferable(self, payload)
        # updating drag source variables
        obj = payload.get('itemId')

        if obj is not None:
            transferable.setData('itemId', self.itemIdMapper.get(obj))

        return transferable


class TreeDragMode(object):
    """Supported drag modes for Tree."""
    # When drag mode is NONE, dragging from Tree is not supported. Browsers
    # may still support selecting text/icons from Tree which can initiate
    # HTML 5 style drag and drop operation.
    NONE = 'NONE'

    # When drag mode is NODE, users can initiate drag from Tree nodes that
    # represent {@link Item}s in from the backed {@link IContainer}.
    NODE = 'NODE'

    _values = [NONE, NODE]

    @classmethod
    def values(cls):
        return cls._enum_values[:]


class ExpandEvent(ComponentEvent):
    """Event to fired when a node is expanded. ExapandEvent is fired when a
    node is to be expanded. it can me used to dynamically fill the sub-nodes
    of the node.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, source, expandedItemId):
        """New instance of options change event

        @param source
                   the Source of the event.
        @param expandedItemId
        """
        super(ExpandEvent, self)(source)
        self._expandedItemId = expandedItemId


    def getItemId(self):
        """Node where the event occurred.

        @return the Source of the event.
        """
        return self._expandedItemId


class IExpandListener(object):
    """Expand event listener.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def nodeExpand(self, event):
        """A node has been expanded.

        @param event
                   the Expand event.
        """
        raise NotImplementedError


    EXPAND_METHOD = nodeExpand


class CollapseEvent(ComponentEvent):
    """Collapse event

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, source, collapsedItemId):
        """New instance of options change event.

        @param source
                   the Source of the event.
        @param collapsedItemId
        """
        super(CollapseEvent, self)(source)
        self._collapsedItemId = collapsedItemId


    def getItemId(self):
        """Gets tge Collapsed Item id.

        @return the collapsed item id.
        """
        return self._collapsedItemId


class ICollapseListener(object):
    """Collapse event listener.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def nodeCollapse(self, event):
        """A node has been collapsed.

        @param event
                   the Collapse event.
        """
        raise NotImplementedError

    COLLAPSE_METHOD = nodeCollapse


class IItemStyleGenerator(object):
    """IItemStyleGenerator can be used to add custom styles to tree items.
    The CSS class name that will be added to the cell content is
    <tt>v-tree-node-[style name]</tt>.
    """

    def getStyle(self, itemId):
        """Called by Tree when an item is painted.

        @param itemId
                   The itemId of the item to be painted
        @return The style name to add to this item. (the CSS class name
                will be v-tree-node-[style name]
        """
        raise NotImplementedError


class TreeTargetDetails(AbstractSelectTargetDetails):
    """A {@link TargetDetails} implementation with Tree specific api.

    @since 6.3
    """

    def __init__(self, rawVariables):
        super(TreeTargetDetails, self)(rawVariables)


    def getTarget(self):
        return super(TreeTargetDetails, self).getTarget()


    def getItemIdInto(self):
        """If the event is on a node that can not have children (see
        {@link Tree#areChildrenAllowed(Object)}), this method returns the
        parent item id of the target item (see {@link #getItemIdOver()} ).
        The identifier of the parent node is also returned if the cursor is
        on the top part of node. Else this method returns the same as
        {@link #getItemIdOver()}.

        In other words this method returns the identifier of the "folder"
        into the drag operation is targeted.

        If the method returns null, the current target is on a root node or
        on other undefined area over the tree component.

        The default Tree implementation marks the targetted tree node with
        CSS classnames v-tree-node-dragfolder and
        v-tree-node-caption-dragfolder (for the caption element).
        """
        itemIdOver = self.getItemIdOver()

        if (self.areChildrenAllowed(itemIdOver)
                and self.getDropLocation() == VerticalDropLocation.MIDDLE):
            return itemIdOver

        return self.getParent(itemIdOver)


    def getItemIdAfter(self):
        """If drop is targeted into "folder node" (see {@link
        #getItemIdInto()}), this method returns the item id of the node after
        the drag was targeted. This method is useful when implementing drop
        into specific location (between specific nodes) in tree.

        @return the id of the item after the user targets the drop or null if
                "target" is a first item in node list (or the first in root
                node list)
        """
        itemIdOver = self.getItemIdOver()
        itemIdInto2 = self.getItemIdInto()

        if itemIdOver == itemIdInto2:
            return None

        dropLocation = self.getDropLocation()

        if VerticalDropLocation.TOP == dropLocation:
            # if on top of the caption area, add before
            itemIdInto = self.getItemIdInto()
            if itemIdInto is not None:
                # seek the previous from child list
                children = self.getChildren(itemIdInto)
            else:
                children = self.rootItemIds()
            ref = None
            for obj in children:
                if obj == itemIdOver:
                    return ref
                ref = obj

        return itemIdOver


class TreeTransferable(DataBoundTransferable):
    """Concrete implementation of {@link DataBoundTransferable} for data
    transferred from a tree.

    @see {@link DataBoundTransferable}.

    @since 6.3
    """

    def __init__(self, sourceComponent, rawVariables):
        super(TreeTransferable, self)(sourceComponent, rawVariables)


    def getItemId(self):
        return self.getData('itemId')


    def getPropertyId(self):
        return self.getItemCaptionPropertyId()



class TreeDropCriterion(ServerSideCriterion):
    """Lazy loading accept criterion for Tree. Accepted target nodes are
    loaded from server once per drag and drop operation. Developer must
    override one method that decides accepted tree nodes for the whole Tree.

    Initially pretty much no data is sent to client. On first required
    criterion check (per drag request) the client side data structure is
    initialized from server and no subsequent requests requests are needed
    during that drag and drop operation.
    """

    def __init__(self):
        self._tree = None
        self._allowedItemIds = None


    def getIdentifier(self):
        return clsname(TreeDropCriterion)


    def accept(self, dragEvent):
        dropTargetData = dragEvent.getTargetDetails()
        self._tree = dragEvent.getTargetDetails().getTarget()
        self._allowedItemIds = self.getAllowedItemIds(dragEvent, self._tree)
        return dropTargetData.getItemIdOver() in self._allowedItemIds


    def paintResponse(self, target):
        # send allowed nodes to client so subsequent requests
        # can be avoided
        arry = list(self._allowedItemIds)
        for i in range(len(arry)):
            key = self._tree.key(arry[i])
            arry[i] = key
        target.addAttribute('allowedIds', arry)


    def getAllowedItemIds(self, dragEvent, tree):
        pass


class TargetItemAllowsChildren(TargetDetailIs):
    """A criterion that accepts {@link Transferable} only directly on a tree
    node that can have children.

    Class is singleton, use {@link TargetItemAllowsChildren#get()} to get the
    instance.

    @see Tree#setChildrenAllowed(Object, boolean)

    @since 6.3
    """

    INSTANCE = None

    @classmethod
    def get(cls):
        return cls.INSTANCE


    def __init__(self):
        # Uses enhanced server side check
        super(TargetItemAllowsChildren, self)('itemIdOverIsNode', True)


    def accept(self, dragEvent):
        try:
            # must be over tree node and in the middle of it (not top or
            # bottom part)
            eventDetails = dragEvent.getTargetDetails()

            itemIdOver = eventDetails.getItemIdOver()
            if not eventDetails.getTarget().areChildrenAllowed(itemIdOver):
                return False

            # return true if directly over
            return (eventDetails.getDropLocation()
                        == VerticalDropLocation.MIDDLE)
        except Exception:
            return False

TargetItemAllowsChildren.INSTANCE = TargetItemAllowsChildren()


class TargetInSubtree(ClientSideCriterion):
    """An accept criterion that checks the parent node (or parent hierarchy)
    for the item identifier given in constructor. If the parent is found,
    content is accepted. Criterion can be used to accepts drags on a specific
    sub tree only.

    The root items is also consider to be valid target.
    """

    def __init__(self, rootId, depthToCheck=None):
        """Constructs a criteria that accepts the drag if the targeted Item
        is a descendant of Item identified by given id

        @param parentItemId
                   the item identifier of the parent node
        ---
        Constructs a criteria that accepts drops within given level below the
        subtree root identified by given id.

        @param rootId
                   the item identifier to be sought for
        @param depthToCheck
                   the depth that tree is traversed upwards to seek for the
                   parent, -1 means that the whole structure should be
                   checked
        """
        self._rootId = rootId
        self._depthToCheck = -1

        if depthToCheck is not None:
            self._depthToCheck = depthToCheck


    def accept(self, dragEvent):
        try:
            eventDetails = dragEvent.getTargetDetails()

            if eventDetails.getItemIdOver() is not None:
                itemId = eventDetails.getItemIdOver()
                i = 0
                while (itemId is not None
                        and (self._depthToCheck == -1)
                        or (i <= self._depthToCheck)):
                    if itemId == self._rootId:
                        return True
                    itemId = self.getParent(itemId)
                    i += 1

            return False
        except Exception:
            return False


    def paintContent(self, target):
        super(TargetInSubtree, self).paintContent(target)
        target.addAttribute('depth', self._depthToCheck)
        target.addAttribute('key', self.key(self._rootId))
