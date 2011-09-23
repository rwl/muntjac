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

from muntjac.ui.AbstractField import AbstractField
from muntjac.data.Property import Property
from muntjac.terminal.gwt.client.ui.richtextarea.VRichTextArea import VRichTextArea
from muntjac.ui.ClientWidget import LoadStyle


class RichTextArea(AbstractField):
    """A simple RichTextArea to edit HTML format text.

    Note, that using {@link TextField#setMaxLength(int)} method in
    {@link RichTextArea} may produce unexpected results as formatting is counted
    into length of field.
    """

    CLIENT_WIDGET = VRichTextArea
    LOAD_STYLE = LoadStyle.LAZY

    def __init__(self, *args):
        """Constructs an empty <code>RichTextArea</code> with no caption.
        ---
        Constructs an empty <code>RichTextArea</code> with the given caption.

        @param caption
                   the caption for the editor.
        ---
        Constructs a new <code>RichTextArea</code> that's bound to the specified
        <code>Property</code> and has no caption.

        @param dataSource
                   the data source for the editor value
        ---
        Constructs a new <code>RichTextArea</code> that's bound to the specified
        <code>Property</code> and has the given caption.

        @param caption
                   the caption for the editor.
        @param dataSource
                   the data source for the editor value
        ---
        Constructs a new <code>RichTextArea</code> with the given caption and
        initial text contents.

        @param caption
                   the caption for the editor.
        @param value
                   the initial text content of the editor.
        """
        # Value formatter used to format the string contents.
        self._format = None

        # Null representation.
        self._nullRepresentation = 'null'

        # Is setting to null from non-null value allowed by setting with null
        # representation .
        self._nullSettingAllowed = False

        # Temporary flag that indicates all content will be selected after the next
        # paint. Reset to false after painted.
        self._selectAll = False

        args = args
        nargs = len(args)
        if nargs == 0:
            self.setValue('')
        elif nargs == 1:
            if isinstance(args[0], Property):
                dataSource, = args
                self.setPropertyDataSource(dataSource)
            else:
                caption, = args
                self.__init__()
                self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], Property):
                caption, dataSource = args
                self.__init__(dataSource)
                self.setCaption(caption)
            else:
                caption, value = args
                self.setValue(value)
                self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'


    def paintContent(self, target):
        if self._selectAll:
            target.addAttribute('selectAll', True)
            self._selectAll = False

        # Adds the content as variable
        value = self.getFormattedValue()
        if value is None:
            value = self.getNullRepresentation()

        if value is None:
            raise ValueError, 'Null values are not allowed if the null-representation is null'

        target.addVariable(self, 'text', value)

        super(RichTextArea, self).paintContent(target)


    def setReadOnly(self, readOnly):
        super(RichTextArea, self).setReadOnly(readOnly)
        # IE6 cannot support multi-classname selectors properly
        if readOnly:
            self.addStyleName('v-richtextarea-readonly')
        else:
            self.removeStyleName('v-richtextarea-readonly')


    def selectAll(self):
        """Selects all text in the rich text area. As a side effect, focuses the
        rich text area.

        @since 6.5
        """
        # Set selection range functionality is currently being
        # planned/developed for GWT RTA. Only selecting all is currently
        # supported. Consider moving selectAll and other selection related
        # functions to AbstractTextField at that point to share the
        # implementation. Some third party components extending
        # AbstractTextField might however not want to support them.
        self._selectAll = True
        self.focus()
        self.requestRepaint()


    def getFormattedValue(self):
        """Gets the formatted string value. Sets the field value by using the
        assigned Format.

        @return the Formatted value.
        @see #setFormat(Format)
        @see Format
        @deprecated
        """
        v = self.getValue()
        if v is None:
            return None
        return str(v)


    def getValue(self):
        v = super(RichTextArea, self).getValue()
        if (self._format is None) or (v is None):
            return v
        try:
            return self._format.format(v)
        except ValueError:
            return v


    def changeVariables(self, source, variables):

        super(RichTextArea, self).changeVariables(source, variables)

        # Sets the text
        if 'text' in variables and not self.isReadOnly():

            # Only do the setting if the string representation of the value
            # has been updated
            newValue = variables['text']

            oldValue = self.getFormattedValue()
            if newValue is not None \
                    and (oldValue is None) or self.isNullSettingAllowed() \
                    and newValue == self.getNullRepresentation():
                newValue = None

            if newValue != oldValue \
                    and (newValue is None or not (newValue == oldValue)):
                wasModified = self.isModified()
                self.setValue(newValue, True)

                # If the modified status changes, or if we have a formatter,
                # repaint is needed after all.
                if (self._format is not None or wasModified != self.isModified()):
                    self.requestRepaint()


    def getType(self):
        return basestring


    def getNullRepresentation(self):
        """Gets the null-string representation.

        <p>
        The null-valued strings are represented on the user interface by
        replacing the null value with this string. If the null representation is
        set null (not 'null' string), painting null value throws exception.
        </p>

        <p>
        The default value is string 'null'.
        </p>

        @return the String Textual representation for null strings.
        @see TextField#isNullSettingAllowed()
        """
        return self._nullRepresentation


    def isNullSettingAllowed(self):
        """Is setting nulls with null-string representation allowed.

        <p>
        If this property is true, writing null-representation string to text
        field always sets the field value to real null. If this property is
        false, null setting is not made, but the null values are maintained.
        Maintenance of null-values is made by only converting the textfield
        contents to real null, if the text field matches the null-string
        representation and the current value of the field is null.
        </p>

        <p>
        By default this setting is false
        </p>

        @return boolean Should the null-string represenation be always converted
                to null-values.
        @see TextField#getNullRepresentation()
        """
        return self._nullSettingAllowed


    def setNullRepresentation(self, nullRepresentation):
        """Sets the null-string representation.

        <p>
        The null-valued strings are represented on the user interface by
        replacing the null value with this string. If the null representation is
        set null (not 'null' string), painting null value throws exception.
        </p>

        <p>
        The default value is string 'null'
        </p>

        @param nullRepresentation
                   Textual representation for null strings.
        @see TextField#setNullSettingAllowed(boolean)
        """
        self._nullRepresentation = nullRepresentation


    def setNullSettingAllowed(self, nullSettingAllowed):
        """Sets the null conversion mode.

        <p>
        If this property is true, writing null-representation string to text
        field always sets the field value to real null. If this property is
        false, null setting is not made, but the null values are maintained.
        Maintenance of null-values is made by only converting the textfield
        contents to real null, if the text field matches the null-string
        representation and the current value of the field is null.
        </p>

        <p>
        By default this setting is false.
        </p>

        @param nullSettingAllowed
                   Should the null-string represenation be always converted to
                   null-values.
        @see TextField#getNullRepresentation()
        """
        self._nullSettingAllowed = nullSettingAllowed


    def getFormat(self):
        """Gets the value formatter of TextField.

        @return the Format used to format the value.
        @deprecated replaced by {@link com.vaadin.data.util.PropertyFormatter}
        """
        return self._format


    def setFormat(self, frmt):
        """Gets the value formatter of TextField.

        @param format
                   the Format used to format the value. Null disables the
                   formatting.
        @deprecated replaced by {@link com.vaadin.data.util.PropertyFormatter}
        """
        self._format = frmt
        self.requestRepaint()


    def isEmpty(self):
        return super(RichTextArea, self).isEmpty() or (len(str(self)) == 0)
