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

"""Parent class for criteria which are verified on the server side."""

from muntjac.event.dd.acceptcriteria.accept_criterion import IAcceptCriterion


class ServerSideCriterion(IAcceptCriterion):
    """Parent class for criteria which are verified on the server side
    during a drag operation to accept/discard dragged content (presented
    by L{Transferable}).

    Subclasses should implement the L{IAcceptCriterion.accept} method.

    As all server side state can be used to make a decision, this is more
    flexible than L{ClientSideCriterion}. However, this does require
    additional requests from the browser to the server during a drag operation.

    @see: IAcceptCriterion
    @see: ClientSideCriterion
    """

    def isClientSideVerifiable(self):
        return False


    def paint(self, target):
        target.startTag('-ac')
        target.addAttribute('name', self.getIdentifier())
        self.paintContent(target)
        target.endTag('-ac')


    def paintContent(self, target):
        pass


    def paintResponse(self, target):
        pass


    def getIdentifier(self):
        #return clsname(ServerSideCriterion)  # FIXME: Python client side
        return 'com.vaadin.event.dd.acceptcriteria.ServerSideCriterion'
