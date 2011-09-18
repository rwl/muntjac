# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
from com.vaadin.event.Action import (Action, Container, Handler, Notifier,)
# from com.vaadin.event.Action.Container import (Container,)
# from com.vaadin.event.Action.Handler import (Handler,)
# from java.util.HashSet import (HashSet,)
# from java.util.Map import (Map,)


class ActionManager(Action, Container, Action, Handler, Action, Notifier):
    """Javadoc TODO

    Notes:
    <p>
    Empties the keymapper for each repaint to avoid leaks; can cause problems in
    the future if the client assumes key don't change. (if lazyloading, one must
    not cache results)
    </p>
    """
    _serialVersionUID = 1641868163608066491L
    # List of action handlers
    ownActions = None
    # List of action handlers
    actionHandlers = None
    # Action mapper
    actionMapper = None
    viewer = None
    _clientHasActions = False

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 1:
            viewer, = _0
            self.viewer = viewer
        else:
            raise ARGERROR(0, 1)

    def requestRepaint(self):
        if self.viewer is not None:
            self.viewer.requestRepaint()

    def setViewer(self, viewer):
        if viewer == self.viewer:
            return
        if self.viewer is not None:
            self.viewer.removeActionHandler(self)
        self.requestRepaint()
        # this goes to the old viewer
        if viewer is not None:
            viewer.addActionHandler(self)
        self.viewer = viewer
        self.requestRepaint()
        # this goes to the new viewer

    def addAction(self, action):
        if self.ownActions is None:
            self.ownActions = set()
        if self.ownActions.add(action):
            self.requestRepaint()

    def removeAction(self, action):
        if self.ownActions is not None:
            if self.ownActions.remove(action):
                self.requestRepaint()

    def addActionHandler(self, actionHandler):
        if actionHandler == self:
            # don't add the actionHandler to itself
            return
        if actionHandler is not None:
            if self.actionHandlers is None:
                self.actionHandlers = set()
            if self.actionHandlers.add(actionHandler):
                self.requestRepaint()

    def removeActionHandler(self, actionHandler):
        if self.actionHandlers is not None and actionHandler in self.actionHandlers:
            if self.actionHandlers.remove(actionHandler):
                self.requestRepaint()
            if self.actionHandlers.isEmpty():
                self.actionHandlers = None

    def removeAllActionHandlers(self):
        if self.actionHandlers is not None:
            self.actionHandlers = None
            self.requestRepaint()



#    public void paintActions(Object actionTarget, PaintTarget paintTarget)
#            throws PaintException {
#
#        actionMapper = null;
#
#        HashSet<Action> actions = new HashSet<Action>();
#        if (actionHandlers != null) {
#            for (Action.Handler handler : actionHandlers) {
#                Action[] as = handler.getActions(actionTarget, viewer);
#                if (as != null) {
#                    for (Action action : as) {
#                        actions.add(action);
#                    }
#                }
#            }
#        }
#        if (ownActions != null) {
#            actions.addAll(ownActions);
#        }
#
#        /*
#         * Must repaint whenever there are actions OR if all actions have been
#         * removed but still exist on client side
#         */
#        if (!actions.isEmpty() || clientHasActions) {
#            actionMapper = new KeyMapper();
#
#            paintTarget.addVariable(viewer, "action", "");
#            paintTarget.startTag("actions");
#
#            for (final Action a : actions) {
#                paintTarget.startTag("action");
#                final String akey = actionMapper.key(a);
#                paintTarget.addAttribute("key", akey);
#                if (a.getCaption() != null) {
#                    paintTarget.addAttribute("caption", a.getCaption());
#                }
#                if (a.getIcon() != null) {
#                    paintTarget.addAttribute("icon", a.getIcon());
#                }
#                if (a instanceof ShortcutAction) {
#                    final ShortcutAction sa = (ShortcutAction) a;
#                    paintTarget.addAttribute("kc", sa.getKeyCode());
#                    final int[] modifiers = sa.getModifiers();
#                    if (modifiers != null) {
#                        final String[] smodifiers = new String[modifiers.length];
#                        for (int i = 0; i < modifiers.length; i++) {
#                            smodifiers[i] = String.valueOf(modifiers[i]);
#                        }
#                        paintTarget.addAttribute("mk", smodifiers);
#                    }
#                }
#                paintTarget.endTag("action");
#            }
#
#            paintTarget.endTag("actions");
#        }
#
#        /*
#         * Update flag for next repaint so we know if we need to paint empty
#         * actions or not (must send actions is client had actions before and
#         * all actions were removed).
#         */
#        clientHasActions = !actions.isEmpty();
#    }

    def handleActions(self, variables, sender):
        if 'action' in variables and self.actionMapper is not None:
            key = variables['action']
            action = self.actionMapper.get(key)
            target = variables['actiontarget']
            if action is not None:
                self.handleAction(action, sender, target)

    def getActions(self, target, sender):
        actions = set()
        if self.ownActions is not None:
            for a in self.ownActions:
                actions.add(a)
        if self.actionHandlers is not None:
            for h in self.actionHandlers:
                as_ = h.getActions(target, sender)
                if as_ is not None:
                    for a in as_:
                        actions.add(a)
        return list([None] * len(actions))

    def handleAction(self, action, sender, target):
        if self.actionHandlers is not None:
            array = list([None] * len(self.actionHandlers))
            for handler in array:
                handler.handleAction(action, sender, target)
        if (
            self.ownActions is not None and action in self.ownActions and isinstance(action, Action.Listener)
        ):
            action.handleAction(sender, target)
