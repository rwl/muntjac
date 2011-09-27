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

import logging
from Queue import LifoQueue
from muntjac.ui.CustomLayout import CustomLayout
from muntjac.terminal.Resource import Resource
from muntjac.terminal.ExternalResource import ExternalResource
from muntjac.terminal.ApplicationResource import ApplicationResource
from muntjac.terminal.ThemeResource import ThemeResource
from muntjac.ui.Alignment import Alignment
from muntjac.terminal.StreamVariable import StreamVariable

try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from muntjac.terminal.Paintable import Paintable
from muntjac.terminal.PaintTarget import PaintTarget
from muntjac.terminal.PaintException import PaintException


class JsonPaintTarget(PaintTarget):
    """User Interface Description Language Target.

    TODO document better: role of this class, UIDL format, attributes, variables,
    etc.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 5.0
    """
    _logger = logging.getLogger('.'.join(__package__, __class__.__name__))

    # Document type declarations
    _UIDL_ARG_NAME = 'name'

    def __init__(self, manager, outWriter, cachingRequired):
        """Creates a new XMLPrintWriter, without automatic line flushing.

        @param variableMap
        @param manager
        @param outWriter
                   A character-output stream.
        @throws PaintException
                    if the paint operation failed.
        """
        self._manager = manager
        # Sets the target for UIDL writing
        self._uidlBuffer = outWriter
        # Initialize tag-writing
        self._mOpenTags = LifoQueue()
        self._openJsonTags = LifoQueue()
        self._cacheEnabled = cachingRequired

        self._closed = False
        self._changes = 0
        self._usedResources = set()
        self._customLayoutArgumentsOpen = False
        self._tag = None
        self._errorsOpen = None
        self._paintedComponents = set()
        self._identifiersCreatedDueRefPaint = None
        self._usedPaintableTypes = list()


    def startTag(self, arg, arg2=False):
        """None
        ---
        Prints the element start tag.

        <pre>
          Todo:
           Checking of input values

        </pre>

        @param tagName
                   the name of the start tag.
        @throws PaintException
                    if the paint operation failed.
        """
        if isinstance(arg, Paintable):
            paintable, tagName = arg, arg2
            self.startTag(tagName, True)
            isPreviouslyPainted = self._manager.hasPaintableId(paintable) \
                and (self._identifiersCreatedDueRefPaint is None) \
                or (paintable not in self._identifiersCreatedDueRefPaint)
            idd = self._manager.getPaintableId(paintable)
            paintable.addListener(self._manager)
            self.addAttribute('id', idd)
            self._paintedComponents.add(paintable)

            if isinstance(paintable, CustomLayout):
                self._customLayoutArgumentsOpen = True

            return self._cacheEnabled and isPreviouslyPainted
        else:
            tagName, _ = arg, arg2
            if tagName is None:
                raise self.NullPointerException()

            # Ensures that the target is open
            if self._closed:
                raise PaintException('Attempted to write to a closed PaintTarget.')

            if self._tag is not None:
                self._openJsonTags.put(self._tag)

            # Checks tagName and attributes here
            self._mOpenTags.put(tagName)

            self._tag = JsonTag(tagName)

            if 'error' == tagName:
                self._errorsOpen += 1

            self._customLayoutArgumentsOpen = False


    def endTag(self, tagName):
        """Prints the element end tag.

        If the parent tag is closed before every child tag is closed an
        PaintException is raised.

        @param tag
                   the name of the end tag.
        @throws Paintexception
                    if the paint operation failed.
        """
        # In case of null data output nothing:
        if tagName is None:
            raise ValueError

        # Ensure that the target is open
        if self._closed:
            raise PaintException('Attempted to write to a closed PaintTarget.')

        if len(self._openJsonTags) > 0:
            parent = self._openJsonTags.pop()

            lastTag = ''

            lastTag = self._mOpenTags.pop()
            if tagName.lower() != lastTag.lower():
                raise PaintException('Invalid UIDL: wrong ending tag: \'' \
                        + tagName + '\' expected: \'' + lastTag + '\'.')

            # simple hack which writes error uidl structure into attribute
            if 'error' == lastTag:
                if self._errorsOpen == 1:
                    parent.addAttribute('\"error\":[\"error\",{}' \
                                        + self._tag.getData() + ']')
                else:
                    # sub error
                    parent.addData(self._tag.getJSON())

                self._errorsOpen -= 1
            else:
                parent.addData(self._tag.getJSON())

            self._tag = parent
        else:
            self._changes += 1
            self._uidlBuffer.write((',' if self._changes > 1 else '') \
                                   + self._tag.getJSON())
            self._tag = None


    @classmethod
    def escapeXML(cls, xml):
        """Substitutes the XML sensitive characters with predefined XML entities.

        @param xml
                   the String to be substituted.
        @return A new string instance where all occurrences of XML sensitive
                characters are substituted with entities.
        """
        if (xml is None) or (len(xml) <= 0):
            return ''

        return cls._escapeXML(xml)


    @classmethod
    def _escapeXML(cls, xml):
        """
        ---
        Substitutes the XML sensitive characters with predefined XML entities.

        @param xml
                   the String to be substituted.
        @return A new StringBuilder instance where all occurrences of XML
                sensitive characters are substituted with entities.
        """
        if (xml is None) or (len(xml) <= 0):
            return ''

        buff = StringIO()#(len(xml) * 2)

        for c in xml:
            s = cls.toXmlChar(c)
            if s is not None:
                buff.write(s)
            else:
                buff.write(c)

        result = buff.getvalue()
        buff.close()

        return result


    @classmethod
    def escapeJSON(cls, s):
        """Escapes the given string so it can safely be used as a JSON string.

        @param s
                   The string to escape
        @return Escaped version of the string
        """
        # FIXME: Move this method to another class as other classes use it
        # also.
        if s is None:
            return ''

        sb = StringIO()
        for ch in s:
            if ch == '"':
                sb.write('\\\"')
            elif ch == '\\':
                sb.write('\\\\')
            elif ch == '\b':
                sb.write('\\b')
            elif ch == '\f':
                sb.write('\\f')
            elif ch == '\n':
                sb.write('\\n')
            elif ch == '\r':
                sb.write('\\r')
            elif ch == '\t':
                sb.write('\\t')
            elif ch == '/':
                sb.write('\\/')
            else:
                if ch >= '\u0000' and ch <= '\u001F':
                    ss = hex( int(ch) )
                    sb.write('\\u')
                    _3 = True
                    k = 0
                    while k < 4 - len(ss):
                        k += 1
                        sb.write('0')
                    sb.write(ss.upper())
                else:
                    sb.write(ch)

        result = sb.getvalue()
        sb.close()

        return result


    @classmethod
    def toXmlChar(cls, c):
        """Substitutes a XML sensitive character with predefined XML entity.

        @param c
                   the Character to be replaced with an entity.
        @return String of the entity or null if character is not to be replaced
                with an entity.
        """
        if c == '&':
            return '&amp;'   # & => &amp;
        elif c == '>':
            return '&gt;'    # > => &gt;
        elif c == '<':
            return '&lt;'    # < => &lt;
        elif c == '"':
            return '&quot;'  # " => &quot;
        elif c == '\'':
            return '&apos;'  # ' => &apos;
        else:
            return None


    def addText(self, s):
        """Prints XML-escaped text.

        @param s
        @throws PaintException
                    if the paint operation failed.
        """
        self._tag.addData('\"' + self.escapeJSON(s) + '\"')


    def addAttribute(self, name, value):
        if isinstance(value, list):
            values = value
            # In case of null data output nothing:
            if (values is None) or (name is None):
                raise self.NullPointerException('Parameters must be non-null strings')
            buf = StringIO()
            buf.write('\"' + name + '\":[')
            for i in range(len(values)):
                if i > 0:
                    buf.write(',')
                buf.write('\"')
                buf.write(self.escapeJSON( str(values[i]) ))
                buf.write('\"')
            buf.write(']')
            self._tag.addAttribute(buf.getvalue())
            buf.close()
        elif isinstance(value, Paintable):
            idd = self.getPaintIdentifier(value)
            self.addAttribute(name, idd)
        elif isinstance(value, Resource):

            if isinstance(value, ExternalResource):
                self.addAttribute(name, value.getURL())
            elif isinstance(value, ApplicationResource):
                r = value
                a = r.getApplication()
                if a is None:
                    raise PaintException('Application not specified for resource ' \
                                         + value.getClass().getName())
                uri = a.getRelativeLocation(r)
                self.addAttribute(name, uri)
            elif isinstance(value, ThemeResource):
                uri = 'theme://' + value.getResourceId()
                self.addAttribute(name, uri)
            else:
                raise PaintException('Ajax adapter does not ' \
                                     + 'support resources of type: ' \
                                     + value.getClass().getName())
        elif isinstance(value, bool):
            self._tag.addAttribute('\"' + name + '\":' + ('true' if value else 'false'))
        elif isinstance(value, dict):
            sb = StringIO()
            sb.write('\"')
            sb.write(name)
            sb.write('\": ')
            sb.write('{')
            i = 0
            for key, mapValue in value.iteritems():
                sb.write('\"')
                if isinstance(key, Paintable):
                    paintable = key
                    sb.write(self.getPaintIdentifier(paintable))
                else:
                    sb.write(self.escapeJSON(str(key)))
                sb.write('\":')
                if isinstance(mapValue, float) \
                        or isinstance(mapValue, int) \
                        or isinstance(mapValue, float) \
                        or isinstance(mapValue, bool) \
                        or isinstance(mapValue, Alignment):
                    sb.write(mapValue)
                else:
                    sb.write('\"')
                    sb.write(self.escapeJSON(str(mapValue)))
                    sb.write('\"')
                if i < len(value) - 1:
                    sb.append(',')
                i += 1
            sb.write('}')
            self._tag.addAttribute(sb.getvalue())
            sb.close()
        elif isinstance(value, str):
            # In case of null data output nothing:
            if (value is None) or (name is None):
                raise ValueError, 'Parameters must be non-null strings'

            self._tag.addAttribute('\"' + name + '\": \"' + self.escapeJSON(value) + '\"')

            if self._customLayoutArgumentsOpen and 'template' == name:
                self.getUsedResources().add('layouts/' + value + '.html')

            if name == 'locale':
                self._manager.requireLocale(value)
        else:
            self._tag.addAttribute('\"' + name + '\":' + str(value))


    def addVariable(self, owner, name, value):
        if isinstance(value, Paintable):
            self._tag.addVariable( StringVariable(owner, name, self.getPaintIdentifier(value)) )
        elif isinstance(value, StreamVariable):
            url = self._manager.getStreamVariableTargetUrl(owner, name, value)
            if url is not None:
                self.addVariable(owner, name, url)
            # else { //NOP this was just a cleanup by component }
        elif isinstance(value, bool):
            self._tag.addVariable( BooleanVariable(owner, name, value) )
        elif isinstance(value, float):
            self._tag.addVariable( DoubleVariable(owner, name, value) )
