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

from muntjac.ui.default_field_factory import DefaultFieldFactory
from muntjac.ui.field_factory import IFieldFactory
from muntjac.data.property import IProperty
from muntjac.ui.abstract_component import AbstractComponent


class BaseFieldFactory(IFieldFactory):
    """Default implementation of the the following Field types are used
    by default:

    <b>Boolean</b>: Button(switchMode:true).<br/>
    <b>Date</b>: DateField(resolution: day).<br/>
    <b>Item</b>: Form. <br/>
    <b>default field type</b>: TextField.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.1
    @deprecated use {@link DefaultFieldFactory} or own implementations
                on {@link FormFieldFactory} or {@link TableFieldFactory}
                instead.
    """

    def __init__(self):
        raise DeprecationWarning, 'use DefaultFieldFactory'


    def createField(self, *args):
        """Creates the field based on type of data.

        @param type
                   the type of data presented in field.
        @param uiContext
                   the context where the Field is presented.
        @see IFieldFactory.createField
        """
        nargs = len(args)
        if nargs == 2:
            if isinstance(args[0], IProperty):
                prop, uiContext = args
                if property is not None:
                    return self.createField(prop.getType(), uiContext)
                else:
                    return None
            else:
                typ, uiContext = args
                return DefaultFieldFactory.createFieldByPropertyType(typ)
        elif nargs == 3:
            item, propertyId, uiContext = args
            if item is not None and propertyId is not None:
                f = self.createField(item.getItemProperty(propertyId),
                        uiContext)
                if isinstance(f, AbstractComponent):
                    name = DefaultFieldFactory.createCaptionByPropertyId(
                            propertyId)
                    f.setCaption(name)
                return f
            else:
                return None
        elif nargs == 4:
            container, itemId, propertyId, uiContext = args
            prop = container.getContainerProperty(itemId, propertyId)
            return self.createField(prop, uiContext)
        else:
            raise ValueError, 'invalid number of arguments'
