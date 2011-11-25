# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.user.client.ui.KeyboardListener import (KeyboardListener,)
# from com.google.gwt.user.client.ui.KeyboardListenerCollection import (KeyboardListenerCollection,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Iterator import (Iterator,)


class ShortcutActionHandler(object):
    """A helper class to implement keyboard shorcut handling. Keeps a list of owners
    actions and fires actions to server. User class needs to delegate keyboard
    events to handleKeyboardEvents function.

    @author IT Mill ltd
    """

    class ShortcutActionHandlerOwner(HasWidgets):
        """An interface implemented by those users (most often {@link Container}s,
        but HasWidgets at least) of this helper class that want to support
        special components like {@link VRichTextArea} that don't properly
        propagate key down events. Those components can build support for
        shortcut actions by traversing the closest
        {@link ShortcutActionHandlerOwner} from the component hierarchy an
        passing keydown events to {@link ShortcutActionHandler}.
        """

        def getShortcutActionHandler(self):
            """Returns the ShortCutActionHandler currently used or null if there is
            currently no shortcutactionhandler
            """
            pass

    class BeforeShortcutActionListener(Paintable):
        """A focusable {@link Paintable} implementing this interface will be
        notified before shortcut actions are handled if it will be the target of
        the action (most commonly means it is the focused component during the
        keyboard combination is triggered by the user).
        """

        def onBeforeShortcutAction(self, e):
            """This method is called by ShortcutActionHandler before firing the
            shortcut if the Paintable is currently focused (aka the target of the
            shortcut action). Eg. a field can update its possibly changed value
            to the server before shortcut action is fired.

            @param e
                       the event that triggered the shortcut action
            """
            pass

    _actions = list()
    _client = None
    _paintableId = None

    def __init__(self, pid, c):
        """@param pid
                   Paintable id
        @param c
                   reference to application connections
        """
        self._paintableId = pid
        self._client = c

    def updateActionMap(self, c):
        """Updates list of actions this handler listens to.

        @param c
                   UIDL snippet containing actions
        """
        self._actions.clear()
        it = c.getChildIterator()
        while it.hasNext():
            action = it.next()
            modifiers = None
            if action.hasAttribute('mk'):
                modifiers = action.getIntArrayAttribute('mk')
            kc = self.ShortcutKeyCombination(action.getIntAttribute('kc'), modifiers)
            key = action.getStringAttribute('key')
            caption = action.getStringAttribute('caption')
            self._actions.add(self.ShortcutAction(key, kc, caption))

    def handleKeyboardEvent(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            event, = _0
            self.handleKeyboardEvent(event, None)
        elif _1 == 2:
            event, target = _0
            modifiers = KeyboardListenerCollection.getKeyboardModifiers(event)
            keyCode = DOM.eventGetKeyCode(event)
            kc = self.ShortcutKeyCombination(keyCode, modifiers)
            it = self._actions
            while it.hasNext():
                a = it.next()
                if a.getShortcutCombination() == kc:
                    self.fireAction(event, a, target)
                    break
        else:
            raise ARGERROR(1, 2)

    def fireAction(self, event, a, target):
        et = DOM.eventGetTarget(event)
        if target is None:
            w = Util.findWidget(et, None)
            while w is not None and not isinstance(w, Paintable):
                w = w.getParent()
            target = w
        finalTarget = target
        event.preventDefault()
        # The target component might have unpublished changes, try to
        # synchronize them before firing shortcut action.

        if isinstance(finalTarget, self.BeforeShortcutActionListener):
            finalTarget.onBeforeShortcutAction(event)
        else:
            self.shakeTarget(et)

            class _0_(Command):

                def execute(self):
                    ShortcutActionHandler_this.shakeTarget(self.et)

            _0_ = _0_()
            Scheduler.get().scheduleDeferred(_0_)

        class _1_(Command):

            def execute(self):
                if self.finalTarget is not None:
                    ShortcutActionHandler_this._client.updateVariable(ShortcutActionHandler_this._paintableId, 'actiontarget', self.finalTarget, False)
                ShortcutActionHandler_this._client.updateVariable(ShortcutActionHandler_this._paintableId, 'action', self.a.getKey(), True)

        _1_ = _1_()
        Scheduler.get().scheduleDeferred(_1_)

    @classmethod
    def shakeTarget(cls, e):
        """We try to fire value change in the component the key combination was
        typed. Eg. textfield may contain newly typed text that is expected to be
        sent to server. This is done by removing focus and then returning it
        immediately back to target element.
        <p>
        This is practically a hack and should be replaced with an interface
        {@link BeforeShortcutActionListener} via widgets could be notified when
        they should fire value change. Big task for TextFields, DateFields and
        various selects.

        <p>
        TODO separate opera impl with generator
        """
        cls.blur(e)
        if BrowserInfo.get().isOpera():
            # will mess up with focus and blur event if the focus is not
            # deferred. Will cause a small flickering, so not doing it for all
            # browsers.

            class _2_(Command):

                def execute(self):
                    ShortcutActionHandler_this.focus(self.e)

            _2_ = _2_()
            Scheduler.get().scheduleDeferred(_2_)
        else:
            cls.focus(e)

    @classmethod
    def blur(cls, e):
        JS("""
        if(@{{e}}.blur) {
            @{{e}}.blur();
       }
    """)
        pass

    @classmethod
    def focus(cls, e):
        JS("""
        if(@{{e}}.blur) {
            @{{e}}.focus();
       }
    """)
        pass


class ShortcutKeyCombination(object):
    SHIFT = 16
    CTRL = 17
    ALT = 18
    META = 91
    _keyCode = 0
    _modifiersMask = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 2:
            if isinstance(_0[0], char):
                kc, modifierMask = _0
                self._keyCode = kc
                self._modifiersMask = modifierMask
            else:
                kc, modifiers = _0
                self._keyCode = kc
                self._modifiersMask = 0
                if modifiers is not None:
                    _0 = True
                    i = 0
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            i += 1
                        if not (i < modifiers.length):
                            break
                        _1 = modifiers[i]
                        _2 = False
                        while True:
                            if _1 == self.ALT:
                                _2 = True
                                self._modifiersMask = self._modifiersMask | KeyboardListener.MODIFIER_ALT
                                break
                            if (_2 is True) or (_1 == self.CTRL):
                                _2 = True
                                self._modifiersMask = self._modifiersMask | KeyboardListener.MODIFIER_CTRL
                                break
                            if (_2 is True) or (_1 == self.SHIFT):
                                _2 = True
                                self._modifiersMask = self._modifiersMask | KeyboardListener.MODIFIER_SHIFT
                                break
                            if (_2 is True) or (_1 == self.META):
                                _2 = True
                                self._modifiersMask = self._modifiersMask | KeyboardListener.MODIFIER_META
                                break
                            if True:
                                _2 = True
                                break
                            break
        else:
            raise ARGERROR(0, 2)

    def equals(self, other):
        if (
            self._keyCode == other.keyCode and self._modifiersMask == other.modifiersMask
        ):
            return True
        return False


class ShortcutAction(object):
    _sc = None
    _caption = None
    _key = None

    def __init__(self, key, sc, caption):
        self._sc = sc
        self._key = key
        self._caption = caption

    def getShortcutCombination(self):
        return self._sc

    def getCaption(self):
        return self._caption

    def getKey(self):
        return self._key