#        elif isinstance(value, float):
#            self._tag.addVariable( FloatVariable(owner, name, value) )
        elif isinstance(value, int):
            self._tag.addVariable( IntVariable(owner, name, value) )
        elif isinstance(value, long):
            self._tag.addVariable( LongVariable(owner, name, value) )
        elif isinstance(value, str):
            self._tag.addVariable( StringVariable(owner, name, self.escapeJSON(value)) )
        else:  # list
            self._tag.addVariable( ArrayVariable(owner, name, value) )


    def addUploadStreamVariable(self, owner, name):
        """Adds a upload stream type variable.

        TODO not converted for JSON

        @param owner
                   the Listener for variable changes.
        @param name
                   the Variable name.

        @throws PaintException
                    if the paint operation failed.
        """
        self.startTag('uploadstream')
        self.addAttribute(self._UIDL_ARG_NAME, name)
        self.endTag('uploadstream')


    def addSection(self, sectionTagName, sectionData):
        """Prints the single text section.

        Prints full text section. The section data is escaped

        @param sectionTagName
                   the name of the tag.
        @param sectionData
                   the section data to be printed.
        @throws PaintException
                    if the paint operation failed.
        """
        self._tag.addData('{\"' + sectionTagName + '\":\"' \
                + self.escapeJSON(sectionData) + '\"}')


    def addUIDL(self, xml):
        """Adds XML directly to UIDL.

        @param xml
                   the Xml to be added.
        @throws PaintException
                    if the paint operation failed.
        """
        # Ensure that the target is open
        if self._closed:
            raise PaintException('Attempted to write to a closed PaintTarget.')

        # Make sure that the open start tag is closed before
        # anything is written.

        # Escape and write what was given
        if xml is not None:
            self._tag.addData('\"' + self.escapeJSON(xml) + '\"')


    def addXMLSection(self, sectionTagName, sectionData, namespace):
        """Adds XML section with namespace.

        @param sectionTagName
                   the name of the tag.
        @param sectionData
                   the section data.
        @param namespace
                   the namespace to be added.
        @throws PaintException
                    if the paint operation failed.

        @see com.vaadin.terminal.PaintTarget#addXMLSection(String, String,
             String)
        """
        # Ensure that the target is open
        if self._closed:
            raise PaintException('Attempted to write to a closed PaintTarget.')

        self.startTag(sectionTagName)

        if namespace is not None:
            self.addAttribute('xmlns', namespace)

        if sectionData is not None:
            self._tag.addData('\"' + self.escapeJSON(sectionData) + '\"')

        self.endTag(sectionTagName)


    def getUIDL(self):
        """Gets the UIDL already printed to stream. Paint target must be closed
        before the <code>getUIDL</code> can be called.

        @return the UIDL.
        """
        if self._closed:
            return self._uidlBuffer.getvalue()

        raise ValueError, 'Tried to read UIDL from open PaintTarget'


    def close(self):
        """Closes the paint target. Paint target must be closed before the
        <code>getUIDL</code> can be called. Subsequent attempts to write to paint
        target. If the target was already closed, call to this function is
        ignored. will generate an exception.

        @throws PaintException
                    if the paint operation failed.
        """
        if self._tag is not None:
            self._uidlBuffer.write(self._tag.getJSON())
        self._flush()
        self._closed = True


    def _flush(self):
        """Method flush."""
        self._uidlBuffer.flush()


    def paintReference(self, paintable, referenceName):
        raise DeprecationWarning
        self.addAttribute(referenceName, paintable)


    def getPaintIdentifier(self, paintable):
        if not self._manager.hasPaintableId(paintable):
            if self._identifiersCreatedDueRefPaint is None:
                self._identifiersCreatedDueRefPaint = set()
            self._identifiersCreatedDueRefPaint.add(paintable)

        return self._manager.getPaintableId(paintable)


    def addCharacterData(self, text):
        if text is not None:
            self._tag.addData(text)


    def getUsedResources(self):
        return self._usedResources


    def needsToBePainted(self, p):
        """Method to check if paintable is already painted into this target.

        @param p
        @return true if is not yet painted into this target and is connected to
                app
        """
        if self._paintedComponents.contains(p):
            return False
        elif p.getApplication() is None:
            return False
        else:
            return True

    _widgetMappingCache = dict()

    def getTag(self, paintable):
        class1 = self._widgetMappingCache[paintable.getClass()]

        if class1 is None:
            # Client widget annotation is searched from component hierarchy to
            # detect the component that presumably has client side
            # implementation. The server side name is used in the
            # transportation, but encoded into integer strings to optimized
            # transferred data.
            class1 = paintable.__class__
            while not self.hasClientWidgetMapping(class1):
                superclass = class1.mro()[1] if len(class1.mro()) > 1 else None
                if superclass is not None and Paintable in superclass.mro():  # FIXME: check isAssignableFrom translation
                    class1 = superclass
                else:
                    self._logger.warning('No superclass of ' \
                            + paintable.getClass().getName() \
                            + ' has a @ClientWidget' \
                            + ' annotation. Component will not be mapped correctly on client side.')
                    break

            self._widgetMappingCache[paintable.getClass()] = class1

        self._usedPaintableTypes.append(class1)
        return self._manager.getTagForType(class1)


    def hasClientWidgetMapping(self, class1):
        try:
            return class1.isAnnotationPresent(self.ClientWidget)
        except RuntimeError, e:
            self._logger.critical('An error occurred while finding widget mapping.')
            return False


    def getUsedPaintableTypes(self):
        return self._usedPaintableTypes


