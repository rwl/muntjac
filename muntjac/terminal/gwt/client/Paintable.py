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



class Paintable(object):
    """An interface used by client-side widgets or paintable parts to receive
    updates from the corresponding server-side components in the form of
    {@link UIDL}.

    Updates can be sent back to the server using the
    {@link ApplicationConnection#updateVariable()} methods.
    """

    def updateFromUIDL(self, uidl, client):
        pass
