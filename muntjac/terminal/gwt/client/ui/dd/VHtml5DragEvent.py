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

# from com.google.gwt.core.client.JsArrayString import (JsArrayString,)


class VHtml5DragEvent(NativeEvent):
    """Helper class to access html5 style drag events.

    TODO Gears support ?
    """

    def __init__(self):
        pass

    def getTypes(self):
        # -{
        #         // IE does not support types, return some basic values
        #         return this.dataTransfer.types ? this.dataTransfer.types : ["Text","Url","Html"];
        #      }-

        pass

    def getDataAsText(self, type):
        # -{
        #          var v = this.dataTransfer.getData(type);
        #          return v;
        #      }-

        pass

    def getFileAsString(self, index):
        """Works on FF 3.6 and possibly with gears.

        @param index
        @return
        """
        # -{
        #         if(this.dataTransfer.files.length > 0 && this.dataTransfer.files[0].getAsText) {
        #             return this.dataTransfer.files[index].getAsText("UTF-8");
        #         }
        #         return null;
        #     }-

        pass

    def setDragEffect(self, effect):
        # -{
        #         try {
        #             this.dataTransfer.dropEffect = effect;
        #         } catch (e){}
        #      }-

        pass

    def getEffectAllowed(self):
        # -{
        #             return this.dataTransfer.effectAllowed;
        #      }-

        pass

    def getFileCount(self):
        # -{
        #             return this.dataTransfer.files ? this.dataTransfer.files.length : 0;
        #      }-

        pass

    def getFile(self, fileIndex):
        # -{
        #             return this.dataTransfer.files[fileIndex];
        #      }-

        pass
