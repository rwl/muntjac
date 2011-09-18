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
from com.vaadin.data.util.ObjectProperty import (ObjectProperty,)
from com.vaadin.ui.AbstractComponent import (AbstractComponent,)
from com.vaadin.data.Property import (Property, ValueChangeListener, ValueChangeNotifier, Viewer,)
# from com.vaadin.ui.ClientWidget.LoadStyle import (LoadStyle,)
# from java.lang.reflect.Method import (Method,)


class Label(AbstractComponent, Property, Property, Viewer, Property, ValueChangeListener, Property, ValueChangeNotifier, Comparable):
    """Label component for showing non-editable short texts.

    The label content can be set to the modes specified by the final members
    CONTENT_*

    <p>
    The contents of the label may contain simple formatting:
    <ul>
    <li><b>&lt;b></b> Bold
    <li><b>&lt;i></b> Italic
    <li><b>&lt;u></b> Underlined
    <li><b>&lt;br/></b> Linebreak
    <li><b>&lt;ul>&lt;li>item 1&lt;/li>&lt;li>item 2&lt;/li>&lt;/ul></b> List of
    items
    </ul>
    The <b>b</b>,<b>i</b>,<b>u</b> and <b>li</b> tags can contain all the tags in
    the list recursively.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Content mode, where the label contains only plain text. The getValue()
    # result is coded to XML when painting.

    CONTENT_TEXT = 0
    # Content mode, where the label contains preformatted text.
    CONTENT_PREFORMATTED = 1
    # Formatted content mode, where the contents is XML restricted to the UIDL
    # 1.0 formatting markups.
    #
    # @deprecated Use CONTENT_XML instead.

    CONTENT_UIDL = 2
    # Content mode, where the label contains XHTML. Contents is then enclosed
    # in DIV elements having namespace of
    # "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd".

    CONTENT_XHTML = 3
    # Content mode, where the label contains well-formed or well-balanced XML.
    # Each of the root elements must have their default namespace specified.

    CONTENT_XML = 4
    # Content mode, where the label contains RAW output. Output is not required
    # to comply to with XML. In Web Adapter output is inserted inside the
    # resulting HTML document as-is. This is useful for some specific purposes
    # where possibly broken HTML content needs to be shown, but in most cases
    # XHTML mode should be preferred.

    CONTENT_RAW = 5
    # The default content mode is plain text.
    CONTENT_DEFAULT = CONTENT_TEXT
    # Array of content mode names that are rendered in UIDL as mode attribute.
    _CONTENT_MODE_NAME = ['text', 'pre', 'uidl', 'xhtml', 'xml', 'raw']
    _DATASOURCE_MUST_BE_SET = 'Datasource must be set'
    _dataSource = None
    _contentMode = CONTENT_DEFAULT

    def __init__(self, *args):
        """Creates an empty Label.
        ---
        Creates a new instance of Label with text-contents.

        @param content
        ---
        Creates a new instance of Label with text-contents read from given
        datasource.

        @param contentSource
        ---
        Creates a new instance of Label with text-contents.

        @param content
        @param contentMode
        ---
        Creates a new instance of Label with text-contents read from given
        datasource.

        @param contentSource
        @param contentMode
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__('')
        elif _1 == 1:
            if isinstance(_0[0], Property):
                contentSource, = _0
                self.__init__(contentSource, self.CONTENT_DEFAULT)
            else:
                content, = _0
                self.__init__(content, self.CONTENT_DEFAULT)
        elif _1 == 2:
            if isinstance(_0[0], Property):
                contentSource, contentMode = _0
                self.setPropertyDataSource(contentSource)
                if contentMode != self.CONTENT_DEFAULT:
                    self.setContentMode(contentMode)
                self.setWidth(100, self.UNITS_PERCENTAGE)
            else:
                content, contentMode = _0
                self.__init__(ObjectProperty(content, str), contentMode)
        else:
            raise ARGERROR(0, 2)

    def setReadOnly(self, readOnly):
        """Set the component to read-only. Readonly is not used in label.

        @param readOnly
                   True to enable read-only mode, False to disable it.
        """
        if self._dataSource is None:
            raise self.IllegalStateException(self._DATASOURCE_MUST_BE_SET)
        self._dataSource.setReadOnly(readOnly)

    def isReadOnly(self):
        """Is the component read-only ? Readonly is not used in label - this returns
        allways false.

        @return <code>true</code> if the component is in read only mode.
        """
        if self._dataSource is None:
            raise self.IllegalStateException(self._DATASOURCE_MUST_BE_SET)
        return self._dataSource.isReadOnly()

    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   the Paint Event.
        @throws PaintException
                    if the Paint Operation fails.
        """
        if self._contentMode != self.CONTENT_TEXT:
            target.addAttribute('mode', self._CONTENT_MODE_NAME[self._contentMode])
        if self._contentMode == self.CONTENT_TEXT:
            target.addText(str(self))
        elif self._contentMode == self.CONTENT_UIDL:
            target.addUIDL(str(self))
        elif self._contentMode == self.CONTENT_XHTML:
            target.startTag('data')
            target.addXMLSection('div', str(self), 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd')
            target.endTag('data')
        elif self._contentMode == self.CONTENT_PREFORMATTED:
            target.startTag('pre')
            target.addText(str(self))
            target.endTag('pre')
        elif self._contentMode == self.CONTENT_XML:
            target.addXMLSection('data', str(self), None)
        elif self._contentMode == self.CONTENT_RAW:
            target.startTag('data')
            target.addAttribute('escape', False)
            target.addText(str(self))
            target.endTag('data')

    def getValue(self):
        """Gets the value of the label. Value of the label is the XML contents of
        the label.

        @return the Value of the label.
        """
        if self._dataSource is None:
            raise self.IllegalStateException(self._DATASOURCE_MUST_BE_SET)
        return self._dataSource.getValue()

    def setValue(self, newValue):
        """Set the value of the label. Value of the label is the XML contents of the
        label.

        @param newValue
                   the New value of the label.
        """
        if self._dataSource is None:
            raise self.IllegalStateException(self._DATASOURCE_MUST_BE_SET)
        self._dataSource.setValue(newValue)

    def toString(self):
        """@see java.lang.Object#toString()"""
        if self._dataSource is None:
            raise self.IllegalStateException(self._DATASOURCE_MUST_BE_SET)
        return str(self._dataSource)

    def getType(self):
        """Gets the type of the Property.

        @see com.vaadin.data.Property#getType()
        """
        if self._dataSource is None:
            raise self.IllegalStateException(self._DATASOURCE_MUST_BE_SET)
        return self._dataSource.getType()

    def getPropertyDataSource(self):
        """Gets the viewing data-source property.

        @return the data source property.
        @see com.vaadin.data.Property.Viewer#getPropertyDataSource()
        """
        return self._dataSource

    def setPropertyDataSource(self, newDataSource):
        """Sets the property as data-source for viewing.

        @param newDataSource
                   the new data source Property
        @see com.vaadin.data.Property.Viewer#setPropertyDataSource(com.vaadin.data.Property)
        """
        # Stops listening the old data source changes
        if (
            self._dataSource is not None and Property.ValueChangeNotifier.isAssignableFrom(self._dataSource.getClass())
        ):
            self._dataSource.removeListener(self)
        # Sets the new data source
        self._dataSource = newDataSource
        # Listens the new data source if possible
        if (
            self._dataSource is not None and Property.ValueChangeNotifier.isAssignableFrom(self._dataSource.getClass())
        ):
            self._dataSource.addListener(self)
        self.requestRepaint()

    def getContentMode(self):
        """Gets the content mode of the Label.

        <p>
        Possible content modes include:
        <ul>
        <li><b>CONTENT_TEXT</b> Content mode, where the label contains only plain
        text. The getValue() result is coded to XML when painting.</li>
        <li><b>CONTENT_PREFORMATTED</b> Content mode, where the label contains
        preformatted text.</li>
        <li><b>CONTENT_UIDL</b> Formatted content mode, where the contents is XML
        restricted to the UIDL 1.0 formatting markups.</li>
        <li><b>CONTENT_XHTML</b> Content mode, where the label contains XHTML.
        Contents is then enclosed in DIV elements having namespace of
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd".</li>
        <li><b>CONTENT_XML</b> Content mode, where the label contains well-formed
        or well-balanced XML. Each of the root elements must have their default
        namespace specified.</li>
        <li><b>CONTENT_RAW</b> Content mode, where the label contains RAW output.
        Output is not required to comply to with XML. In Web Adapter output is
        inserted inside the resulting HTML document as-is. This is useful for
        some specific purposes where possibly broken HTML content needs to be
        shown, but in most cases XHTML mode should be preferred.</li>
        </ul>
        </p>

        @return the Content mode of the label.
        """
        return self._contentMode

    def setContentMode(self, contentMode):
        """Sets the content mode of the Label.

        <p>
        Possible content modes include:
        <ul>
        <li><b>CONTENT_TEXT</b> Content mode, where the label contains only plain
        text. The getValue() result is coded to XML when painting.</li>
        <li><b>CONTENT_PREFORMATTED</b> Content mode, where the label contains
        preformatted text.</li>
        <li><b>CONTENT_UIDL</b> Formatted content mode, where the contents is XML
        restricted to the UIDL 1.0 formatting markups.</li>
        <li><b>CONTENT_XHTML</b> Content mode, where the label contains XHTML.
        Contents is then enclosed in DIV elements having namespace of
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd".</li>
        <li><b>CONTENT_XML</b> Content mode, where the label contains well-formed
        or well-balanced XML. Each of the root elements must have their default
        namespace specified.</li>
        <li><b>CONTENT_RAW</b> Content mode, where the label contains RAW output.
        Output is not required to comply to with XML. In Web Adapter output is
        inserted inside the resulting HTML document as-is. This is useful for
        some specific purposes where possibly broken HTML content needs to be
        shown, but in most cases XHTML mode should be preferred.</li>
        </ul>
        </p>

        @param contentMode
                   the New content mode of the label.
        """
        # Value change events
        if (
            contentMode != self._contentMode and contentMode >= self.CONTENT_TEXT and contentMode <= self.CONTENT_RAW
        ):
            self._contentMode = contentMode
            self.requestRepaint()

    _VALUE_CHANGE_METHOD = None