class JsonTag(object):
    """This is basically a container for UI components variables, that will be
    added at the end of JSON object.

    @author mattitahvonen
    """

    def __init__(self, tagName):

        self._firstField = False
        self._variables = list()
        self._children = list()
        self._attr = list()
        self._data = StringIO()
        self.childrenArrayOpen = False
        self._childNode = False
        self._tagClosed = False

        self._data.append('[\"' + tagName + '\"')


    def _closeTag(self):
        if not self._tagClosed:
            self._data.write(self._attributesAsJsonObject())
            self._data.write(self.getData())
            # Writes the end (closing) tag
            self._data.write(']')
            self._tagClosed = True


    def getJSON(self):
        if not self._tagClosed:
            self._closeTag()
        return self._data.getvalue()


    def openChildrenArray(self):
        if not self.childrenArrayOpen:
            # append("c : [");
            self.childrenArrayOpen = True
            # firstField = true;


    def closeChildrenArray(self):
        # append("]");
        # firstField = false;
        pass


    def setChildNode(self, b):
        self._childNode = b


    def isChildNode(self):
        return self._childNode


    def startField(self):
        if self._firstField:
            self._firstField = False
            return ''
        else:
            return ','


    def addData(self, s):
        """@param s
                   json string, object or array
        """
        self._children.append(s)


    def getData(self):
        buf = StringIO()
        for c in self._children:
            buf.append(self.startField())
            buf.append(c)
        result = buf.getvalue()
        buf.close()
        return result


    def addAttribute(self, jsonNode):
        self._attr.append(jsonNode)


    def _attributesAsJsonObject(self):
        buf = StringIO()
        buf.write(self.startField())
        buf.write('{')
        i = 0
        for element in self._attr:
            buf.write(element)
            if i != len(self._attr) - 1:
                buf.write(',')
            i += 1
        buf.write(self.tag._variablesAsJsonObject())
        buf.write('}')
        result = buf.getvalue()
        buf.close()
        return result


    def addVariable(self, v):
        self._variables.append(v)


    def _variablesAsJsonObject(self):
        if len(self._variables) == 0:
            return ''

        buf = StringIO()
        buf.write(self.startField())
        buf.write('\"v\":{')
        i = 0
        for element in self._variables:
            buf.write(element.getJsonPresentation())
            if i != len(self._variables) - 1:
                buf.write(',')
            i += 1
        buf.write('}')
        result = buf.getvalue()
        buf.close()
        return result


class Variable(object):

    def getJsonPresentation(self):
        pass


class BooleanVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name


    def getJsonPresentation(self):
        return '\"' + self.name + '\":' \
            + ('true' if self._value == True else 'false')


class StringVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name


    def getJsonPresentation(self):
        return '\"' + self.name + '\":\"' + self._value + '\"'


class IntVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name


    def getJsonPresentation(self):
        return '\"' + self.name + '\":' + self._value


class LongVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name


    def getJsonPresentation(self):
        return '\"' + self.name + '\":' + self._value


class FloatVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name


    def getJsonPresentation(self):
        return '\"' + self.name + '\":' + self._value


class DoubleVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name


    def getJsonPresentation(self):
        return '\"' + self.name + '\":' + self._value


class ArrayVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name


    def getJsonPresentation(self):
        sb = StringIO()
        sb.write('\"')
        sb.write(self.name)
        sb.write('\":[')
        for i in range(len(self._value)):
            sb.write('\"')
            sb.write( self.escapeJSON(self._value[i]) )
            sb.write('\"')
            if i < len(self._value) - 1:
                sb.write(',')
        sb.write(']')
        result = sb.getvalue()
        sb.close()
        return result
