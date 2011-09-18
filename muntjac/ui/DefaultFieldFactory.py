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
from com.vaadin.data.Item import (Item,)
from com.vaadin.ui.TableFieldFactory import (TableFieldFactory,)
from com.vaadin.ui.FormFieldFactory import (FormFieldFactory,)
from com.vaadin.ui.DateField import (DateField,)
from com.vaadin.ui.TextField import (TextField,)
from com.vaadin.ui.CheckBox import (CheckBox,)
from com.vaadin.ui.Form import (Form,)
# from java.util.Date import (Date,)


class DefaultFieldFactory(FormFieldFactory, TableFieldFactory):
    """This class contains a basic implementation for both {@link FormFieldFactory}
    and {@link TableFieldFactory}. The class is singleton, use {@link #get()}
    method to get reference to the instance.

    <p>
    There are also some static helper methods available for custom built field
    factories.
    """
    _instance = DefaultFieldFactory()

    @classmethod
    def get(cls):
        """Singleton method to get an instance of DefaultFieldFactory.

        @return an instance of DefaultFieldFactory
        """
        return cls._instance

    def __init__(self):
        pass

    def createField(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 3:
            item, propertyId, uiContext = _0
            type = item.getItemProperty(propertyId).getType()
            field = self.createFieldByPropertyType(type)
            field.setCaption(self.createCaptionByPropertyId(propertyId))
            return field
        elif _1 == 4:
            container, itemId, propertyId, uiContext = _0
            containerProperty = container.getContainerProperty(itemId, propertyId)
            type = containerProperty.getType()
            field = self.createFieldByPropertyType(type)
            field.setCaption(self.createCaptionByPropertyId(propertyId))
            return field
        else:
            raise ARGERROR(3, 4)

    @classmethod
    def createCaptionByPropertyId(cls, propertyId):
        """If name follows method naming conventions, convert the name to spaced
        upper case text. For example, convert "firstName" to "First Name"

        @param propertyId
        @return the formatted caption string
        """
        name = str(propertyId)
        if len(name) > 0:
            if (
                name.find(' ') < 0 and name[0] == cls.Character.toLowerCase(name[0]) and name[0] != cls.Character.toUpperCase(name[0])
            ):
                out = str()
                out.__add__(cls.Character.toUpperCase(name[0]))
                i = 1
                while i < len(name):
                    j = i
                    _0 = True
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            j += 1
                        if not (j < len(name)):
                            break
                        c = name[j]
                        if cls.Character.toLowerCase(c) != c and cls.Character.toUpperCase(c) == c:
                            break
                    if j == len(name):
                        out.__add__(name[i:])
                    else:
                        out.__add__(name[i:j])
                        out.__add__(' ' + name[j])
                    i = j + 1
                name = str(out)
        return name

    @classmethod
    def createFieldByPropertyType(cls, type):
        """Creates fields based on the property type.
        <p>
        The default field type is {@link TextField}. Other field types generated
        by this method:
        <p>
        <b>Boolean</b>: {@link CheckBox}.<br/>
        <b>Date</b>: {@link DateField}(resolution: day).<br/>
        <b>Item</b>: {@link Form}. <br/>
        <b>default field type</b>: {@link TextField}.
        <p>

        @param type
                   the type of the property
        @return the most suitable generic {@link Field} for given type
        """
        # Null typed properties can not be edited
        if type is None:
            return None
        # Item field
        if Item.isAssignableFrom(type):
            return Form()
        # Date field
        if Date.isAssignableFrom(type):
            df = DateField()
            df.setResolution(DateField.RESOLUTION_DAY)
            return df
        # Boolean field
        if bool.isAssignableFrom(type):
            return CheckBox()
        return TextField()
