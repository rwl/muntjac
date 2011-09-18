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

# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)


class ComponentDetailMap(JavaScriptObject):

    def __init__(self):
        pass

    @classmethod
    def create(cls):
        return cls.JavaScriptObject.createObject()

    def isEmpty(self):
        return len(self) == 0

    def containsKey(self, key):
        # -{
        #         return this.hasOwnProperty(key);
        #     }-

        pass

    def get(self, key):
        # -{
        #         return this[key];
        #     }-

        pass

    def put(self, id, value):
        # -{
        #         this[id] = value;
        #     }-

        pass

    def remove(self, id):
        # -{
        #         delete this[id];
        #     }-

        pass

    def size(self):
        # -{
        #         var count = 0;
        #         for(var key in this) {
        #             count++;
        #         }
        #         return count;
        #     }-

        pass

    def clear(self):
        # -{
        #         for(var key in this) {
        #             if(this.hasOwnProperty(key)) {
        #                 delete this[key];
        #             }
        #         }
        #     }-

        pass

    def fillWithValues(self, list):
        # -{
        #         for(var key in this) {
        #             list.@java.util.Collection::add(Ljava/lang/Object;)(this[key]);
        #         }
        #     }-

        pass

    def values(self):
        list = list()
        self.fillWithValues(list)
        return list
