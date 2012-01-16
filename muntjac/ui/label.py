# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

"""Defines a component for showing non-editable short texts."""

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

      - B{<b>} Bold
      - B{<i>} Italic
      - B{<u>} Underlined
      - B{<br/>} Linebreak
      - B{<ul><li>item 1</li><li>item 2</li></ul>} List of items

    The B{b},B{i},B{u} and B{li} tags can contain all the tags
    in the list recursively.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    CLIENT_WIDGET = None #ClientWidget(VLabel, LoadStyle.EAGER)

    #: Content mode, where the label contains only plain text. The getValue()
    #  result is coded to XML when painting.
    CONTENT_TEXT = 0

    #: Content mode, where the label contains preformatted text.
    CONTENT_PREFORMATTED = 1

    #: Formatted content mode, where the contents is XML restricted to the UIDL
    #  1.0 formatting markups.
    #
    # @deprecated: Use CONTENT_XML instead.
    CONTENT_UIDL = 2

    #: Content mode, where the label contains XHTML. Contents is then enclosed
    #  in DIV elements having namespace of
    #  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd".
    CONTENT_XHTML = 3

    #: Content mode, where the label contains well-formed or well-balanced XML.
    #  Each of the root elements must have their default namespace specified.
    CONTENT_XML = 4

    #: Content mode, where the label contains RAW output. Output is not
    #  required to comply to with XML. In Web Adapter output is inserted inside
    #  the resulting HTML document as-is. This is useful for some specific
    #  purposes where possibly broken HTML content needs to be shown, but in
    #  most cases XHTML mode should be preferred.
    CONTENT_RAW = 5

    #: The default content mode is plain text.
    CONTENT_DEFAULT = CONTENT_TEXT

    #: Array of content mode names that are rendered in UIDL as mode attribute.
    _CONTENT_MODE_NAME = ['text', 'pre', 'uidl', 'xhtml', 'xml', 'raw']

    _DATASOURCE_MUST_BE_SET = 'Datasource must be set'


    def __init__(self, contentSource="", contentMode=None):
        """Creates a new instance of Label with text-contents read from given
        datasource.
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

        @param readOnly:
                   True to enable read-only mode, False to disable it.
        """
        if self._dataSource is None:
            raise ValueError, self._DATASOURCE_MUST_BE_SET
        self._dataSource.setReadOnly(readOnly)


    def isReadOnly(self):
        """Is the component read-only ? Readonly is not used in label - this
        returns always false.

        @return: C{True} if the component is in read only mode.
        """
        if self._dataSource is None:
            raise ValueError, self._DATASOURCE_MUST_BE_SET
        return self._dataSource.isReadOnly()


    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the Paint Event.
        @raise PaintException:
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

        @return: the Value of the label.
        """
        if self._dataSource is None:
            raise ValueError, self._DATASOURCE_MUST_BE_SET
        return self._dataSource.getValue()


    def setValue(self, newValue):
        """Set the value of the label. Value of the label is the XML
        contents of the label.

        @param newValue:
                   the New value of the label.
        """
        if self._dataSource is None:
            raise ValueError, self._DATASOURCE_MUST_BE_SET
        self._dataSource.setValue(newValue)


    def __str__(self):
        if self._dataSource is None:
            raise ValueError, self._DATASOURCE_MUST_BE_SET
        return str(self._dataSource)


    def getType(self):
        """Gets the type of the IProperty.

        @see: L{IProperty.getType}
        """
        if self._dataSource is None:
            raise ValueError, self._DATASOURCE_MUST_BE_SET
        return self._dataSource.getType()


    def getPropertyDataSource(self):
        """Gets the viewing data-source property.

        @return: the data source property.
        @see: L{IViewer.getPropertyDataSource}
        """
        return self._dataSource


    def setPropertyDataSource(self, newDataSource):
        """Sets the property as data-source for viewing.

        @param newDataSource:
                   the new data source IProperty
        @see: L{IViewer.setPropertyDataSource}
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

          - B{CONTENT_TEXT} Content mode, where the label contains only plain
            text. The getValue() result is coded to XML when painting.
          - B{CONTENT_PREFORMATTED} Content mode, where the label contains
            preformatted text.
          - B{CONTENT_UIDL} Formatted content mode, where the contents is XML
            restricted to the UIDL 1.0 formatting markups.
          - B{CONTENT_XHTML} Content mode, where the label contains XHTML.
            Contents is then enclosed in DIV elements having namespace of
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd".
          - B{CONTENT_XML} Content mode, where the label contains well-formed
            or well-balanced XML. Each of the root elements must have their
            default namespace specified.
          - B{CONTENT_RAW} Content mode, where the label contains RAW output.
            Output is not required to comply to with XML. In Web Adapter output
            is inserted inside the resulting HTML document as-is. This is
            useful for some specific purposes where possibly broken HTML
            content needs to be shown, but in most cases XHTML mode should be
            preferred.

        @return: the Content mode of the label.
        """
        return self._contentMode


    def setContentMode(self, contentMode):
        """Sets the content mode of the Label.

        Possible content modes include:

          - B{CONTENT_TEXT} Content mode, where the label contains only plain
            text. The getValue() result is coded to XML when painting.
          - B{CONTENT_PREFORMATTED} Content mode, where the label contains
            preformatted text.
          - B{CONTENT_UIDL} Formatted content mode, where the contents is XML
            restricted to the UIDL 1.0 formatting markups.
          - B{CONTENT_XHTML} Content mode, where the label contains XHTML.
            Contents is then enclosed in DIV elements having namespace of
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd".
          - B{CONTENT_XML} Content mode, where the label contains well-formed
            or well-balanced XML. Each of the root elements must have their
            default namespace specified.
          - B{CONTENT_RAW} Content mode, where the label contains RAW output.
            Output is not required to comply to with XML. In Web Adapter output
            is inserted inside the resulting HTML document as-is. This is
            useful for some specific purposes where possibly broken HTML
            content needs to be shown, but in most cases XHTML mode should be
            preferred.

        @param contentMode:
                   the New content mode of the label.
        """
        # Value change events
        if (contentMode != self._contentMode
                and contentMode >= self.CONTENT_TEXT
                and contentMode <= self.CONTENT_RAW):
            self._contentMode = contentMode
            self.requestRepaint()


    def addListener(self, listener, iface=None):
        """Adds the value change listener."""
        if (isinstance(listener, prop.IValueChangeListener) and
                (iface is None or
                        issubclass(iface, prop.IValueChangeListener))):
            self.registerListener(ValueChangeEvent, listener,
                    _VALUE_CHANGE_METHOD)

        super(Label, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, prop.ValueChangeEvent):
            self.registerCallback(prop.ValueChangeEvent, callback, None, *args)
        else:
            super(Label, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        """Removes the value change listener."""
        if (isinstance(listener, prop.IValueChangeListener) and
                (iface is None or
                        issubclass(iface, prop.IValueChangeListener))):
            self.withdrawListener(ValueChangeEvent, listener,
                    _VALUE_CHANGE_METHOD)

        super(Label, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, prop.ValueChangeEvent):
            self.withdrawCallback(prop.ValueChangeEvent, callback)
        else:
            super(Label, self).removeCallback(callback, eventType)


    def fireValueChange(self):
        """Emits the options change event."""
        event = ValueChangeEvent(self)
        self.fireEvent(event)
        self.requestRepaint()


    def valueChange(self, event):
        """Listens the value change events from data source."""
        self.fireValueChange()


    def compareTo(self, other):
        """Compares the Label to other objects.

        Labels can be compared to other labels for sorting label contents.
        This is especially handy for sorting table columns.

        In RAW, PREFORMATTED and TEXT modes, the label contents are compared
        as is. In XML, UIDL and XHTML modes, only CDATA is compared and tags
        ignored. If the other object is not a Label, its toString() return
        value is used in comparison.

        @param other:
                   the Other object to compare to.
        @return: a negative integer, zero, or a positive integer as this object
                is less than, equal to, or greater than the specified object.
        """
        if (self._contentMode == self.CONTENT_XML
                or self._contentMode == self.CONTENT_UIDL
                or self._contentMode == self.CONTENT_XHTML):
            thisValue = self.stripTags(str(self))
        else:
            thisValue = str(self)

        if (isinstance(other, Label)
                and (other.getContentMode() == self.CONTENT_XML
                     or other.getContentMode() == self.CONTENT_UIDL
                     or other.getContentMode() == self.CONTENT_XHTML)):
            otherValue = self.stripTags(str(other))
        else:
            otherValue = str(other)

        return cmp(thisValue, otherValue)


    def stripTags(self, xml):
        """Strips the tags from the XML.

        @param xml: the string containing a XML snippet.
        @return: the original XML without tags.
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
