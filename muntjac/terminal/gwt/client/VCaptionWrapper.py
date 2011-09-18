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

from com.vaadin.terminal.gwt.client.VCaption import (VCaption,)


class VCaptionWrapper(FlowPanel):
    CLASSNAME = 'v-captionwrapper'
    _caption = None
    _widget = None

    def __init__(self, toBeWrapped, client):
        self._caption = VCaption(toBeWrapped, client)
        self.add(self._caption)
        self._widget = toBeWrapped
        self.add(self._widget)
        self.setStyleName(self.CLASSNAME)

    def updateCaption(self, uidl):
        self._caption.updateCaption(uidl)
        self.setVisible(not uidl.getBooleanAttribute('invisible'))

    def getPaintable(self):
        return self._widget
