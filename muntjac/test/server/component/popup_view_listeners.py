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

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.popup_view import \
    PopupView, PopupVisibilityEvent, IPopupVisibilityListener

from muntjac.ui.label import Label


class PopupViewListeners(AbstractListenerMethodsTest):

    def testPopupVisibilityListenerAddGetRemove(self):
        self._testListenerAddGetRemove(PopupView, PopupVisibilityEvent,
                IPopupVisibilityListener, PopupView('', Label()))
