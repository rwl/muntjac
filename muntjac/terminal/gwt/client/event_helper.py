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

from muntjac.terminal.gwt.client.event_id import IEventId


class EventHelper(object):
    """Helper class for attaching/detaching handlers for Muntjac client side
    components, based on identifiers in UIDL. Helpers expect Paintables to be
    both listeners and sources for events. This helper cannot be used for more
    complex widgets.

    Possible current registration is given as parameter. The returned
    registration (possibly the same as given, should be store for next update.

    Pseudocode what helpers do::

        if paintable has event listener in UIDL
             if registration is null
                     register paintable as as handler for event
             return the registration
        else
             if registration is not null
                     remove the handler from paintable
             return null
    """

    @classmethod
    def updateFocusHandler(cls, paintable, client, handlerRegistration):
        if client.hasEventListeners(paintable, IEventId.FOCUS):
            if handlerRegistration is None:
                handlerRegistration = paintable.addFocusHandler(paintable)
            return handlerRegistration
        elif handlerRegistration is not None:
            handlerRegistration.removeHandler()
            handlerRegistration = None
        return None


    @classmethod
    def updateBlurHandler(cls, paintable, client, handlerRegistration):
        if client.hasEventListeners(paintable, IEventId.BLUR):
            if handlerRegistration is None:
                handlerRegistration = paintable.addBlurHandler(paintable)
            return handlerRegistration
        elif handlerRegistration is not None:
            handlerRegistration.removeHandler()
            handlerRegistration = None
        return None
