# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.ui.component import IComponent


class IDragSource(IComponent):
    """IDragSource is a {@link IComponent} that builds a {@link Transferable} for a
    drag and drop operation.
    <p>
    In Vaadin the drag and drop operation practically starts from client side
    component. The client side component initially defines the data that will be
    present in {@link Transferable} object on server side. If the server side
    counterpart of the component implements this interface, terminal
    implementation lets it create the {@link Transferable} instance from the raw
    client side "seed data". This way server side implementation may translate or
    extend the data that will be available for {@link DropHandler}.

    @since 6.3
    """

    def getTransferable(self, rawVariables):
        """IDragSource may convert data added by client side component to meaningful
        values for server side developer or add other data based on it.

        <p>
        For example Tree converts item identifiers to generated string keys for
        the client side. Vaadin developer don't and can't know anything about
        these generated keys, only about item identifiers. When tree node is
        dragged client puts that key to {@link Transferable}s client side
        counterpart. In {@link Tree#getTransferable(Map)} the key is converted
        back to item identifier that the server side developer can use.
        <p>

        @since 6.3
        @param rawVariables
                   the data that client side initially included in
                   {@link Transferable}s client side counterpart.
        @return the {@link Transferable} instance that will be passed to
                {@link DropHandler} (and/or {@link AcceptCriterion})
        """
        raise NotImplementedError
