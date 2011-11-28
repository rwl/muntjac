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

from __pyjamas__ import JS


class ComponentDetailMap(JavaScriptObject):

    def __init__(self):
        pass


    @classmethod
    def create(cls):
        return JavaScriptObject.createObject()


    def isEmpty(self):
        return len(self) == 0


    def containsKey(self, key):
        JS("""
            return @{{self}}.hasOwnProperty(@{{key}});
        """)
        pass


    def get(self, key):
        JS("""
            return @{{self}}[@{{key}}];
        """)
        pass


    def put(self, Id, value):
        JS("""
            @{{self}}[@{{Id}}] = @{{value}};
        """)
        pass


    def remove(self, Id):
        JS("""
            delete @{{self}}[@{{Id}}];
        """)
        pass


    def size(self):
        JS("""
            var count = 0;
            for(var key in @{{self}}) {
                count++;
            }
            return count;
        """)
        pass


    def clear(self):
        JS("""
            for(var key in @{{self}}) {
                if(@{{self}}.hasOwnProperty(key)) {
                    delete @{{self}}[key];
                }
            }
        """)
        pass


    def fillWithValues(self, lst):
        JS("""
            for(var key in @{{self}}) {
                @{{lst}}.@java.util.Collection::add(Ljava/lang/Object;)(@{{self}}[key]);
            }
        """)
        pass


    def values(self):
        lst = list()
        self.fillWithValues(lst)
        return lst
