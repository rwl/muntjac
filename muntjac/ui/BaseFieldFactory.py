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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.ui.DefaultFieldFactory import (DefaultFieldFactory,)
from com.vaadin.ui.FieldFactory import (FieldFactory,)


class BaseFieldFactory(FieldFactory):
    """Default implementation of the the following Field types are used by default:
    <p>
    <b>Boolean</b>: Button(switchMode:true).<br/>
    <b>Date</b>: DateField(resolution: day).<br/>
    <b>Item</b>: Form. <br/>
    <b>default field type</b>: TextField.
    <p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.1
    @deprecated use {@link DefaultFieldFactory} or own implementations on
                {@link FormFieldFactory} or {@link TableFieldFactory} instead.
    """

    def createField(self, *args):
        """Creates the field based on type of data.


        @param type
                   the type of data presented in field.
        @param uiContext
                   the context where the Field is presented.

        @see com.vaadin.ui.FieldFactory#createField(Class, Component)
        ---
        Creates the field based on the datasource property.

        @see com.vaadin.ui.FieldFactory#createField(Property, Component)
        ---
        Creates the field based on the item and property id.

        @see com.vaadin.ui.FieldFactory#createField(Item, Object, Component)
        ---
        @see com.vaadin.ui.FieldFactory#createField(com.vaadin.data.Container,
             java.lang.Object, java.lang.Object, com.vaadin.ui.Component)
        """
        _0 = args
        _1 = len(args)
        if _1 == 2:
            if isinstance(_0[0], Class):
                type, uiContext = _0
                return DefaultFieldFactory.createFieldByPropertyType(type)
            else:
                property, uiContext = _0
                if property is not None:
                    return self.createField(property.getType(), uiContext)
                else:
                    return None
        elif _1 == 3:
            item, propertyId, uiContext = _0
            if item is not None and propertyId is not None:
                f = self.createField(item.getItemProperty(propertyId), uiContext)
                if isinstance(f, AbstractComponent):
                    name = DefaultFieldFactory.createCaptionByPropertyId(propertyId)
                    f.setCaption(name)
                return f
            else:
                return None
        elif _1 == 4:
            container, itemId, propertyId, uiContext = _0
            return self.createField(container.getContainerProperty(itemId, propertyId), uiContext)
        else:
            raise ARGERROR(2, 4)
