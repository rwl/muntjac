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


class ISubPartAware(object):
    """Interface implemented by {@link Widget}s which can provide identifiers
    for at least one element inside the component. Used by L{ComponentLocator}.
    """

    def getSubPartElement(self, subPart):
        """Locates an element inside a component using the identifier provided
        in C{subPart}. The C{subPart} identifier is component specific and may
        be any string of characters, numbers, space characters and brackets.

        @param subPart:
                   The identifier for the element inside the component
        @return: The element identified by subPart or null if the element could
                 not be found.
        """
        raise NotImplementedError


    def getSubPartName(self, subElement):
        """Provides an identifier that identifies the element within the
        component. The {@code subElement} is a part of the component and must
        never be null.

        B{Note!}
        C{getSubPartElement(getSubPartName(element)) == element} is I{not
        always} true. A component can choose to provide a more generic
        identifier for any given element if the results of all interactions
        with C{subElement} are the same as interactions with the element
        identified by the return value. For example a button can return an
        identifier for the root element even though a DIV inside the button was
        passed as C{subElement} because interactions with the DIV and the
        root button element produce the same result.

        @param subElement:
                   The element the identifier string should uniquely identify
        @return: An identifier that uniquely identifies C{subElement} or null
                 if no identifier could be provided.
        """
        raise NotImplementedError
