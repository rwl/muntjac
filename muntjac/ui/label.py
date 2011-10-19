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

try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from muntjac.data.util.object_property import ObjectProperty
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.component import Event as ComponentEvent

from muntjac.data import property as prop


_VALUE_CHANGE_METHOD = getattr(prop.IValueChangeListener, "valueChange")


class Label(AbstractComponent, prop.IProperty, prop.IViewer,
            prop.IValueChangeListener, prop.IValueChangeNotifier):
    """Label component for showing non-editable short texts.

    The label content can be set to the modes specified by the final members
    CONTENT_*

    The contents of the label may contain simple formatting:
    <ul>
    <li><b>&lt;b></b> Bold
    <li><b>&lt;i></b> Italic
    <li><b>&lt;u></b> Underlined
    <li><b>&lt;br/></b> Linebreak
    <li><b>&lt;ul>&lt;li>item 1&lt;/li>&lt;li>item 2&lt;/li>&lt;/ul></b> List
    of items
    </ul>
    The <b>b</b>,<b>i</b>,<b>u</b> and <b>li</b> tags can contain all the tags
    in the list recursively.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    #CLIENT_WIDGET = ClientWidget(VLabel, LoadStyle.EAGER)

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


    def __init__(self, contentSource="", contentMode=None):

        """Creates a new instance of Label with text-contents read from given
        datasource.

        @param contentSource
        @param contentMode
        """
        super(Label, self).__init__()

        self._dataSource = None
        self._contentMode = self.CONTENT_DEFAULT

        if isinstance(contentSource, basestring):
            contentSource = ObjectProperty(contentSource, str)

        if contentMode is None:
            contentMode = self.CONTENT_DEFAULT

        self.setPropertyDataSource(contentSource)

        if contentMode != self.CONTENT_DEFAULT:
            self.setContentMode(contentMode)

        self.setWidth(100, self.UNITS_PERCENTAGE)


    def setReadOnly(self, readOnly):
        """Set the component to read-only. Readonly is not used in label.

        @param readOnly
                   True to enable read-only mode, False to disable it.
        """
        if self._dataSource is None:
            raise ValueError, self._DATASOURCE_MUST_BE_SET
        self._dataSource.setReadOnly(readOnly)


    def isReadOnly(self):
        """Is the component read-only ? Readonly is not used in label - this
        returns always false.

        @return <code>true</code> if the component is in read only mode.
        """
        if self._dataSource is None:
            raise ValueError, self._DATASOURCE_MUST_BE_SET
        return self._dataSource.isReadOnly()


    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   the Paint Event.
        @throws PaintException
                    if the Paint Operation fails.
        """
        if self._contentMode != self.CONTENT_TEXT:
            target.addAttribute('mode',
                    self._CONTENT_MODE_NAME[self._contentMode])

        if self._contentMode == self.CONTENT_TEXT:
            target.addText(str(self))

        elif self._contentMode == self.CONTENT_UIDL:
            target.addUIDL(str(self))

        elif self._contentMode == self.CONTENT_XHTML:
            target.startTag('data')
            target.addXMLSection('div', str(self),
                    'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd')
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
        """Gets the value of the label. Value of the label is the XML
        contents of the label.

        @return the Value of the label.
        """
        if self._dataSource is None:
            raise ValueError, self._DATASOURCE_MUST_BE_SET
        return self._dataSource.getValue()


    def setValue(self, newValue):
        """Set the value of the label. Value of the label is the XML
        contents of the label.

        @param newValue
                   the New value of the label.
        """
        if self._dataSource is None:
            raise ValueError, self._DATASOURCE_MUST_BE_SET
        self._dataSource.setValue(newValue)


    def __str__(self):
        """@see java.lang.Object#toString()"""
        if self._dataSource is None:
            raise ValueError, self._DATASOURCE_MUST_BE_SET
        return str(self._dataSource)


    def getType(self):
        """Gets the type of the IProperty.

        @see com.vaadin.data.IProperty#getType()
        """
        if self._dataSource is None:
            raise ValueError, self._DATASOURCE_MUST_BE_SET
        return self._dataSource.getType()


    def getPropertyDataSource(self):
        """Gets the viewing data-source property.

        @return the data source property.
        @see com.vaadin.data.property.IViewer#getPropertyDataSource()
        """
        return self._dataSource


    def setPropertyDataSource(self, newDataSource):
        """Sets the property as data-source for viewing.

        @param newDataSource
                   the new data source IProperty
        @see property.IViewer#setPropertyDataSource()
        """
        # Stops listening the old data source changes
        if (self._dataSource is not None
                and issubclass(self._dataSource.__class__,
                        prop.IValueChangeNotifier)):
            self._dataSource.removeListener(self, prop.IValueChangeListener)

        # Sets the new data source
        self._dataSource = newDataSource

        # Listens the new data source if possible
        if (self._dataSource is not None
                and issubclass(self._dataSource.__class__,
                        prop.IValueChangeNotifier)):
            self._dataSource.addListener(self, prop.IValueChangeListener)

        self.requestRepaint()


    def getContentMode(self):
        """Gets the content mode of the Label.

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

        @return the Content mode of the label.
        """
        return self._contentMode


    def setContentMode(self, contentMode):
        """Sets the content mode of the Label.

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

        @param contentMode
                   the New content mode of the label.
        """
        # Value change events
        if (contentMode != self._contentMode
                and contentMode >= self.CONTENT_TEXT
                and contentMode <= self.CONTENT_RAW):
            self._contentMode = contentMode
            self.requestRepaint()


    def addListener(self, listener, iface):
        """Adds the value change listener."""
        if iface == prop.IValueChangeListener:
            self.registerListener(ValueChangeEvent, listener,
                    _VALUE_CHANGE_METHOD)
        else:
            super(Label, self).addListener(listener, iface)


    def addValueChangeListener(self, listener):
        self.addListener(listener, prop.IValueChangeListener)


    def removeListener(self, listener, iface):
        """Removes the value change listener."""
        if isinstance(listener, prop.IValueChangeListener):
            self.withdrawListener(ValueChangeEvent, listener,
                    _VALUE_CHANGE_METHOD)
        else:
            super(Label, self).removeListener(listener, iface)


    def removeValueChangeListener(self, listener):
        self.removeListener(listener, prop.IValueChangeListener)


    def fireValueChange(self):
        """Emits the options change event."""
        # Set the error message
        self.fireEvent( ValueChangeEvent(self) )
        self.requestRepaint()


    def valueChange(self, event):
        """Listens the value change events from data source."""
        self.fireValueChange()


    def __eq__(self, other):
        """Compares the Label to other objects.

        Labels can be compared to other labels for sorting label contents.
        This is especially handy for sorting table columns.

        In RAW, PREFORMATTED and TEXT modes, the label contents are compared
        as is. In XML, UIDL and XHTML modes, only CDATA is compared and tags
        ignored. If the other object is not a Label, its toString() return
        value is used in comparison.

        @param other
                   the Other object to compare to.
        @return a negative integer, zero, or a positive integer as this object
                is less than, equal to, or greater than the specified object.
        @see java.lang.Comparable#compareTo(java.lang.Object)
        """
        if (self._contentMode == self.CONTENT_XML
                or self._contentMode == self.CONTENT_UIDL
                or self._contentMode == self.CONTENT_XHTML):
            thisValue = self.stripTags(str(self))
        else:
            thisValue = str(self)
        if isinstance(other, Label) \
                and (other.getContentMode() == self.CONTENT_XML
                     or other.getContentMode() == self.CONTENT_UIDL
                     or other.getContentMode() == self.CONTENT_XHTML):
            otherValue = self.stripTags(str(other))
        else:
            otherValue = str(other)

        return thisValue == otherValue


    def stripTags(self, xml):
        """Strips the tags from the XML.

        @param xml
                   the String containing a XML snippet.
        @return the original XML without tags.
        """
        res = StringIO()
        processed = 0
        xmlLen = len(xml)
        while processed < xmlLen:
            nxt = xml.find('<', processed)
            if nxt < 0:
                nxt = xmlLen
            res.write(xml[processed:nxt])
            if processed < xmlLen:
                nxt = xml.find('>', processed)
                if nxt < 0:
                    nxt = xmlLen
                processed = nxt + 1
        result = res.getvalue()
        res.close()
        return result


class ValueChangeEvent(ComponentEvent, prop.ValueChangeEvent):
    """Value change event."""

    def __init__(self, source):
        """New instance of text change event."""
        super(ValueChangeEvent, self).__init__(source)


    def getProperty(self):
        """Gets the IProperty that has been modified."""
        return self.getSource()
