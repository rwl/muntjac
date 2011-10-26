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

from warnings import warn

from muntjac.ui.abstract_text_field import AbstractTextField
from muntjac.data.property import IProperty


class TextField(AbstractTextField):
    """A text editor component that can be bound to any bindable IProperty.
    The text editor supports both multiline and single line modes, default
    is one-line mode.

    Since <code>TextField</code> extends <code>AbstractField</code> it
    implements the {@link com.vaadin.data.Buffered} interface. A
    <code>TextField</code> is in write-through mode by default, so
    {@link com.vaadin.ui.AbstractField#setWriteThrough(boolean)} must be
    called to enable buffering.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    CLIENT_WIDGET = None #ClientWidget(VTextField, LoadStyle.EAGER)

    def __init__(self, *args):
        """Constructs an empty <code>TextField</code> with no caption.
        ---
        Constructs an empty <code>TextField</code> with given caption.

        @param caption
                   the caption <code>String</code> for the editor.
        ---
        Constructs a new <code>TextField</code> that's bound to the specified
        <code>IProperty</code> and has no caption.

        @param dataSource
                   the IProperty to be edited with this editor.
        ---
        Constructs a new <code>TextField</code> that's bound to the specified
        <code>IProperty</code> and has the given caption <code>String</code>.

        @param caption
                   the caption <code>String</code> for the editor.
        @param dataSource
                   the IProperty to be edited with this editor.
        ---
        Constructs a new <code>TextField</code> with the given caption and
        initial text contents. The editor constructed this way will not be
        bound to a IProperty unless
        {@link IProperty.Viewer#setPropertyDataSource(IProperty)} is called to
        bind it.

        @param caption
                   the caption <code>String</code> for the editor.
        @param text
                   the initial text content of the editor.
        """
        # Tells if input is used to enter sensitive information that is not
        # echoed to display. Typically passwords.
        self._secret = False

        # Number of visible rows in a multiline TextField. Value 0 implies a
        # single-line text-editor.
        self._rows = 0

        # Tells if word-wrapping should be used in multiline mode.
        self._wordwrap = True

        nargs = len(args)
        if nargs == 0:
            super(TextField, self).__init__()
            self.setValue('')
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                super(TextField, self).__init__()
                dataSource, = args
                self.setPropertyDataSource(dataSource)
            else:
                caption, = args
                TextField.__init__(self)
                self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], IProperty):
                caption, dataSource = args
                TextField.__init__(self, dataSource)
                self.setCaption(caption)
            else:
                super(TextField, self).__init__()
                caption, value = args
                self.setValue(value)
                self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'


    def isSecret(self):
        """Gets the secret property. If a field is used to enter secret
        information the information is not echoed to display.

        @return <code>true</code> if the field is used to enter secret
                information, <code>false</code> otherwise.

        @deprecated Starting from 6.5 use {@link PasswordField} instead for
                    secret text input.
        """
        warn('use PasswordField instead', DeprecationWarning)

        return self._secret


    def setSecret(self, secret):
        """Sets the secret property on and off. If a field is used to enter
        secret information the information is not echoed to display.

        @param secret
                   the value specifying if the field is used to enter secret
                   information.
        @deprecated Starting from 6.5 use {@link PasswordField} instead for
                    secret text input.
        """
        warn('use PasswordField instead', DeprecationWarning)

        if self._secret != secret:
            self._secret = secret
            self.requestRepaint()


    def paintContent(self, target):
        if self.isSecret():
            target.addAttribute('secret', True)

        rows = self.getRows()
        if rows != 0:
            target.addAttribute('rows', rows)
            target.addAttribute('multiline', True)

            if not self.isWordwrap():
                # Wordwrap is only painted if turned off to minimize
                # communications
                target.addAttribute('wordwrap', False)

        super(TextField, self).paintContent(target)


    def getRows(self):
        """Gets the number of rows in the editor. If the number of rows is set
        to 0, the actual number of displayed rows is determined implicitly by
        the adapter.

        @return number of explicitly set rows.
        @deprecated Starting from 6.5 use {@link TextArea} for a multi-line
                    text input.
        """
        warn('use TextArea for a multi-line text input', DeprecationWarning)

        return self._rows


    def setRows(self, rows):
        """Sets the number of rows in the editor.

        @param rows
                   the number of rows for this editor.

        @deprecated Starting from 6.5 use {@link TextArea} for a multi-line
                    text input.
        """
        warn('use TextArea for a multi-line text input', DeprecationWarning)

        if rows < 0:
            rows = 0

        if self._rows != rows:
            self._rows = rows
            self.requestRepaint()


    def isWordwrap(self):
        """Tests if the editor is in word-wrap mode.

        @return <code>true</code> if the component is in the word-wrap mode,
                <code>false</code> if not.
        @deprecated Starting from 6.5 use {@link TextArea} for a multi-line
                    text input.
        """
        warn('use TextArea for a multi-line text input', DeprecationWarning)
        return self._wordwrap


    def setWordwrap(self, wordwrap):
        """Sets the editor's word-wrap mode on or off.

        @param wordwrap
                   the boolean value specifying if the editor should be in
                   word-wrap mode after the call or not.

        @deprecated Starting from 6.5 use {@link TextArea} for a multi-line
                    text input.
        """
        warn('use TextArea for a multi-line text input', DeprecationWarning)
        if self._wordwrap != wordwrap:
            self._wordwrap = wordwrap
            self.requestRepaint()


    def setHeight(self, height, unit=None):
        """Sets the height of the {@link TextField} instance.

        Setting height for {@link TextField} also has a side-effect that puts
        {@link TextField} into multiline mode (aka "textarea"). Multiline mode
        can also be achieved by calling {@link #setRows(int)}. The height
        value overrides the number of rows set by {@link #setRows(int)}.

        If you want to set height of single line {@link TextField}, call
        {@link #setRows(int)} with value 0 after setting the height. Setting
        rows to 0 resets the side-effect.

        Starting from 6.5 you should use {@link TextArea} instead of
        {@link TextField} for multiline text input.

        @see com.vaadin.ui.AbstractComponent#setHeight(float, int)
        ---
        Sets the height of the {@link TextField} instance.

        <p>
        Setting height for {@link TextField} also has a side-effect that puts
        {@link TextField} into multiline mode (aka "textarea"). Multiline mode
        can also be achieved by calling {@link #setRows(int)}. The height
        value overrides the number of rows set by {@link #setRows(int)}.
        <p>
        If you want to set height of single line {@link TextField}, call
        {@link #setRows(int)} with value 0 after setting the height. Setting
        rows to 0 resets the side-effect.

        @see com.vaadin.ui.AbstractComponent#setHeight(java.lang.String)
        """
        if unit is None:
            # will call setHeight(float, int) the actually does the magic.
            # Method is overridden just to document side-effects.
            super(TextField, self).setHeight(height)
        else:
            super(TextField, self).setHeight(height, unit)
            if height > 1 and self.__class__ == TextField:
                # In html based terminals we most commonly want to make
                # component to be textarea if height is defined. Setting row
                # field above 0 will render component as textarea.
                self.setRows(2)