#    static {
#        try {
#            VALUE_CHANGE_METHOD = Property.ValueChangeListener.class
#                    .getDeclaredMethod("valueChange",
#                            new Class[] { Property.ValueChangeEvent.class });
#        } catch (java.lang.NoSuchMethodException e) {
#            // This should never happen
#            throw new java.lang.RuntimeException(
#                    "Internal error finding methods in Label");
#        }
#    }
#
#    /**
#     * Value change event
#     *
#     * @author IT Mill Ltd.
#     * @version
#     * @VERSION@
#     * @since 3.0
#     */
#    public class ValueChangeEvent extends Component.Event implements
#            Property.ValueChangeEvent {
#
#        /**
#         * New instance of text change event
#         *
#         * @param source
#         *            the Source of the event.
#         */
#        public ValueChangeEvent(Label source) {
#            super(source);
#        }
#
#        /**
#         * Gets the Property that has been modified.
#         *
#         * @see com.vaadin.data.Property.ValueChangeEvent#getProperty()
#         */
#        public Property getProperty() {
#            return (Property) getSource();
#        }
#    }
#
#    /**
#     * Adds the value change listener.
#     *
#     * @param listener
#     *            the Listener to be added.
#     * @see com.vaadin.data.Property.ValueChangeNotifier#addListener(com.vaadin.data.Property.ValueChangeListener)
#     */
#    public void addListener(Property.ValueChangeListener listener) {
#        addListener(Label.ValueChangeEvent.class, listener, VALUE_CHANGE_METHOD);
#    }
#
#    /**
#     * Removes the value change listener.
#     *
#     * @param listener
#     *            the Listener to be removed.
#     * @see com.vaadin.data.Property.ValueChangeNotifier#removeListener(com.vaadin.data.Property.ValueChangeListener)
#     */
#    public void removeListener(Property.ValueChangeListener listener) {
#        removeListener(Label.ValueChangeEvent.class, listener,
#                VALUE_CHANGE_METHOD);
#    }
#
#    /**
#     * Emits the options change event.
#     */
#    protected void fireValueChange() {
#        // Set the error message
#        fireEvent(new Label.ValueChangeEvent(this));
#        requestRepaint();
#    }
#
#    /**
#     * Listens the value change events from data source.
#     *
#     * @see com.vaadin.data.Property.ValueChangeListener#valueChange(Property.ValueChangeEvent)
#     */
#    public void valueChange(Property.ValueChangeEvent event) {
#        fireValueChange();
#    }

    def compareTo(self, other):
        """Compares the Label to other objects.

        <p>
        Labels can be compared to other labels for sorting label contents. This
        is especially handy for sorting table columns.
        </p>

        <p>
        In RAW, PREFORMATTED and TEXT modes, the label contents are compared as
        is. In XML, UIDL and XHTML modes, only CDATA is compared and tags
        ignored. If the other object is not a Label, its toString() return value
        is used in comparison.
        </p>

        @param other
                   the Other object to compare to.
        @return a negative integer, zero, or a positive integer as this object is
                less than, equal to, or greater than the specified object.
        @see java.lang.Comparable#compareTo(java.lang.Object)
        """
        if (
            ((self._contentMode == self.CONTENT_XML) or (self._contentMode == self.CONTENT_UIDL)) or (self._contentMode == self.CONTENT_XHTML)
        ):
            thisValue = self.stripTags(str(self))
        else:
            thisValue = str(self)
        if (
            isinstance(other, Label) and ((other.getContentMode() == self.CONTENT_XML) or (other.getContentMode() == self.CONTENT_UIDL)) or (other.getContentMode() == self.CONTENT_XHTML)
        ):
            otherValue = self.stripTags(str(other))
        else:
            otherValue = str(other)
        return thisValue.compareTo(otherValue)

    def stripTags(self, xml):
        """Strips the tags from the XML.

        @param xml
                   the String containing a XML snippet.
        @return the original XML without tags.
        """
        res = str()
        processed = 0
        xmlLen = len(xml)
        while processed < xmlLen:
            next = xml.find('<', processed)
            if next < 0:
                next = xmlLen
            res.__add__(xml[processed:next])
            if processed < xmlLen:
                next = xml.find('>', processed)
                if next < 0:
                    next = xmlLen
                processed = next + 1
        return str(res)
