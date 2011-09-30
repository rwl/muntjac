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

from muntjac.ui.AbstractSelect import AbstractSelect
from muntjac.data.Container import Container

from muntjac.event.FieldEvents import \
    BlurEvent, IBlurListener, IBlurNotifier, FocusEvent, \
    IFocusListener, IFocusNotifier
from muntjac.ui.AbstractComponent import AbstractComponent


class OptionGroup(AbstractSelect, IBlurNotifier, IFocusNotifier):
    """Configures select to be used as an option group."""

    #CLIENT_WIDGET = ClientWidget(VOptionGroup, LoadStyle.EAGER)

    def __init__(self, *args):
        self._disabledItemIds = set()

        args = args
        nargs = len(args)
        if nargs == 0:
            super(OptionGroup, self)()
        elif nargs == 1:
            caption, = args
            super(OptionGroup, self)(caption)
        elif nargs == 2:
            if isinstance(args[1], Container):
                caption, dataSource = args
                super(OptionGroup, self)(caption, dataSource)
            else:
                caption, options = args
                super(OptionGroup, self)(caption, options)
        else:
            raise ValueError, 'too many arguments'


    def paintContent(self, target):
        target.addAttribute('type', 'optiongroup')
        super(OptionGroup, self).paintContent(target)


    def paintItem(self, target, itemId):
        super(OptionGroup, self).paintItem(target, itemId)
        if not self.isItemEnabled(itemId):
            target.addAttribute('disabled', True)


    def changeVariables(self, source, variables):
        super(OptionGroup, self).changeVariables(source, variables)

        if FocusEvent.EVENT_ID in variables:
            self.fireEvent(FocusEvent(self))

        if BlurEvent.EVENT_ID in variables:
            self.fireEvent(BlurEvent(self))


    def addListener(self, listener):
        if isinstance(listener, IBlurListener):
            AbstractComponent.addListener(self, BlurEvent.EVENT_ID,
                    BlurEvent, listener, IBlurListener.blurMethod)
        else:
            AbstractComponent.addListener(self, FocusEvent.EVENT_ID,
                    FocusEvent, listener, IFocusListener.focusMethod)


    def removeListener(self, listener):
        if isinstance(listener, IBlurListener):
            AbstractComponent.removeListener(self, BlurEvent.EVENT_ID,
                    BlurEvent, listener)
        else:
            AbstractComponent.removeListener(self, FocusEvent.EVENT_ID,
                    FocusEvent, listener)


    def setValue(self, newValue, repaintIsNotNeeded):
        if repaintIsNotNeeded:
            # Check that value from changeVariables() doesn't contain unallowed
            # selections: In the multi select mode, the user has selected or
            # deselected a disabled item. In the single select mode, the user
            # has selected a disabled item.
            if self.isMultiSelect():
                currentValueSet = self.getValue()
                newValueSet = newValue
                for itemId in currentValueSet:
                    if (not self.isItemEnabled(itemId)
                            and not (itemId in newValueSet)):
                        self.requestRepaint()
                        return

                for itemId in newValueSet:
                    if (not self.isItemEnabled(itemId)
                            and not (itemId in currentValueSet)):
                        self.requestRepaint()
                        return
            else:
                if newValue is None:
                    newValue = self.getNullSelectionItemId()

                if not self.isItemEnabled(newValue):
                    self.requestRepaint()
                    return

        super(OptionGroup, self).setValue(newValue, repaintIsNotNeeded)


    def setItemEnabled(self, itemId, enabled):
        """Sets an item disabled or enabled. In the multiselect mode, a disabled
        item cannot be selected or deselected by the user. In the single
        selection mode, a disable item cannot be selected.

        However, programmatical selection or deselection of an disable item is
        possible. By default, items are enabled.

        @param itemId
                   the id of the item to be disabled or enabled
        @param enabled
                   if true the item is enabled, otherwise the item is disabled
        """
        if itemId is not None:

            if enabled:
                self._disabledItemIds.remove(itemId)
            else:
                self._disabledItemIds.add(itemId)

            self.requestRepaint()


    def isItemEnabled(self, itemId):
        """Returns true if the item is enabled.

        @param itemId
                   the id of the item to be checked
        @return true if the item is enabled, false otherwise
        @see #setItemEnabled(Object, boolean)
        """
        if itemId is not None:
            return not (itemId in self._disabledItemIds)

        return True
