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

# from com.google.gwt.user.client.ui.AbstractImagePrototype import (AbstractImagePrototype,)


class TreeImages(com.google.gwt.user.client.ui.TreeImages):

    def treeOpen(self):
        """An image indicating an open branch.

        @return a prototype of this image
        @gwt.resource com/vaadin/terminal/gwt/public/default/tree/img/expanded
                      .png
        """
        pass

    def treeClosed(self):
        """An image indicating a closed branch.

        @return a prototype of this image
        @gwt.resource com/vaadin/terminal/gwt/public/default/tree/img/collapsed
                      .png
        """
        pass
