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

import re

from muntjac.event.Action import Action


class ShortcutAction(Action):
    """Shortcuts are a special type of {@link Action}s used to create keyboard
    shortcuts.
    <p>
    The ShortcutAction is triggered when the user presses a given key in
    combination with the (optional) given modifier keys.
    </p>
    <p>
    ShortcutActions can be global (by attaching to the {@link Window}), or
    attached to different parts of the UI so that a specific shortcut is only
    valid in part of the UI. For instance, one can attach shortcuts to a specific
    {@link Panel} - look for {@link ComponentContainer}s implementing
    {@link Handler Action.Handler} or {@link Notifier Action.Notifier}.
    </p>
    <p>
    ShortcutActions have a caption that may be used to display the shortcut
    visually. This allows the ShortcutAction to be used as a plain Action while
    still reacting to a keyboard shortcut. Note that this functionality is not
    very well supported yet, but it might still be a good idea to give a caption
    to the shortcut.
    </p>

    @author IT Mill Ltd.
    @version
    @since 4.0.1
    """

    # Used in the caption shorthand notation to indicate the ALT modifier.
    SHORTHAND_CHAR_ALT = '&'

    # Used in the caption shorthand notation to indicate the SHIFT modifier.
    SHORTHAND_CHAR_SHIFT = '_'

    # Used in the caption shorthand notation to indicate the CTRL modifier.
    SHORTHAND_CHAR_CTRL = '^'

    # regex-quote (escape) the characters
    _SHORTHAND_ALT = re.escape(SHORTHAND_CHAR_ALT)
    _SHORTHAND_SHIFT = re.escape(SHORTHAND_CHAR_SHIFT)
    _SHORTHAND_CTRL = re.escape(SHORTHAND_CHAR_CTRL)

    # Used for replacing escaped chars, e.g && with &
    _SHORTHAND_ESCAPE = re.compile('(' + _SHORTHAND_ALT + '?)' \
            + _SHORTHAND_ALT + '|(' + _SHORTHAND_SHIFT + '?)' \
            + _SHORTHAND_SHIFT + '|(' + _SHORTHAND_CTRL + '?)' \
            + _SHORTHAND_CTRL)

    # Used for removing escaped chars, only leaving real shorthands
    _SHORTHAND_REMOVE = re.compile('([' + _SHORTHAND_ALT + '|' \
            + _SHORTHAND_SHIFT + '|' + _SHORTHAND_CTRL + '])\\1')

    # Mnemonic char, optionally followed by another, and optionally a third
    _SHORTHANDS = re.compile('(' + _SHORTHAND_ALT + '|' + _SHORTHAND_SHIFT \
            + '|' + _SHORTHAND_CTRL + ')(?!\\1)(?:(' + _SHORTHAND_ALT \
            + '|' + _SHORTHAND_SHIFT + '|' + _SHORTHAND_CTRL \
            + ')(?!\\1|\\2))?(?:(' + _SHORTHAND_ALT + '|' + _SHORTHAND_SHIFT \
            + '|' + _SHORTHAND_CTRL + ')(?!\\1|\\2|\\3))?.')


    def __init__(self, *args):
        """Creates a shortcut that reacts to the given {@link KeyCode} and
        (optionally) {@link ModifierKey}s. <br/>
        The shortcut might be shown in the UI (e.g context menu), in which case
        the caption will be used.

        @param caption
                   used when displaying the shortcut visually
        @param kc
                   KeyCode that the shortcut reacts to
        @param m
                   optional modifier keys
        ---
        Creates a shortcut that reacts to the given {@link KeyCode} and
        (optionally) {@link ModifierKey}s. <br/>
        The shortcut might be shown in the UI (e.g context menu), in which case
        the caption and icon will be used.

        @param caption
                   used when displaying the shortcut visually
        @param icon
                   used when displaying the shortcut visually
        @param kc
                   KeyCode that the shortcut reacts to
        @param m
                   optional modifier keys
        ---
        Constructs a ShortcutAction using a shorthand notation to encode the
        keycode and modifiers in the caption.
        <p>
        Insert one or more modifier characters before the character to use as
        keycode. E.g <code>"&Save"</code> will make a shortcut responding to
        ALT-S, <code>"E^xit"</code> will respond to CTRL-X.<br/>
        Multiple modifiers can be used, e.g <code>"&^Delete"</code> will respond
        to CTRL-ALT-D (the order of the modifier characters is not important).
        </p>
        <p>
        The modifier characters will be removed from the caption. The modifier
        character is be escaped by itself: two consecutive characters are turned
        into the original character w/o the special meaning. E.g
        <code>"Save&&&close"</code> will respond to ALT-C, and the caption will
        say "Save&close".
        </p>

        @param shorthandCaption
                   the caption in modifier shorthand
        ---
        Constructs a ShortcutAction using a shorthand notation to encode the
        keycode a in the caption.
        <p>
        This works the same way as {@link #ShortcutAction(String)}, with the
        exception that the modifiers given override those indicated in the
        caption. I.e use any of the modifier characters in the caption to
        indicate the keycode, but the modifier will be the given set.<br/>
        E.g
        <code>new ShortcutAction("Do &stuff", new int[]{ShortcutAction.ModifierKey.CTRL}));</code>
        will respond to CTRL-S.
        </p>

        @param shorthandCaption
        @param modifierKeys
        """
        self._keyCode = None
        self._modifiers = None

        args = args
        nargs = len(args)
        if nargs == 1:
            shorthandCaption, = args
            self.__init__(shorthandCaption, None)
        elif nargs == 2:
            shorthandCaption, modifierKeys = args

            # && -> & etc
            super(ShortcutAction, self)(self._SHORTHAND_ESCAPE.sub(shorthandCaption, '$1$2$3'))

            # replace escaped chars with something that won't accidentally match
            shorthandCaption = self._SHORTHAND_REMOVE.sub(shorthandCaption, '\u001A')

            m = self._SHORTHANDS.search(shorthandCaption)  # FIXME: check regex
            if m is not None:
                match = m.group()

                # KeyCode from last char in match, uppercase
                self._keyCode = m.group()[len(match) - 1].upper()

                # Given modifiers override this indicated in the caption
                if modifierKeys is not None:
                    self._modifiers = modifierKeys
                else:
                    # Read modifiers from caption
                    mod = [None] * (len(match) - 1)
                    for i in range(len(mod)):
                        kc = match[i]

                        if kc == self.SHORTHAND_CHAR_ALT:
                            mod[i] = self.ModifierKey.ALT

                        elif kc == self.SHORTHAND_CHAR_CTRL:
                            mod[i] = self.ModifierKey.CTRL

                        elif kc == self.SHORTHAND_CHAR_SHIFT:
                            mod[i] = self.ModifierKey.SHIFT

                    self._modifiers = mod
            else:
                self._keyCode = -1
                self._modifiers = modifierKeys
        elif nargs == 3:
            caption, kc, m = args
            super(ShortcutAction, self)(caption)
            self._keyCode = kc
            self._modifiers = m
        elif nargs == 4:
            caption, icon, kc, m = args
            super(ShortcutAction, self)(caption, icon)
            self._keyCode = kc
            self._modifiers = m
        else:
            raise ValueError, 'invalid number of arguments'


    def getKeyCode(self):
        """Get the {@link KeyCode} that this shortcut reacts to (in combination with
        the {@link ModifierKey}s).

        @return keycode for this shortcut
        """
        return self._keyCode


    def getModifiers(self):
        """Get the {@link ModifierKey}s required for the shortcut to react.

        @return modifier keys for this shortcut
        """
        return self._modifiers


class KeyCode(object):
    """Key codes that can be used for shortcuts"""

    ENTER = 13
    ESCAPE = 27
    PAGE_UP = 33
    PAGE_DOWN = 34
    TAB = 9
    ARROW_LEFT = 37
    ARROW_UP = 38
    ARROW_RIGHT = 39
    ARROW_DOWN = 40
    BACKSPACE = 8
    DELETE = 46
    INSERT = 45
    END = 35
    HOME = 36
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    A = 65
    B = 66
    C = 67
    D = 68
    E = 69
    F = 70
    G = 71
    H = 72
    I = 73
    J = 74
    K = 75
    L = 76
    M = 77
    N = 78
    O = 79
    P = 80
    Q = 81
    R = 82
    S = 83
    T = 84
    U = 85
    V = 86
    W = 87
    X = 88
    Y = 89
    Z = 90
    NUM0 = 48
    NUM1 = 49
    NUM2 = 50
    NUM3 = 51
    NUM4 = 52
    NUM5 = 53
    NUM6 = 54
    NUM7 = 55
    NUM8 = 56
    NUM9 = 57
    SPACEBAR = 32


class ModifierKey(object):
    """Modifier key constants"""

    SHIFT = 16
    CTRL = 17
    ALT = 18
    META = 91
