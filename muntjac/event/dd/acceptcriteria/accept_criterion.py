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

"""Criterion that can be used create policy to accept/discard dragged
content."""


class IAcceptCriterion(object):
    """Criterion that can be used create policy to accept/discard dragged
    content (presented by L{Transferable}).

    The drag and drop mechanism will verify the criteria returned by
    L{DropHandler.getAcceptCriterion} before calling L{DropHandler.drop}.

    The criteria can be evaluated either on the client (browser - see
    L{ClientSideCriterion}) or on the server (see L{ServerSideCriterion}).
    If no constraints are needed, an L{AcceptAll} can be used.

    In addition to accepting or rejecting a possible drop, criteria can provide
    additional hints for client side painting.

    @see: L{DropHandler}
    @see: L{ClientSideCriterion}
    @see: L{ServerSideCriterion}
    """

    def isClientSideVerifiable(self):
        """Returns whether the criteria can be checked on the client or whether
        a server request is needed to check the criteria.

        This requirement may depend on the state of the criterion (e.g. logical
        operations between criteria), so this cannot be based on a marker
        interface.
        """
        raise NotImplementedError


    def paint(self, target):
        raise NotImplementedError


    def paintResponse(self, target):
        """This needs to be implemented iff criterion does some lazy server
        side initialization. The UIDL painted in this method will be passed to
        client side drop handler implementation. Implementation can assume that
        L{accept} is called before this method.
        """
        raise NotImplementedError


    def accept(self, dragEvent):
        """Validates the data in event to be appropriate for the
        L{DropHandler.drop} method.

        Note that even if your criterion is validated on client side, you
        should always validate the data on server side too.
        """
        raise NotImplementedError
