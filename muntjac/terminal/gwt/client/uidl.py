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


class UIDL(JavaScriptObject):
    """When a component is updated, it's client side widget's
    L{Paintable.updateFromUIDL} will be called with the updated ("changes")
    UIDL received from the server.

    UIDL is hierarchical, and there are a few methods to retrieve the children,
    L{getChildCount}, L{getChildIterator}, L{getChildString}, L{getChildUIDL}.

    It can be helpful to keep in mind that UIDL was originally modeled in XML,
    so it's structure is very XML -like. For instance, the first to children in
    the underlying UIDL representation will contain the "tag" name and
    attributes, but will be skipped by the methods mentioned above.
    """

    _CHILD_TYPE_STRING = 0
    _CHILD_TYPE_UIDL = 1
    _CHILD_TYPE_XML = 2

    def __init__(self):
        pass


    def getId(self):
        """Shorthand for getting the attribute named "id", which for Paintables
        is the essential paintableId which binds the server side component to
        the client side widget.

        @return: the value of the id attribute, if available
        """
        return self.getStringAttribute('id')


    def getTag(self):
        """Gets the name of this UIDL section, as created with
        L{PaintTarget.startTag} in the server-side L{Componentpaint} or
        (usually) L{AbstractComponent.paintContent}. Note that if the UIDL
        corresponds to a Paintable, a component identifier will be returned
        instead - this is used internally and is not needed within
        L{Paintable.updateFromUIDL}.

        @return: the name for this section
        """
        JS("""
            return @{{self}}[0];
        """)
        pass


    def attr(self):
        JS("""
            return @{{self}}[1];
        """)
        pass


    def var(self):
        JS("""
            return @{{self}}[1]["v"];
        """)
        pass


    def hasVariables(self):
        JS("""
            return Boolean(@{{self}}[1]["v"]);
        """)
        pass


    def getStringAttribute(self, name):
        """Gets the named attribute as a String.

        @param name:
                   the name of the attribute to get
        @return: the attribute value
        """
        return self.attr().getString(name)


    def getAttributeNames(self):
        """Gets the names of the attributes available.

        @return: the names of available attributes
        """
        keySet = self.attr().getKeySet()
        keySet.remove('v')
        return keySet


    def getVariableNames(self):
        """Gets the names of variables available.

        @return the names of available variables
        """
        if not self.hasVariables():
            return set()
        else:
            keySet = self.var().getKeySet()
            return keySet


    def getIntAttribute(self, name):
        """Gets the named attribute as an int.

        @param name:
                   the name of the attribute to get
        @return: the attribute value
        """
        return self.attr().getInt(name)


    def getLongAttribute(self, name):
        """Gets the named attribute as a long.

        @param name:
                   the name of the attribute to get
        @return: the attribute value
        """
        return self.attr().getRawNumber(name)


    def getFloatAttribute(self, name):
        """Gets the named attribute as a float.

        @param name:
                   the name of the attribute to get
        @return: the attribute value
        """
        return self.attr().getRawNumber(name)


    def getDoubleAttribute(self, name):
        """Gets the named attribute as a double.

        @param name:
                   the name of the attribute to get
        @return: the attribute value
        """
        return self.attr().getRawNumber(name)


    def getBooleanAttribute(self, name):
        """Gets the named attribute as a boolean.

        @param name:
                   the name of the attribute to get
        @return: the attribute value
        """
        return self.attr().getBoolean(name)


    def getMapAttribute(self, name):
        """Gets the named attribute as a Map of named values
        (key/value pairs).

        @param name:
                   the name of the attribute to get
        @return: the attribute Map
        """
        return self.attr().getValueMap(name)


    def getStringArrayAttribute(self, name):
        """Gets the named attribute as an array of Strings.

        @param name:
                   the name of the attribute to get
        @return: the attribute value
        """
        return self.attr().getStringArray(name)


    def getIntArrayAttribute(self, name):
        """Gets the named attribute as an int array.

        @param name:
                   the name of the attribute to get
        @return: the attribute value
        """
        return self.attr().getIntArray(name)


    def getAttribute(self, name):
        """Get attributes value as string whatever the type is

        @param name:
        @return: string presentation of attribute
        """
        JS("""
            return '' + @{{self}}[1][@{{name}}];
        """)
        pass


    def getVariable(self, name):
        JS("""
            return '' + @{{self}}[1]['v'][@{{name}}];
        """)
        pass


    def hasAttribute(self, name):
        """Indicates whether or not the named attribute is available.

        @param name:
                   the name of the attribute to check
        @return: true if the attribute is available, false otherwise
        """
        return name in self.attr()


    def getChildUIDL(self, i):
        """Gets the UIDL for the child at the given index.

        @param i:
                   the index of the child to get
        @return: the UIDL of the child if it exists
        """
        JS("""
            return @{{self}}[@{{i}} + 2];
        """)
        pass


    def getChildString(self, i):
        """Gets the child at the given index as a String.

        @param i:
                   the index of the child to get
        @return: the String representation of the child if it exists
        """
        JS("""
            return @{{self}}[@{{i}} + 2];
        """)
        pass


    def getChildXML(self, index):
        JS("""
            return @{{self}}[@{{index}} + 2];
        """)
        pass


    def getChildIterator(self):
        """Gets an iterator that can be used to iterate trough the children of
        this UIDL.

        The Object returned by <code>next()</code> will be appropriately typed -
        if it's UIDL, L{getTag} can be used to check which section is in
        question.

        The basic use case is to iterate over the children of an UIDL update,
        and update the appropriate part of the widget for each child
        encountered, e.g if C{getTag()} returns "color", one would update the
        widgets color to reflect the value of the "color" section.

        @return: an iterator for iterating over UIDL children
        """

        class ChildIterator(Iterator):

            def __init__(self, uidl):
                self._index = -1
                self._uidl = uidl


            def remove(self):
                raise NotImplementedError


            def next(self):
                if self.hasNext():
                    self._index += 1
                    typeOfChild = self._uidl.typeOfChild(self._index)

                    if typeOfChild == self._uidl._CHILD_TYPE_UIDL:
                        childUIDL = self._uidl.getChildUIDL(self._index)
                        return childUIDL
                    elif typeOfChild == self._uidl._CHILD_TYPE_STRING:
                        return self._uidl.getChildString(self._index)
                    elif typeOfChild == self._uidl._CHILD_TYPE_XML:
                        return self._uidl.getChildXML(self._index)
                    else:
                        raise ValueError('Illegal child  in tag '
                            + self._uidl.getTag() + ' at index ' + self._index)
                return None


            def hasNext(self):
                count = self._uidl.getChildCount()
                return count > self._index + 1

        return ChildIterator(self)


    def typeOfChild(self, index):
        JS("""
            var t = typeof @{{self}}[@{{index}} + 2];
            if(t == "object") {
                if(typeof(t.length) == "number") {
                    return 1;
                } else {
                    return 2;
                }
            } else if (t == "string") {
                return 0;
            }
            return -1;
        """)
        pass


    def getChildrenAsXML(self):
        """@deprecated:"""
        return str(self)


    def hasVariable(self, name):
        """Checks if the named variable is available.

        @param name:
                   the name of the variable desired
        @return: true if the variable exists, false otherwise
        """
        return self.hasVariables() and name in self.var()


    def getStringVariable(self, name):
        """Gets the value of the named variable.

        @param name:
                   the name of the variable
        @return: the value of the variable
        """
        return self.var().getString(name)


    def getIntVariable(self, name):
        """Gets the value of the named variable.

        @param name:
                   the name of the variable
        @return: the value of the variable
        """
        return self.var().getInt(name)


    def getLongVariable(self, name):
        """Gets the value of the named variable.

        @param name:
                   the name of the variable
        @return: the value of the variable
        """
        return self.var().getRawNumber(name)


    def getFloatVariable(self, name):
        """Gets the value of the named variable.

        @param name:
                   the name of the variable
        @return: the value of the variable
        """
        return self.var().getRawNumber(name)


    def getDoubleVariable(self, name):
        """Gets the value of the named variable.

        @param name:
                   the name of the variable
        @return: the value of the variable
        """
        return self.var().getRawNumber(name)


    def getBooleanVariable(self, name):
        """Gets the value of the named variable.

        @param name:
                   the name of the variable
        @return: the value of the variable
        """
        return self.var().getBoolean(name)


    def getStringArrayVariable(self, name):
        """Gets the value of the named variable.

        @param name:
                   the name of the variable
        @return: the value of the variable
        """
        return self.var().getStringArray(name)


    def getStringArrayVariableAsSet(self, name):
        """Gets the value of the named String[] variable as a Set of Strings.

        @param name
                   the name of the variable
        @return the value of the variable
        """
        s = set()
        a = self.var().getJSStringArray(name)
        for i in range(len(a)):
            s.add(a.get(i))
        return s


    def getIntArrayVariable(self, name):
        """Gets the value of the named variable.

        @param name:
                   the name of the variable
        @return: the value of the variable
        """
        return self.var().getIntArray(name)


    class XML(JavaScriptObject):
        """@deprecated: should not be used anymore"""

        def __init__(self):
            pass

        def getXMLAsString(self):
            JS("""
                var buf = new Array();
                var self = @{{self}};
                for(j in self) {
                    buf.push("<");
                    buf.push(j);
                    buf.push(">");
                    buf.push(self[j]);
                    buf.push("</");
                    buf.push(j);
                    buf.push(">");
                }
                return buf.join("");
            """)
            pass


    def getChildCount(self):
        """Returns the number of children.

        @return: the number of children
        """
        JS("""
            return @{{self}}.length - 2;
        """)
        pass


    def getErrors(self):
        """Shorthand that returns the component errors as UIDL. Only
        applicable for Paintables.

        @return: the error UIDL if available
        """
        JS("""
            return @{{self}}[1]['error'];
        """)
        pass


    def isMapAttribute(self, name):
        JS("""
            return typeof @{{self}}[1][@{{name}}] == "object";
        """)
        pass


    def getPaintableAttribute(self, name, connection):
        """Gets the Paintable with the id found in the named attributes's
        value.

        @param name:
                   the name of the attribute
        @return: the Paintable referenced by the attribute, if it exists
        """
        return connection.getPaintable(self.getStringAttribute(name))


    def getPaintableVariable(self, name, connection):
        """Gets the Paintable with the id found in the named variable's value.

        @param name:
                   the name of the variable
        @return: the Paintable referenced by the variable, if it exists
        """
        return connection.getPaintable(self.getStringVariable(name))


    def getChildByTagName(self, tagName):
        """Returns the child UIDL by its name. If several child nodes exist
        with the given name, the first child UIDL will be returned.

        @return: the child UIDL or null if child wit given name was not found
        """
        for childUIDL in self.getChildIterator():
            if isinstance(childUIDL, UIDL):
                if childUIDL.getTag() == tagName:
                    return childUIDL
        return None
