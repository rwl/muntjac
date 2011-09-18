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

from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
# from java.util.Set import (Set,)


class Container(Paintable):

    def replaceChildComponent(self, oldComponent, newComponent):
        """Replace child of this layout with another component.

        Each layout must be able to switch children. To to this, one must just
        give references to a current and new child.

        @param oldComponent
                   Child to be replaced
        @param newComponent
                   Child that replaces the oldComponent
        """
        pass

    def hasChildComponent(self, component):
        """Is a given component child of this layout.

        @param component
                   Component to test.
        @return true iff component is a child of this layout.
        """
        pass

    def updateCaption(self, component, uidl):
        """Update child components caption, description and error message.

        <p>
        Each component is responsible for maintaining its caption, description
        and error message. In most cases components doesn't want to do that and
        those elements reside outside of the component. Because of this layouts
        must provide service for it's childen to show those elements for them.
        </p>

        @param component
                   Child component for which service is requested.
        @param uidl
                   UIDL of the child component.
        """
        pass

    def requestLayout(self, children):
        """Called when a child components size has been updated in the rendering
        phase.

        @param children
                   Set of child widgets whose size have changed
        @return true if the size of the Container remains the same, false if the
                event need to be propagated to the Containers parent
        """
        pass

    def getAllocatedSpace(self, child):
        """Returns the size currently allocated for the child component.

        @param child
        @return
        """
        pass
