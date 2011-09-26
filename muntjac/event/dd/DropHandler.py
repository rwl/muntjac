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


class DropHandler(object):
    """DropHandlers contain the actual business logic for drag and drop operations.
    <p>
    The {@link #drop(DragAndDropEvent)} method is used to receive the transferred
    data and the {@link #getAcceptCriterion()} method contains the (possibly
    client side verifiable) criterion whether the dragged data will be handled at
    all.

    @since 6.3
    """

    def drop(self, event):
        """Drop method is called when the end user has finished the drag operation
        on a {@link DropTarget} and {@link DragAndDropEvent} has passed
        {@link AcceptCriterion} defined by {@link #getAcceptCriterion()} method.
        The actual business logic of drag and drop operation is implemented into
        this method.

        @param event
                   the event related to this drop
        """
        pass


    def getAcceptCriterion(self):
        """Returns the {@link AcceptCriterion} used to evaluate whether the
        {@link Transferable} will be handed over to
        {@link DropHandler#drop(DragAndDropEvent)} method. If client side can't
        verify the {@link AcceptCriterion}, the same criteria may be tested also
        prior to actual drop - during the drag operation.
        <p>
        Based on information from {@link AcceptCriterion} components may display
        some hints for the end user whether the drop will be accepted or not.
        <p>
        Vaadin contains a variety of criteria built in that can be composed to
        more complex criterion. If the build in criteria are not enough,
        developer can use a {@link ServerSideCriterion} or build own custom
        criterion with client side counterpart.
        <p>
        If developer wants to handle everything in the
        {@link #drop(DragAndDropEvent)} method, {@link AcceptAll} instance can be
        returned.

        @return the {@link AcceptCriterion}
        """
        pass
