# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from __pyjamas__ import JS

from pyjamas import DOM

from muntjac.terminal.gwt.client.paintable import IPaintable
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.browser_info import BrowserInfo


class ShortcutActionHandler(object):
    """A helper class to implement keyboard shorcut handling. Keeps a list of
    owners actions and fires actions to server. User class needs to delegate
    keyboard events to handleKeyboardEvents function.

    @author: Vaadin Ltd
    @author: Richard Lincoln
    """

    def __init__(self, pid, c):
        """@param pid:
                   Paintable id
        @param c:
                   reference to application connections
        """
        self._actions = list()
        self._paintableId = pid
        self._client = c


    def updateActionMap(self, c):
        """Updates list of actions this handler listens to.

        @param c:
                   UIDL snippet containing actions
        """
        self._actions.clear()
        it = c.getChildIterator()
        while it.hasNext():
            action = it.next()
            modifiers = None
            if action.hasAttribute('mk'):
                modifiers = action.getIntArrayAttribute('mk')
            kc = ShortcutKeyCombination(action.getIntAttribute('kc'),
                    modifiers)
            key = action.getStringAttribute('key')
            caption = action.getStringAttribute('caption')
            self._actions.add(ShortcutAction(key, kc, caption))


    def handleKeyboardEvent(self, event, target=None):
        modifiers = KeyboardListenerCollection.getKeyboardModifiers(event)
        keyCode = DOM.eventGetKeyCode(event)
        kc = ShortcutKeyCombination(keyCode, modifiers)
        it = self._actions
        while it.hasNext():
            a = it.next()
            if a.getShortcutCombination() == kc:
                self.fireAction(event, a, target)
                break


    def fireAction(self, event, a, target):
        et = DOM.eventGetTarget(event)
        if target is None:
            w = Util.findWidget(et, None)
            while (w is not None) and not isinstance(w, IPaintable):
                w = w.getParent()
            target = w

        finalTarget = target

        event.preventDefault()

        # The target component might have unpublished changes, try to
        # synchronize them before firing shortcut action.
        if isinstance(finalTarget, IBeforeShortcutActionListener):
            finalTarget.onBeforeShortcutAction(event)
        else:
            self.shakeTarget(et)

            class Command1(Command):

                def __init__(self, handler):
                    self._handler = handler

                def execute(self):
                    self._handler.shakeTarget(self.et)

            Scheduler.get().scheduleDeferred(Command1(self))

        class Command2(Command):

            def __init__(self, handler):
                self._handler = handler

            def execute(self):
                if self.finalTarget is not None:
                    self._handler._client.updateVariable(
                            self._handler._paintableId, 'actiontarget',
                            self.finalTarget, False)
                self._handler._client.updateVariable(self._handler._paintableId,
                        'action', self.a.getKey(), True)

        Scheduler.get().scheduleDeferred(Command2(self))


    @classmethod
    def shakeTarget(cls, e):
        """We try to fire value change in the component the key combination was
        typed. Eg. textfield may contain newly typed text that is expected to
        be sent to server. This is done by removing focus and then returning it
        immediately back to target element.

        This is practically a hack and should be replaced with an interface
        L{IBeforeShortcutActionListener} via widgets could be notified when
        they should fire value change. Big task for TextFields, DateFields and
        various selects.

        TODO: separate opera impl with generator
        """
        cls.blur(e)
        if BrowserInfo.get().isOpera():
            # will mess up with focus and blur event if the focus is not
            # deferred. Will cause a small flickering, so not doing it for
            # all browsers.

            class Command1(Command):

                def __init__(self, handler):
                    self._handler = handler

                def execute(self):
                    self._handler.focus(self.e)

            Scheduler.get().scheduleDeferred(Command1(self))
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

    def __init__(self, kc=None, mod=None):
        self._keyCode = 0
        self._modifiersMask = None

        if kc is not None and mod is not None:
            if isinstance(kc, basestring):
                self._keyCode = kc
                self._modifiersMask = mod
            else:
                modifiers = mod
                self._keyCode = kc
                self._modifiersMask = 0
                if modifiers is not None:
                    for m in modifiers:
                        if m == self.ALT:
                            self._modifiersMask = (self._modifiersMask
                                    | KeyboardListener.MODIFIER_ALT)
                        elif m == self.CTRL:
                            self._modifiersMask = (self._modifiersMask
                                    | KeyboardListener.MODIFIER_CTRL)
                        elif m == self.SHIFT:
                            self._modifiersMask = (self._modifiersMask
                                    | KeyboardListener.MODIFIER_SHIFT)
                        elif m == self.META:
                            self._modifiersMask = (self._modifiersMask
                                    | KeyboardListener.MODIFIER_META)


    def equals(self, other):
        if (self._keyCode == other.keyCode
                and self._modifiersMask == other.modifiersMask):
            return True
        return False


class ShortcutAction(object):

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


class IShortcutActionHandlerOwner(HasWidgets):
    """An interface implemented by those users (most often Containers,
    but HasWidgets at least) of this helper class that want to support
    special components like L{VRichTextArea} that don't properly
    propagate key down events. Those components can build support for
    shortcut actions by traversing the closest
    L{ShortcutActionHandlerOwner} from the component hierarchy an
    passing keydown events to L{ShortcutActionHandler}.
    """

    def getShortcutActionHandler(self):
        """Returns the ShortCutActionHandler currently used or null if there
        is currently no shortcutactionhandler
        """
        raise NotImplementedError


class IBeforeShortcutActionListener(IPaintable):
    """A focusable L{IPaintable} implementing this interface will be
    notified before shortcut actions are handled if it will be the target of
    the action (most commonly means it is the focused component during the
    keyboard combination is triggered by the user).
    """

    def onBeforeShortcutAction(self, e):
        """This method is called by ShortcutActionHandler before firing the
        shortcut if the Paintable is currently focused (aka the target of the
        shortcut action). Eg. a field can update its possibly changed value
        to the server before shortcut action is fired.

        @param e:
                   the event that triggered the shortcut action
        """
        raise NotImplementedError
