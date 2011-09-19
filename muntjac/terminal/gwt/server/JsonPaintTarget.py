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
from com.vaadin.terminal.Paintable import (Paintable,)
from com.vaadin.terminal.PaintTarget import (PaintTarget,)
from com.vaadin.terminal.PaintException import (PaintException,)
# from java.io.BufferedReader import (BufferedReader,)
# from java.io.File import (File,)
# from java.io.IOException import (IOException,)
# from java.io.InputStream import (InputStream,)
# from java.io.InputStreamReader import (InputStreamReader,)
# from java.io.PrintWriter import (PrintWriter,)
# from java.io.Serializable import (Serializable,)
# from java.util.Collection import (Collection,)
# from java.util.HashMap import (HashMap,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.Map import (Map,)
# from java.util.Set import (Set,)
# from java.util.Stack import (Stack,)
# from java.util.Vector import (Vector,)
# from java.util.logging.Level import (Level,)
# from java.util.logging.Logger import (Logger,)
try:
    from cStringIO import (StringIO,)
except ImportError, e:
    from StringIO import (StringIO,)


class JsonPaintTarget(PaintTarget):
    """User Interface Description Language Target.

    TODO document better: role of this class, UIDL format, attributes, variables,
    etc.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 5.0
    """
    _logger = Logger.getLogger(JsonPaintTarget.getName())
    # Document type declarations
    _UIDL_ARG_NAME = 'name'
    _mOpenTags = None
    _openJsonTags = None
    _uidlBuffer = None
    _closed = False
    _manager = None
    _changes = 0
    _usedResources = set()
    _customLayoutArgumentsOpen = False
    _tag = None
    _errorsOpen = None
    _cacheEnabled = False
    _paintedComponents = set()
    _identifiersCreatedDueRefPaint = None
    _usedPaintableTypes = LinkedList()

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
        self._mOpenTags = Stack()
        self._openJsonTags = Stack()
        self._cacheEnabled = cachingRequired

    def startTag(self, *args):
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
        _0 = args
        _1 = len(args)
        if _1 == 1:
            tagName, = _0
            self.startTag(tagName, False)
        elif _1 == 2:
            if isinstance(_0[0], Paintable):
                paintable, tagName = _0
                self.startTag(tagName, True)
                isPreviouslyPainted = self._manager.hasPaintableId(paintable) and (self._identifiersCreatedDueRefPaint is None) or (not self._identifiersCreatedDueRefPaint.contains(paintable))
                id = self._manager.getPaintableId(paintable)
                paintable.addListener(self._manager)
                self.addAttribute('id', id)
                self._paintedComponents.add(paintable)
                if isinstance(paintable, CustomLayout):
                    self._customLayoutArgumentsOpen = True
                return self._cacheEnabled and isPreviouslyPainted
            else:
                tagName, isChildNode = _0
                if tagName is None:
                    raise self.NullPointerException()
                # Ensures that the target is open
                if self._closed:
                    raise PaintException('Attempted to write to a closed PaintTarget.')
                if self._tag is not None:
                    self._openJsonTags.push(self._tag)
                # Checks tagName and attributes here
                self._mOpenTags.push(tagName)
                self._tag = self.JsonTag(tagName)
                if 'error' == tagName:
                    self._errorsOpen += 1
                self._customLayoutArgumentsOpen = False
        else:
            raise ARGERROR(1, 2)

    # In case of null data output nothing:

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
            raise self.NullPointerException()
        # Ensure that the target is open
        if self._closed:
            raise PaintException('Attempted to write to a closed PaintTarget.')
        if len(self._openJsonTags) > 0:
            parent = self._openJsonTags.pop()
            lastTag = ''
            lastTag = self._mOpenTags.pop()
            if not tagName.equalsIgnoreCase(lastTag):
                raise PaintException('Invalid UIDL: wrong ending tag: \'' + tagName + '\' expected: \'' + lastTag + '\'.')
            # simple hack which writes error uidl structure into attribute
            if 'error' == lastTag:
                if self._errorsOpen == 1:
                    parent.addAttribute('\"error\":[\"error\",{}' + self._tag.getData() + ']')
                else:
                    # sub error
                    parent.addData(self._tag.getJSON())
                self._errorsOpen -= 1
            else:
                parent.addData(self._tag.getJSON())
            self._tag = parent
        else:
            self._changes += 1
            self._uidlBuffer.print_((',' if self._changes > 1 else '') + self._tag.getJSON())
            self._tag = None

    @classmethod
    def escapeXML(cls, *args):
        """Substitutes the XML sensitive characters with predefined XML entities.

        @param xml
                   the String to be substituted.
        @return A new string instance where all occurrences of XML sensitive
                characters are substituted with entities.
        ---
        Substitutes the XML sensitive characters with predefined XML entities.

        @param xml
                   the String to be substituted.
        @return A new StringBuilder instance where all occurrences of XML
                sensitive characters are substituted with entities.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], StringBuilder):
                xml, = _0
                if (xml is None) or (len(xml) <= 0):
                    return cls.StringBuilder('')
                result = cls.StringBuilder(len(xml) * 2)
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(xml)):
                        break
                    c = xml[i]
                    s = cls.toXmlChar(c)
                    if s is not None:
                        result.append(s)
                    else:
                        result.append(c)
                return result
            else:
                xml, = _0
                if (xml is None) or (len(xml) <= 0):
                    return ''
                return str(cls.escapeXML(cls.StringBuilder(xml)))
        else:
            raise ARGERROR(1, 1)

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
        sb = cls.StringBuilder()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(s)):
                break
            ch = s[i]
            _1 = ch
            _2 = False
            while True:
                if _1 == '"':
                    _2 = True
                    sb.append('\\\"')
                    break
                if (_2 is True) or (_1 == '\\'):
                    _2 = True
                    sb.append('\\\\')
                    break
                if (_2 is True) or (_1 == '\b'):
                    _2 = True
                    sb.append('\\b')
                    break
                if (_2 is True) or (_1 == '\f'):
                    _2 = True
                    sb.append('\\f')
                    break
                if (_2 is True) or (_1 == '\n'):
                    _2 = True
                    sb.append('\\n')
                    break
                if (_2 is True) or (_1 == '\r'):
                    _2 = True
                    sb.append('\\r')
                    break
                if (_2 is True) or (_1 == '\t'):
                    _2 = True
                    sb.append('\\t')
                    break
                if (_2 is True) or (_1 == '/'):
                    _2 = True
                    sb.append('\\/')
                    break
                if True:
                    _2 = True
                    if ch >= '\u0000' and ch <= '\u001F':
                        ss = Integer.toHexString.toHexString(ch)
                        sb.append('\\u')
                        _3 = True
                        k = 0
                        while True:
                            if _3 is True:
                                _3 = False
                            else:
                                k += 1
                            if not (k < 4 - len(ss)):
                                break
                            sb.append('0')
                        sb.append(ss.toUpperCase())
                    else:
                        sb.append(ch)
                break
        return str(sb)

    @classmethod
    def toXmlChar(cls, c):
        """Substitutes a XML sensitive character with predefined XML entity.

        @param c
                   the Character to be replaced with an entity.
        @return String of the entity or null if character is not to be replaced
                with an entity.
        """
        _0 = c
        _1 = False
        while True:
            if _0 == '&':
                _1 = True
                return '&amp;'
                # & => &amp;
            if (_1 is True) or (_0 == '>'):
                _1 = True
                return '&gt;'
                # > => &gt;
            if (_1 is True) or (_0 == '<'):
                _1 = True
                return '&lt;'
                # < => &lt;
            if (_1 is True) or (_0 == '"'):
                _1 = True
                return '&quot;'
                # " => &quot;
            if (_1 is True) or (_0 == '\''):
                _1 = True
                return '&apos;'
                # ' => &apos;
            if True:
                _1 = True
                return None
            break

    def addText(self, str):
        """Prints XML-escaped text.

        @param str
        @throws PaintException
                    if the paint operation failed.
        """
        self._tag.addData('\"' + self.escapeJSON(str) + '\"')

    def addAttribute(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 2:
            if isinstance(_0[1], Object):
                name, values = _0
                if (values is None) or (name is None):
                    raise self.NullPointerException('Parameters must be non-null strings')
                buf = self.StringBuilder()
                buf.append('\"' + name + '\":[')
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < values.length):
                        break
                    if i > 0:
                        buf.append(',')
                    buf.append('\"')
                    buf.append(self.escapeJSON(str(values[i])))
                    buf.append('\"')
                buf.append(']')
                self._tag.addAttribute(str(buf))
            elif isinstance(_0[1], Paintable):
                name, value = _0
                id = self.getPaintIdentifier(value)
                self.addAttribute(name, id)
            elif isinstance(_0[1], Resource):
                name, value = _0
                if isinstance(value, ExternalResource):
                    self.addAttribute(name, value.getURL())
                elif isinstance(value, ApplicationResource):
                    r = value
                    a = r.getApplication()
                    if a is None:
                        raise PaintException('Application not specified for resorce ' + value.getClass().getName())
                    uri = a.getRelativeLocation(r)
                    self.addAttribute(name, uri)
                elif isinstance(value, ThemeResource):
                    uri = 'theme://' + value.getResourceId()
                    self.addAttribute(name, uri)
                else:
                    raise PaintException('Ajax adapter does not ' + 'support resources of type: ' + value.getClass().getName())
            elif isinstance(_0[1], boolean):
                name, value = _0
                self._tag.addAttribute('\"' + name + '\":' + ('true' if value else 'false'))
            elif isinstance(_0[1], dict):
                name, value = _0
                sb = self.StringBuilder()
                sb.append('\"')
                sb.append(name)
                sb.append('\": ')
                sb.append('{')
                _0 = True
                it = value.keys()
                while True:
                    if _0 is True:
                        _0 = False
                    if not it.hasNext():
                        break
                    key = it.next()
                    mapValue = value.get(key)
                    sb.append('\"')
                    if isinstance(key, Paintable):
                        paintable = key
                        sb.append(self.getPaintIdentifier(paintable))
                    else:
                        sb.append(self.escapeJSON(str(key)))
                    sb.append('\":')
                    if (
                        (((isinstance(mapValue, float) or isinstance(mapValue, int)) or isinstance(mapValue, float)) or isinstance(mapValue, bool)) or isinstance(mapValue, Alignment)
                    ):
                        sb.append(mapValue)
                    else:
                        sb.append('\"')
                        sb.append(self.escapeJSON(str(mapValue)))
                        sb.append('\"')
                    if it.hasNext():
                        sb.append(',')
                sb.append('}')
                self._tag.addAttribute(str(sb))
            elif isinstance(_0[1], double):
                name, value = _0
                self._tag.addAttribute('\"' + name + '\":' + String.valueOf.valueOf(value))
            elif isinstance(_0[1], float):
                name, value = _0
                self._tag.addAttribute('\"' + name + '\":' + String.valueOf.valueOf(value))
            elif isinstance(_0[1], int):
                name, value = _0
                self._tag.addAttribute('\"' + name + '\":' + String.valueOf.valueOf(value))
            elif isinstance(_0[1], long):
                name, value = _0
                self._tag.addAttribute('\"' + name + '\":' + String.valueOf.valueOf(value))
            else:
                name, value = _0
                if (value is None) or (name is None):
                    raise self.NullPointerException('Parameters must be non-null strings')
                self._tag.addAttribute('\"' + name + '\": \"' + self.escapeJSON(value) + '\"')
                if self._customLayoutArgumentsOpen and 'template' == name:
                    self.getUsedResources().add('layouts/' + value + '.html')
                if name == 'locale':
                    self._manager.requireLocale(value)
        else:
            raise ARGERROR(2, 2)

    # In case of null data output nothing:
    # In case of null data output nothing:

    def addVariable(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 3:
            if isinstance(_0[2], Paintable):
                owner, name, value = _0
                self._tag.addVariable(self.StringVariable(owner, name, self.getPaintIdentifier(value)))
            elif isinstance(_0[2], StreamVariable):
                owner, name, value = _0
                url = self._manager.getStreamVariableTargetUrl(owner, name, value)
                if url is not None:
                    self.addVariable(owner, name, url)
                # else { //NOP this was just a cleanup by component }
            elif isinstance(_0[2], boolean):
                owner, name, value = _0
                self._tag.addVariable(self.BooleanVariable(owner, name, value))
            elif isinstance(_0[2], double):
                owner, name, value = _0
                self._tag.addVariable(self.DoubleVariable(owner, name, value))
            elif isinstance(_0[2], float):
                owner, name, value = _0
                self._tag.addVariable(self.FloatVariable(owner, name, value))
            elif isinstance(_0[2], int):
                owner, name, value = _0
                self._tag.addVariable(self.IntVariable(owner, name, value))
            elif isinstance(_0[2], long):
                owner, name, value = _0
                self._tag.addVariable(self.LongVariable(owner, name, value))
            else:
                owner, name, value = _0
                self._tag.addVariable(self.ArrayVariable(owner, name, value))
                owner, name, value = _0
                self._tag.addVariable(self.StringVariable(owner, name, self.escapeJSON(value)))
        else:
            raise ARGERROR(3, 3)

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
        self._tag.addData('{\"' + sectionTagName + '\":\"' + self.escapeJSON(sectionData) + '\"}')

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
            return str(self._uidlBuffer)
        raise self.IllegalStateException('Tried to read UIDL from open PaintTarget')

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
        self.flush()
        self._closed = True

    def flush(self):
        """Method flush."""
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.PaintTarget#startTag(com.vaadin.terminal
        # .Paintable, java.lang.String)

        self._uidlBuffer.flush()

    def paintReference(self, paintable, referenceName):
        self.addAttribute(referenceName, paintable)

    def getPaintIdentifier(self, paintable):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.PaintTarget#addCharacterData(java.lang.String )

        if not self._manager.hasPaintableId(paintable):
            if self._identifiersCreatedDueRefPaint is None:
                self._identifiersCreatedDueRefPaint = set()
            self._identifiersCreatedDueRefPaint.add(paintable)
        return self._manager.getPaintableId(paintable)

    def addCharacterData(self, text):
        if text is not None:
            self._tag.addData(text)

    class JsonTag(Serializable):
        """This is basically a container for UI components variables, that will be
        added at the end of JSON object.

        @author mattitahvonen
        """
        _firstField = False
        _variables = list()
        _children = list()
        _attr = list()
        _data = self.StringBuilder()
        childrenArrayOpen = False
        _childNode = False
        _tagClosed = False

        def __init__(self, tagName):
            self._data.append('[\"' + tagName + '\"')

        def closeTag(self):
            if not self._tagClosed:
                self._data.append(self.attributesAsJsonObject())
                self._data.append(self.getData())
                # Writes the end (closing) tag
                self._data.append(']')
                self._tagClosed = True

        def getJSON(self):
            if not self._tagClosed:
                self.closeTag()
            return str(self._data)

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
            self._children.add(s)

        def getData(self):
            buf = self.StringBuilder()
            it = self._children
            while it.hasNext():
                buf.append(self.startField())
                buf.append(it.next())
            return str(buf)

        def addAttribute(self, jsonNode):
            self._attr.add(jsonNode)

        def attributesAsJsonObject(self):
            buf = self.StringBuilder()
            buf.append(self.startField())
            buf.append('{')
            _0 = True
            iter = self._attr
            while True:
                if _0 is True:
                    _0 = False
                if not iter.hasNext():
                    break
                element = iter.next()
                buf.append(element)
                if iter.hasNext():
                    buf.append(',')
            buf.append(self.tag.variablesAsJsonObject())
            buf.append('}')
            return str(buf)

        def addVariable(self, v):
            self._variables.add(v)

        def variablesAsJsonObject(self):
            if len(self._variables) == 0:
                return ''
            buf = self.StringBuilder()
            buf.append(self.startField())
            buf.append('\"v\":{')
            iter = self._variables
            while iter.hasNext():
                element = iter.next()
                buf.append(element.getJsonPresentation())
                if iter.hasNext():
                    buf.append(',')
            buf.append('}')
            return str(buf)

    class Variable(Serializable):
        _name = None

        def getJsonPresentation(self):
            pass

    class BooleanVariable(Variable, Serializable):
        _value = None

        def __init__(self, owner, name, v):
            self._value = v
            self.name = name

        def getJsonPresentation(self):
            return '\"' + self.name + '\":' + ('true' if self._value == True else 'false')

    class StringVariable(Variable, Serializable):
        _value = None

        def __init__(self, owner, name, v):
            self._value = v
            self.name = name

        def getJsonPresentation(self):
            return '\"' + self.name + '\":\"' + self._value + '\"'

    class IntVariable(Variable, Serializable):
        _value = None

        def __init__(self, owner, name, v):
            self._value = v
            self.name = name

        def getJsonPresentation(self):
            return '\"' + self.name + '\":' + self._value

    class LongVariable(Variable, Serializable):
        _value = None

        def __init__(self, owner, name, v):
            self._value = v
            self.name = name

        def getJsonPresentation(self):
            return '\"' + self.name + '\":' + self._value

    class FloatVariable(Variable, Serializable):
        _value = None

        def __init__(self, owner, name, v):
            self._value = v
            self.name = name

        def getJsonPresentation(self):
            return '\"' + self.name + '\":' + self._value

    class DoubleVariable(Variable, Serializable):
        _value = None

        def __init__(self, owner, name, v):
            self._value = v
            self.name = name

        def getJsonPresentation(self):
            return '\"' + self.name + '\":' + self._value

    class ArrayVariable(Variable, Serializable):
        _value = None

        def __init__(self, owner, name, v):
            self._value = v
            self.name = name

        def getJsonPresentation(self):
            sb = self.StringBuilder()
            sb.append('\"')
            sb.append(self.name)
            sb.append('\":[')
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                if not (i < len(self._value)):
                    break
                sb.append('\"')
                sb.append(self.escapeJSON(self._value[i]))
                sb.append('\"')
                i += 1
                if i < len(self._value):
                    sb.append(',')
            sb.append(']')
            return str(sb)

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

            class1 = paintable.getClass()
            while not self.hasClientWidgetMapping(class1):
                superclass = class1.getSuperclass()
                if superclass is not None and Paintable.isAssignableFrom(superclass):
                    class1 = superclass
                else:
                    self._logger.warning('No superclass of ' + paintable.getClass().getName() + ' has a @ClientWidget' + ' annotation. Component will not be mapped correctly on client side.')
                    break
            self._widgetMappingCache.put(paintable.getClass(), class1)
        self._usedPaintableTypes.add(class1)
        return self._manager.getTagForType(class1)

    def hasClientWidgetMapping(self, class1):
        try:
            return class1.isAnnotationPresent(self.ClientWidget)
        except RuntimeException, e:
            if (
                e.getStackTrace()[0].getClassName() == 'org.glassfish.web.loader.WebappClassLoader'
            ):
                # Glassfish 3 is darn eager to load the value class, even
                # though we just want to check if the annotation exists.
                # See #3920, remove this hack when fixed in glassfish
                # In some situations (depending on class loading order) it
                # would be enough to return true here, but it is safer to check
                # the annotation from bytecode
                name = class1.getName().replace('.', File.separatorChar) + '.class'
                try:
                    stream = class1.getClassLoader().getResourceAsStream(name)
                    bufferedReader = StringIO(InputStreamReader(stream))
                    try:
                        atSourcefile = False
                        while line = bufferedReader.readline() is not None:
                            if line.startswith('SourceFile'):
                                atSourcefile = True
                            if atSourcefile:
                                if line.contains('ClientWidget'):
                                    return True
                            # TODO could optize to quit at the end attribute
                    except IOException, e1:
                        self._logger.log(Level.SEVERE, 'An error occurred while finding widget mapping.', e1)
                    finally:
                        try:
                            bufferedReader.close()
                        except IOException, e1:
                            self._logger.log(Level.SEVERE, 'Could not close reader.', e1)
                except Throwable, e2:
                    self._logger.log(Level.SEVERE, 'An error occurred while finding widget mapping.', e2)
                return False
            else:
                # throw exception forward
                raise e

    def getUsedPaintableTypes(self):
        return self._usedPaintableTypes
