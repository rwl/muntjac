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

from datetime import datetime

try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from muntjac.data.Item import Item
from muntjac.ui.ITableFieldFactory import ITableFieldFactory
from muntjac.ui.IFormFieldFactory import IFormFieldFactory
from muntjac.ui.DateField import DateField
from muntjac.ui.TextField import TextField
from muntjac.ui.CheckBox import CheckBox
from muntjac.ui.Form import Form


class DefaultFieldFactory(IFormFieldFactory, ITableFieldFactory):
    """This class contains a basic implementation for both {@link IFormFieldFactory}
    and {@link ITableFieldFactory}. The class is singleton, use {@link #get()}
    method to get reference to the instance.

    <p>
    There are also some static helper methods available for custom built field
    factories.
    """

    @classmethod
    def get(cls):
        """Singleton method to get an instance of DefaultFieldFactory.

        @return an instance of DefaultFieldFactory
        """
        return INSTANCE


    def createField(self, *args):
        nargs = len(args)
        if nargs == 3:
            item, propertyId, _ = args
            typ = item.getItemProperty(propertyId).getType()
            field = self.createFieldByPropertyType(typ)
            field.setCaption(self.createCaptionByPropertyId(propertyId))
            return field
        elif nargs == 4:
            container, itemId, propertyId, _ = args
            containerProperty = container.getContainerProperty(itemId, propertyId)
            typ = containerProperty.getType()
            field = self.createFieldByPropertyType(typ)
            field.setCaption(self.createCaptionByPropertyId(propertyId))
            return field
        else:
            raise ValueError, 'invalid number of arguments'


    @classmethod
    def createCaptionByPropertyId(cls, propertyId):
        """If name follows method naming conventions, convert the name to spaced
        upper case text. For example, convert "firstName" to "First Name"

        @param propertyId
        @return the formatted caption string
        """
        name = str(propertyId)

        if len(name) > 0:
            if name.find(' ') < 0 \
                    and name[0] == name[0].lower() \
                    and name[0] != name[0].upper():
                out = StringIO()
                out.append(name[0].upper())
                i = 1

                while i < len(name):
                    j = i
                    while j < len(name):
                        c = name[j]
                        if c.lower() != c and c.upper() == c:
                            break
                        j += 1

                    if j == len(name):
                        out.append(name[i:])
                    else:
                        out.append(name[i:j])
                        out.append(' ' + name[j])
                    i = j + 1
                name = out.getvalue()
                out.close()

        return name


    @classmethod
    def createFieldByPropertyType(cls, typ):
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
        if typ is None:
            return None

        # Item field
        if issubclass(typ, Item):
            return Form()

        # Date field
        if issubclass(typ, datetime):
            df = DateField()
            df.setResolution(DateField.RESOLUTION_DAY)
            return df

        # Boolean field
        if issubclass(typ, bool):
            return CheckBox()

        return TextField()


INSTANCE = DefaultFieldFactory()
