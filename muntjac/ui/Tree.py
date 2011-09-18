# Copyright (C) 2011 Vaadin Ltd
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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.VTree import (VTree,)
from com.vaadin.event.dd.acceptcriteria.TargetDetailIs import (TargetDetailIs,)
from com.vaadin.event.dd.DropTarget import (DropTarget,)
from com.vaadin.data.util.ContainerHierarchicalWrapper import (ContainerHierarchicalWrapper,)
from com.vaadin.tools.ReflectTools import (ReflectTools,)
from com.vaadin.terminal.KeyMapper import (KeyMapper,)
from com.vaadin.data.Container import (Container, Hierarchical,)
from com.vaadin.event.Action import (Action,)
from com.vaadin.event.dd.acceptcriteria.ServerSideCriterion import (ServerSideCriterion,)
from com.vaadin.event.dd.DragSource import (DragSource,)
from com.vaadin.event.dd.acceptcriteria.ClientSideCriterion import (ClientSideCriterion,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
from com.vaadin.ui.AbstractSelect import (AbstractSelect,)
from com.vaadin.event.ItemClickEvent import (ItemClickEvent, ItemClickNotifier, ItemClickSource,)
from com.vaadin.event.DataBoundTransferable import (DataBoundTransferable,)
from com.vaadin.data.util.IndexedContainer import (IndexedContainer,)
from com.vaadin.terminal.gwt.client.ui.dd.VerticalDropLocation import (VerticalDropLocation,)
# from java.io.Serializable import (Serializable,)
# from java.lang.reflect.Method import (Method,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.HashMap import (HashMap,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedHashSet import (LinkedHashSet,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.Map import (Map,)
# from java.util.Set import (Set,)
# from java.util.Stack import (Stack,)
# from java.util.StringTokenizer import (StringTokenizer,)


class Tree(AbstractSelect, Container, Hierarchical, Action, Container, ItemClickSource, ItemClickNotifier, DragSource, DropTarget):
    """Tree component. A Tree can be used to select an item (or multiple items) from
    a hierarchical set of items.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Private members
    # Set of expanded nodes.
    _expanded = set()
    # List of action handlers.
    _actionHandlers = None
    # Action mapper.
    _actionMapper = None
    # Is the tree selectable on the client side.
    _selectable = True
    # Flag to indicate sub-tree loading
    _partialUpdate = False
    # Holds a itemId which was recently expanded
    _expandedItemId = None
    # a flag which indicates initial paint. After this flag set true partial
    # updates are allowed.

    _initialPaint = True

    class TreeDragMode(object):
        """Supported drag modes for Tree."""
        # When drag mode is NONE, dragging from Tree is not supported. Browsers
        # may still support selecting text/icons from Tree which can initiate
        # HTML 5 style drag and drop operation.

        # When drag mode is NODE, users can initiate drag from Tree nodes that
        # represent {@link Item}s in from the backed {@link Container}.

        NONE = 'NONE'
        NODE = 'NODE'
        _values = [NONE, NODE]

        @classmethod
        def values(cls):
            return cls._enum_values[:]

    _dragMode = TreeDragMode.NONE
    _multiSelectMode = MultiSelectMode.DEFAULT
    # Tree constructors

    def __init__(self, *args):
        """Creates a new empty tree.
        ---
        Creates a new empty tree with caption.

        @param caption
        ---
        Creates a new tree with caption and connect it to a Container.

        @param caption
        @param dataSource
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 1:
            caption, = _0
            self.setCaption(caption)
        elif _1 == 2:
            caption, dataSource = _0
            self.setCaption(caption)
            self.setContainerDataSource(dataSource)
        else:
            raise ARGERROR(0, 2)

    # Expanding and collapsing

    def isExpanded(self, itemId):
        """Check is an item is expanded

        @param itemId
                   the item id.
        @return true iff the item is expanded.
        """
        return itemId in self._expanded

    def expandItem(self, *args):
        """Expands an item.

        @param itemId
                   the item id.
        @return True iff the expand operation succeeded
        ---
        Expands an item.

        @param itemId
                   the item id.
        @param sendChildTree
                   flag to indicate if client needs subtree or not (may be
                   cached)
        @return True iff the expand operation succeeded
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            itemId, = _0
            success = self.expandItem(itemId, True)
            self.requestRepaint()
            return success
        elif _1 == 2:
            itemId, sendChildTree = _0
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
        else:
            raise ARGERROR(1, 2)

    # Succeeds if the node is already expanded

    def requestRepaint(self):
        super(Tree, self).requestRepaint()
        self._partialUpdate = False

    def requestPartialRepaint(self):
        super(Tree, self).requestRepaint()
        self._partialUpdate = True

    def expandItemsRecursively(self, startItemId):
        """Expands the items recursively

        Expands all the children recursively starting from an item. Operation
        succeeds only if all expandable items are expanded.

        @param startItemId
        @return True iff the expand operation succeeded
        """
        result = True
        # Initial stack
        todo = Stack()
        todo.add(startItemId)
        # Expands recursively
        while not todo.isEmpty():
            id = todo.pop()
            if self.areChildrenAllowed(id) and not self.expandItem(id, False):
                result = False
            if self.hasChildren(id):
                todo.addAll(self.getChildren(id))
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

        Collapse all the children recursively starting from an item. Operation
        succeeds only if all expandable items are collapsed.

        @param startItemId
        @return True iff the collapse operation succeeded
        """
        result = True
        # Initial stack
        todo = Stack()
        todo.add(startItemId)
        # Collapse recursively
        while not todo.isEmpty():
            id = todo.pop()
            if self.areChildrenAllowed(id) and not self.collapseItem(id):
                result = False
            if self.hasChildren(id):
                todo.addAll(self.getChildren(id))
        return result

    def isSelectable(self):
        """Returns the current selectable state. Selectable determines if the a node
        can be selected on the client side. Selectable does not affect
        {@link #setValue(Object)} or {@link #select(Object)}.

        <p>
        The tree is selectable by default.
        </p>

        @return the current selectable state.
        """
        return self._selectable

    def setSelectable(self, selectable):
        """Sets the selectable state. Selectable determines if the a node can be
        selected on the client side. Selectable does not affect
        {@link #setValue(Object)} or {@link #select(Object)}.

        <p>
        The tree is selectable by default.
        </p>

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
        """Returns the mode the multiselect is in. The mode controls how
        multiselection can be done.

        @return The mode
        """
        # Component API
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.AbstractSelect#changeVariables(java.lang.Object,
        # java.util.Map)

        return self._multiSelectMode

    def changeVariables(self, source, variables):
        if 'clickedKey' in variables:
            key = variables['clickedKey']
            id = self.itemIdMapper.get(key)
            details = MouseEventDetails.deSerialize(variables['clickEvent'])
            item = self.getItem(id)
            if item is not None:
                self.fireEvent(ItemClickEvent(self, item, id, None, details))
        if not self.isSelectable() and 'selected' in variables:
            # Not-selectable is a special case, AbstractSelect does not support
            # TODO could be optimized.
            variables = dict(variables)
            variables.remove('selected')
        # Collapses the nodes
        if 'collapse' in variables:
            keys = variables['collapse']
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(keys)):
                    break
                id = self.itemIdMapper.get(keys[i])
                if id is not None and self.isExpanded(id):
                    self._expanded.remove(id)
                    self.fireCollapseEvent(id)
        # Expands the nodes
        if 'expand' in variables:
            sendChildTree = False
            if 'requestChildTree' in variables:
                sendChildTree = True
            keys = variables['expand']
            _1 = True
            i = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    i += 1
                if not (i < len(keys)):
                    break
                id = self.itemIdMapper.get(keys[i])
                if id is not None:
                    self.expandItem(id, sendChildTree)
        # AbstractSelect cannot handle multiselection so we handle
        # it ourself
        if (
            'selected' in variables and self.isMultiSelect() and self._multiSelectMode == self.MultiSelectMode.DEFAULT
        ):
            self.handleSelectedItems(variables)
            variables = dict(variables)
            variables.remove('selected')
        # Selections are handled by the select component
        super(Tree, self).changeVariables(source, variables)
        # Actions
        if 'action' in variables:
            st = StringTokenizer(variables['action'], ',')
            if st.countTokens() == 2:
                itemId = self.itemIdMapper.get(st.nextToken())
                action = self._actionMapper.get(st.nextToken())
                if (
                    action is not None and (itemId is None) or self.containsId(itemId) and self._actionHandlers is not None
                ):
                    for ah in self._actionHandlers:
                        ah.handleAction(action, self, itemId)

    def handleSelectedItems(self, variables):
        """Handles the selection

        @param variables
                   The variables sent to the server from the client
        """
        ka = variables['selected']
        # Converts the key-array to id-set
        s = LinkedList()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(ka)):
                break
            id = self.itemIdMapper.get(ka[i])
            if (
                not self.isNullSelectionAllowed() and (id is None) or (id == self.getNullSelectionItemId())
            ):
                # skip empty selection if nullselection is not allowed
                self.requestRepaint()
            elif id is not None and self.containsId(id):
                s.add(id)
        if not self.isNullSelectionAllowed() and len(s) < 1:
            # empty selection not allowed, keep old value
            self.requestRepaint()
            return
        self.setValue(s, True)

    def paintContent(self, target):
        """Paints any needed component-specific things to the given UIDL stream.

        @see com.vaadin.ui.AbstractComponent#paintContent(PaintTarget)
        """
        # Container.Hierarchical API
        self._initialPaint = False
        if self._partialUpdate:
            target.addAttribute('partialUpdate', True)
            target.addAttribute('rootKey', self.itemIdMapper.key(self._expandedItemId))
        else:
            self.getCaptionChangeListener().clear()
            # The tab ordering number
            if self.getTabIndex() > 0:
                target.addAttribute('tabindex', self.getTabIndex())
            # Paint tree attributes
            if self.isSelectable():
                target.addAttribute('selectmode', 'multi' if self.isMultiSelect() else 'single')
                if self.isMultiSelect():
                    target.addAttribute('multiselectmode', self._multiSelectMode.ordinal())
            else:
                target.addAttribute('selectmode', 'none')
            if self.isNewItemsAllowed():
                target.addAttribute('allownewitem', True)
            if self.isNullSelectionAllowed():
                target.addAttribute('nullselect', True)
            if self._dragMode != self.TreeDragMode.NONE:
                target.addAttribute('dragMode', self._dragMode.ordinal())
        # Initialize variables
        actionSet = LinkedHashSet()
        # rendered selectedKeys
        selectedKeys = LinkedList()
        expandedKeys = LinkedList()
        # Iterates through hierarchical tree using a stack of iterators
        iteratorStack = Stack()
        if self._partialUpdate:
            ids = self.getChildren(self._expandedItemId)
        else:
            ids = self.rootItemIds()
        if ids is not None:
            iteratorStack.push(ids)
        # Body actions - Actions which has the target null and can be invoked
        # by right clicking on the Tree body

        if self._actionHandlers is not None:
            keys = list()
            for ah in self._actionHandlers:
                # Getting action for the null item, which in this case
                # means the body item
                aa = ah.getActions(None, self)
                if aa is not None:
                    _0 = True
                    ai = 0
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            ai += 1
                        if not (ai < len(aa)):
                            break
                        akey = self._actionMapper.key(aa[ai])
                        actionSet.add(aa[ai])
                        keys.add(akey)
            target.addAttribute('alb', list(keys))
        while not iteratorStack.isEmpty():
            # Gets the iterator for current tree level
            i = iteratorStack.peek()
            # If the level is finished, back to previous tree level
            if not i.hasNext():
                # Removes used iterator from the stack
                # Adds the item on current level
                iteratorStack.pop()
                # Closes node
                if not iteratorStack.isEmpty():
                    target.endTag('node')
            else:
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
                    selectedKeys.add(key)
                if self.areChildrenAllowed(itemId) and self.isExpanded(itemId):
                    target.addAttribute('expanded', True)
                    expandedKeys.add(key)
                # Add caption change listener
                self.getCaptionChangeListener().addNotifierForItem(itemId)
                # Actions
                if self._actionHandlers is not None:
                    keys = list()
                    ahi = self._actionHandlers
                    while ahi.hasNext():
                        aa = ahi.next().getActions(itemId, self)
                        if aa is not None:
                            _1 = True
                            ai = 0
                            while True:
                                if _1 is True:
                                    _1 = False
                                else:
                                    ai += 1
                                if not (ai < len(aa)):
                                    break
                                akey = self._actionMapper.key(aa[ai])
                                actionSet.add(aa[ai])
                                keys.add(akey)
                    target.addAttribute('al', list(keys))
                # Adds the children if expanded, or close the tag
                if (
                    self.isExpanded(itemId) and self.hasChildren(itemId) and self.areChildrenAllowed(itemId)
                ):
                    iteratorStack.push(self.getChildren(itemId))
                elif isNode:
                    target.endTag('node')
                else:
                    target.endTag('leaf')
        # Actions
        if not actionSet.isEmpty():
            target.addVariable(self, 'action', '')
            target.startTag('actions')
            i = actionSet
            while i.hasNext():
                a = i.next()
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
            target.addVariable(self, 'selected', list([None] * len(selectedKeys)))
            # Expand and collapse
            target.addVariable(self, 'expand', [])
            target.addVariable(self, 'collapse', [])
            # New items
            target.addVariable(self, 'newitem', [])
            if self._dropHandler is not None:
                self._dropHandler.getAcceptCriterion().paint(target)

    def areChildrenAllowed(self, itemId):
        """Tests if the Item with given ID can have any children.

        @see com.vaadin.data.Container.Hierarchical#areChildrenAllowed(Object)
        """
        return self.items.areChildrenAllowed(itemId)

    def getChildren(self, itemId):
        """Gets the IDs of all Items that are children of the specified Item.

        @see com.vaadin.data.Container.Hierarchical#getChildren(Object)
        """
        return self.items.getChildren(itemId)

    def getParent(self, itemId):
        """Gets the ID of the parent Item of the specified Item.

        @see com.vaadin.data.Container.Hierarchical#getParent(Object)
        """
        return self.items.getParent(itemId)

    def hasChildren(self, itemId):
        """Tests if the Item specified with <code>itemId</code> has child Items.

        @see com.vaadin.data.Container.Hierarchical#hasChildren(Object)
        """
        return self.items.hasChildren(itemId)

    def isRoot(self, itemId):
        """Tests if the Item specified with <code>itemId</code> is a root Item.

        @see com.vaadin.data.Container.Hierarchical#isRoot(Object)
        """
        return self.items.isRoot(itemId)

    def rootItemIds(self):
        """Gets the IDs of all Items in the container that don't have a parent.

        @see com.vaadin.data.Container.Hierarchical#rootItemIds()
        """
        return self.items.rootItemIds()

    def setChildrenAllowed(self, itemId, areChildrenAllowed):
        """Sets the given Item's capability to have children.

        @see com.vaadin.data.Container.Hierarchical#setChildrenAllowed(Object,
             boolean)
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container.Hierarchical#setParent(java.lang.Object ,
        # java.lang.Object)

        success = self.items.setChildrenAllowed(itemId, areChildrenAllowed)
        if success:
            self.requestRepaint()
        return success

    def setParent(self, itemId, newParentId):
        # Overriding select behavior
        success = self.items.setParent(itemId, newParentId)
        if success:
            self.requestRepaint()
        return success

    def setContainerDataSource(self, newDataSource):
        """Sets the Container that serves as the data source of the viewer.

        @see com.vaadin.data.Container.Viewer#setContainerDataSource(Container)
        """
        # Expand event and listener
        if newDataSource is None:
            # Note: using wrapped IndexedContainer to match constructor (super
            # creates an IndexedContainer, which is then wrapped).
            newDataSource = ContainerHierarchicalWrapper(IndexedContainer())
        # Assure that the data source is ordered by making unordered
        # containers ordered by wrapping them
        if Container.Hierarchical.isAssignableFrom(newDataSource.getClass()):
            super(Tree, self).setContainerDataSource(newDataSource)
        else:
            super(Tree, self).setContainerDataSource(ContainerHierarchicalWrapper(newDataSource))

    class ExpandEvent(Component.Event):
        """Event to fired when a node is expanded. ExapandEvent is fired when a node
        is to be expanded. it can me used to dynamically fill the sub-nodes of
        the node.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        _expandedItemId = None

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

    class ExpandListener(Serializable):
        """Expand event listener.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        EXPAND_METHOD = ReflectTools.findMethod(self.ExpandListener, 'nodeExpand', self.ExpandEvent)

        def nodeExpand(self, event):
            """A node has been expanded.

            @param event
                       the Expand event.
            """
            pass

    def addListener(self, *args):
        """Adds the expand listener.

        @param listener
                   the Listener to be added.
        ---
        Adds the collapse listener.

        @param listener
                   the Listener to be added.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], CollapseListener):
                listener, = _0
                self.addListener(self.CollapseEvent, listener, self.CollapseListener.COLLAPSE_METHOD)
            elif isinstance(_0[0], ExpandListener):
                listener, = _0
                self.addListener(self.ExpandEvent, listener, self.ExpandListener.EXPAND_METHOD)
            else:
                listener, = _0
                self.addListener(VTree.ITEM_CLICK_EVENT_ID, ItemClickEvent, listener, ItemClickEvent.ITEM_CLICK_METHOD)
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        """Removes the expand listener.

        @param listener
                   the Listener to be removed.
        ---
        Removes the collapse listener.

        @param listener
                   the Listener to be removed.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], CollapseListener):
                listener, = _0
                self.removeListener(self.CollapseEvent, listener, self.CollapseListener.COLLAPSE_METHOD)
            elif isinstance(_0[0], ExpandListener):
                listener, = _0
                self.removeListener(self.ExpandEvent, listener, self.ExpandListener.EXPAND_METHOD)
            else:
                listener, = _0
                self.removeListener(VTree.ITEM_CLICK_EVENT_ID, ItemClickEvent, listener)
        else:
            raise ARGERROR(1, 1)

    def fireExpandEvent(self, itemId):
        """Emits the expand event.

        @param itemId
                   the item id.
        """
        # Collapse event
        self.fireEvent(self.ExpandEvent(self, itemId))

    class CollapseEvent(Component.Event):
        """Collapse event

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        _collapsedItemId = None

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

    class CollapseListener(Serializable):
        """Collapse event listener.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        COLLAPSE_METHOD = ReflectTools.findMethod(self.CollapseListener, 'nodeCollapse', self.CollapseEvent)

        def nodeCollapse(self, event):
            """A node has been collapsed.

            @param event
                       the Collapse event.
            """
            pass

    def fireCollapseEvent(self, itemId):
        """Emits collapse event.

        @param itemId
                   the item id.
        """
        # Action container
        self.fireEvent(self.CollapseEvent(self, itemId))

    def addActionHandler(self, actionHandler):
        """Adds an action handler.

        @see com.vaadin.event.Action.Container#addActionHandler(Action.Handler)
        """
        if actionHandler is not None:
            if self._actionHandlers is None:
                self._actionHandlers = LinkedList()
                self._actionMapper = KeyMapper()
            if not self._actionHandlers.contains(actionHandler):
                self._actionHandlers.add(actionHandler)
                self.requestRepaint()

    def removeActionHandler(self, actionHandler):
        """Removes an action handler.

        @see com.vaadin.event.Action.Container#removeActionHandler(Action.Handler)
        """
        if (
            self._actionHandlers is not None and self._actionHandlers.contains(actionHandler)
        ):
            self._actionHandlers.remove(actionHandler)
            if self._actionHandlers.isEmpty():
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
        visible = LinkedList()
        # Iterates trough hierarchical tree using a stack of iterators
        iteratorStack = Stack()
        ids = self.rootItemIds()
        if ids is not None:
            iteratorStack.push(ids)
        while not iteratorStack.isEmpty():
            # Gets the iterator for current tree level
            i = iteratorStack.peek()
            # If the level is finished, back to previous tree level
            if not i.hasNext():
                # Removes used iterator from the stack
                # Adds the item on current level
                iteratorStack.pop()
            else:
                itemId = i.next()
                visible.add(itemId)
                # Adds children if expanded, or close the tag
                if self.isExpanded(itemId) and self.hasChildren(itemId):
                    iteratorStack.push(self.getChildren(itemId))
        return visible

    def setNullSelectionItemId(self, nullSelectionItemId):
        """Tree does not support <code>setNullSelectionItemId</code>.

        @see com.vaadin.ui.AbstractSelect#setNullSelectionItemId(java.lang.Object)
        """
        if nullSelectionItemId is not None:
            raise self.UnsupportedOperationException()

    def setNewItemsAllowed(self, allowNewOptions):
        """Adding new items is not supported.

        @throws UnsupportedOperationException
                    if set to true.
        @see com.vaadin.ui.Select#setNewItemsAllowed(boolean)
        """
        if allowNewOptions:
            raise self.UnsupportedOperationException()

    def setLazyLoading(self, useLazyLoading):
        """Tree does not support lazy options loading mode. Setting this true will
        throw UnsupportedOperationException.

        @see com.vaadin.ui.Select#setLazyLoading(boolean)
        """
        if useLazyLoading:
            raise self.UnsupportedOperationException('Lazy options loading is not supported by Tree.')

    _itemStyleGenerator = None
    _dropHandler = None

    def setItemStyleGenerator(self, itemStyleGenerator):
        """Sets the {@link ItemStyleGenerator} to be used with this tree.

        @param itemStyleGenerator
                   item style generator or null to remove generator
        """
        if self._itemStyleGenerator != itemStyleGenerator:
            self._itemStyleGenerator = itemStyleGenerator
            self.requestRepaint()

    def getItemStyleGenerator(self):
        """@return the current {@link ItemStyleGenerator} for this tree. Null if
                {@link ItemStyleGenerator} is not set.
        """
        return self._itemStyleGenerator

    class ItemStyleGenerator(Serializable):
        """ItemStyleGenerator can be used to add custom styles to tree items. The
        CSS class name that will be added to the cell content is
        <tt>v-tree-node-[style name]</tt>.
        """
        # Overriden so javadoc comes from Container.Hierarchical

        def getStyle(self, itemId):
            """Called by Tree when an item is painted.

            @param itemId
                       The itemId of the item to be painted
            @return The style name to add to this item. (the CSS class name will
                    be v-tree-node-[style name]
            """
            pass

    def removeItem(self, itemId):
        return super(Tree, self).removeItem(itemId)

    def getDropHandler(self):
        return self._dropHandler

    def setDropHandler(self, dropHandler):
        self._dropHandler = dropHandler

    class TreeTargetDetails(AbstractSelectTargetDetails):
        """A {@link TargetDetails} implementation with Tree specific api.

        @since 6.3
        """
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.event.dd.DropTarget#translateDropTargetDetails(java.util.Map)

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
            <p>
            In other words this method returns the identifier of the "folder"
            into the drag operation is targeted.
            <p>
            If the method returns null, the current target is on a root node or
            on other undefined area over the tree component.
            <p>
            The default Tree implementation marks the targetted tree node with
            CSS classnames v-tree-node-dragfolder and
            v-tree-node-caption-dragfolder (for the caption element).
            """
            itemIdOver = self.getItemIdOver()
            if (
                self.areChildrenAllowed(itemIdOver) and self.getDropLocation() == VerticalDropLocation.MIDDLE
            ):
                return itemIdOver
            return self.getParent(itemIdOver)

        def getItemIdAfter(self):
            """If drop is targeted into "folder node" (see {@link #getItemIdInto()}
            ), this method returns the item id of the node after the drag was
            targeted. This method is useful when implementing drop into specific
            location (between specific nodes) in tree.

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
                for object in children:
                    if object == itemIdOver:
                        return ref
                    ref = object
            return itemIdOver

    def translateDropTargetDetails(self, clientVariables):
        return self.TreeTargetDetails(clientVariables)

    def key(self, itemId):
        """Helper API for {@link TreeDropCriterion}

        @param itemId
        @return
        """
        return self.itemIdMapper.key(itemId)

    def setDragMode(self, dragMode):
        """Sets the drag mode that controls how Tree behaves as a {@link DragSource}
        .

        @param dragMode
        """
        self._dragMode = dragMode
        self.requestRepaint()

    def getDragMode(self):
        """@return the drag mode that controls how Tree behaves as a
                {@link DragSource}.

        @see TreeDragMode
        """
        return self._dragMode

    class TreeTransferable(DataBoundTransferable):
        """Concrete implementation of {@link DataBoundTransferable} for data
        transferred from a tree.

        @see {@link DataBoundTransferable}.

        @since 6.3
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.event.dd.DragSource#getTransferable(java.util.Map)

        def __init__(self, sourceComponent, rawVariables):
            super(TreeTransferable, self)(sourceComponent, rawVariables)

        def getItemId(self):
            return self.getData('itemId')

        def getPropertyId(self):
            return self.getItemCaptionPropertyId()

    def getTransferable(self, payload):
        transferable = self.TreeTransferable(self, payload)
        # updating drag source variables
        object = payload['itemId']
        if object is not None:
            transferable.setData('itemId', self.itemIdMapper.get(object))
        return transferable

    class TreeDropCriterion(ServerSideCriterion):
        """Lazy loading accept criterion for Tree. Accepted target nodes are loaded
        from server once per drag and drop operation. Developer must override one
        method that decides accepted tree nodes for the whole Tree.

        <p>
        Initially pretty much no data is sent to client. On first required
        criterion check (per drag request) the client side data structure is
        initialized from server and no subsequent requests requests are needed
        during that drag and drop operation.
        """
        _tree = None
        _allowedItemIds = None
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.event.dd.acceptCriteria.ServerSideCriterion#getIdentifier
        # ()

        def getIdentifier(self):
            # (non-Javadoc)
            # 
            # @see
            # com.vaadin.event.dd.acceptCriteria.AcceptCriterion#accepts(com.vaadin
            # .event.dd.DragAndDropEvent)

            return self.TreeDropCriterion.getCanonicalName()

        def accept(self, dragEvent):
            # (non-Javadoc)
            # 
            # @see
            # com.vaadin.event.dd.acceptCriteria.AcceptCriterion#paintResponse(
            # com.vaadin.terminal.PaintTarget)

            dropTargetData = dragEvent.getTargetDetails()
            self._tree = dragEvent.getTargetDetails().getTarget()
            self._allowedItemIds = self.getAllowedItemIds(dragEvent, self._tree)
            return dropTargetData.getItemIdOver() in self._allowedItemIds

        def paintResponse(self, target):
            # send allowed nodes to client so subsequent requests can be
            # avoided

            array = list(self._allowedItemIds)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(array)):
                    break
                key = self._tree.key(array[i])
                array[i] = key
            target.addAttribute('allowedIds', array)

        def getAllowedItemIds(self, dragEvent, tree):
            pass

    class TargetItemAllowsChildren(TargetDetailIs):
        """A criterion that accepts {@link Transferable} only directly on a tree
        node that can have children.
        <p>
        Class is singleton, use {@link TargetItemAllowsChildren#get()} to get the
        instance.

        @see Tree#setChildrenAllowed(Object, boolean)

        @since 6.3
        """
        _instance = self.TargetItemAllowsChildren()

        @classmethod
        def get(cls):
            return cls._instance

        def __init__(self):
            # Uses enhanced server side check
            super(TargetItemAllowsChildren, self)('itemIdOverIsNode', Boolean.TRUE.TRUE)

        def accept(self, dragEvent):
            # must be over tree node and in the middle of it (not top or
            # bottom
            # part)
            try:
                eventDetails = dragEvent.getTargetDetails()
                itemIdOver = eventDetails.getItemIdOver()
                if not eventDetails.getTarget().areChildrenAllowed(itemIdOver):
                    return False
                # return true if directly over
                return eventDetails.getDropLocation() == VerticalDropLocation.MIDDLE
            except Exception, e:
                return False

    class TargetInSubtree(ClientSideCriterion):
        """An accept criterion that checks the parent node (or parent hierarchy) for
        the item identifier given in constructor. If the parent is found, content
        is accepted. Criterion can be used to accepts drags on a specific sub
        tree only.
        <p>
        The root items is also consider to be valid target.
        """
        _rootId = None
        _depthToCheck = -1

        def __init__(self, *args):
            """Constructs a criteria that accepts the drag if the targeted Item is a
            descendant of Item identified by given id

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
            _0 = args
            _1 = len(args)
            if _1 == 1:
                parentItemId, = _0
                self._rootId = parentItemId
            elif _1 == 2:
                rootId, depthToCheck = _0
                self._rootId = rootId
                self._depthToCheck = depthToCheck
            else:
                raise ARGERROR(1, 2)

        def accept(self, dragEvent):
            try:
                eventDetails = dragEvent.getTargetDetails()
                if eventDetails.getItemIdOver() is not None:
                    itemId = eventDetails.getItemIdOver()
                    i = 0
                    while (
                        itemId is not None and (self._depthToCheck == -1) or (i <= self._depthToCheck)
                    ):
                        if itemId == self._rootId:
                            return True
                        itemId = self.getParent(itemId)
                        i += 1
                return False
            except Exception, e:
                return False

        def paintContent(self, target):
            super(TargetInSubtree, self).paintContent(target)
            target.addAttribute('depth', self._depthToCheck)
            target.addAttribute('key', self.key(self._rootId))
