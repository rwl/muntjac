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

from com.vaadin.terminal.gwt.client.ui.dd.VAcceptAll import (VAcceptAll,)
from com.vaadin.terminal.gwt.client.ui.dd.VDropHandler import (VDropHandler,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriteria import (VAcceptCriteria,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCallback import (VAcceptCallback,)
from com.vaadin.terminal.gwt.client.ui.dd.VDragAndDropManager import (VDragAndDropManager,)
# from java.util.Iterator import (Iterator,)


class VAbstractDropHandler(VDropHandler):
    _criterioUIDL = None
    _acceptCriteria = VAcceptAll()

    def updateAcceptRules(self, uidl):
        """Implementor/user of {@link VAbstractDropHandler} must pass the UIDL
        painted by {@link AcceptCriterion} to this method. Practically the
        details about {@link AcceptCriterion} are saved.

        @param uidl
        """
        self._criterioUIDL = uidl
        # supports updating the accept rule root directly or so that it is
        # contained in given uidl node

        if not (uidl.getTag() == '-ac'):
            childIterator = uidl.getChildIterator()
            while not (uidl.getTag() == '-ac') and childIterator.hasNext():
                uidl = childIterator.next()
        self._acceptCriteria = VAcceptCriteria.get(uidl.getStringAttribute('name'))
        if self._acceptCriteria is None:
            raise self.IllegalArgumentException('No accept criteria found with given name ' + uidl.getStringAttribute('name'))

    def dragOver(self, drag):
        """Default implementation does nothing."""
        pass

    def dragLeave(self, drag):
        """Default implementation does nothing. Implementors should clean possible
        emphasis or drag icons here.
        """
        pass

    def dragEnter(self, drag):
        """The default implementation in {@link VAbstractDropHandler} checks if the
        Transferable is accepted.
        <p>
        If transferable is accepted (either via server visit or client side
        rules) the default implementation calls abstract
        {@link #dragAccepted(VDragEvent)} method.
        <p>
        If drop handler has distinct places where some parts may accept the
        {@link Transferable} and others don't, one should use similar validation
        logic in dragOver method and replace this method with empty
        implementation.
        """

        class _0_(VAcceptCallback):

            def accepted(self, event):
                VAbstractDropHandler_this.dragAccepted(self.drag)

        _0_ = _0_()
        self.validate(_0_, drag)

    def dragAccepted(self, drag):
        """This method is called when a valid drop location was found with
        {@link AcceptCriterion} either via client or server side check.
        <p>
        Implementations can set some hints for users here to highlight that the
        drag is on a valid drop location.

        @param drag
        """
        pass

    def validate(self, cb, event):

        class checkCriteria(Command):

            def execute(self):
                VAbstractDropHandler_this._acceptCriteria.accept(self.event, VAbstractDropHandler_this._criterioUIDL, self.cb)

        VDragAndDropManager.get().executeWhenReady(checkCriteria)

    _validated = False

    def drop(self, drag):
        """The default implemmentation visits server if {@link AcceptCriterion}
        can't be verified on client or if {@link AcceptCriterion} are met on
        client.
        """
        if self._acceptCriteria.needsServerSideCheck(drag, self._criterioUIDL):
            return True
        else:
            self._validated = False

            class _2_(VAcceptCallback):

                def accepted(self, event):
                    VAbstractDropHandler_this._validated = True

            _2_ = _2_()
            self._acceptCriteria.accept(drag, self._criterioUIDL, _2_)
            return self._validated

    def getPaintable(self):
        """Returns the Paintable who owns this {@link VAbstractDropHandler}. Server
        side counterpart of the Paintable is expected to implement
        {@link DropTarget} interface.
        """
        pass
