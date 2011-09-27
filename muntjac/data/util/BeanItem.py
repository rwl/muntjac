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

from muntjac.data.util.PropertysetItem import PropertysetItem
from muntjac.data.util.MethodPropertyDescriptor import MethodPropertyDescriptor


class BeanItem(PropertysetItem):
    """A wrapper class for adding the Item interface to any Java Bean.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def __init__(self, *args):
        """<p>
        Creates a new instance of <code>BeanItem</code> and adds all properties
        of a Java Bean to it. The properties are identified by their respective
        bean names.
        </p>

        <p>
        Note : This version only supports introspectable bean properties and
        their getter and setter methods. Stand-alone <code>is</code> and
        <code>are</code> methods are not supported.
        </p>

        @param bean
                   the Java Bean to copy properties from.
        ---
        <p>
        Creates a new instance of <code>BeanItem</code> using a pre-computed set
        of properties. The properties are identified by their respective bean
        names.
        </p>

        @param bean
                   the Java Bean to copy properties from.
        @param propertyDescriptors
                   pre-computed property descriptors
        ---
        <p>
        Creates a new instance of <code>BeanItem</code> and adds all listed
        properties of a Java Bean to it - in specified order. The properties are
        identified by their respective bean names.
        </p>

        <p>
        Note : This version only supports introspectable bean properties and
        their getter and setter methods. Stand-alone <code>is</code> and
        <code>are</code> methods are not supported.
        </p>

        @param bean
                   the Java Bean to copy properties from.
        @param propertyIds
                   id of the property.
        ---
        <p>
        Creates a new instance of <code>BeanItem</code> and adds all listed
        properties of a Java Bean to it - in specified order. The properties are
        identified by their respective bean names.
        </p>

        <p>
        Note : This version only supports introspectable bean properties and
        their getter and setter methods. Stand-alone <code>is</code> and
        <code>are</code> methods are not supported.
        </p>

        @param bean
                   the Java Bean to copy properties from.
        @param propertyIds
                   ids of the properties.
        """
        # The bean which this Item is based on.
        self._bean = None

        nargs = len(args)
        if nargs == 1:
            bean, = args
            self.__init__(bean, self.getPropertyDescriptors(bean.__class__))
        elif nargs == 2:
            if isinstance(args[1], dict):
                bean, propertyDescriptors = args
                self._bean = bean
                for pd in propertyDescriptors.values():
                    self.addItemProperty(pd.getName(), pd.createProperty(bean))
            else:
                bean, propertyIds = args
                self._bean = bean
                # Create bean information
                pds = self.getPropertyDescriptors(bean.__class__)
                # Add all the bean properties as MethodProperties to this Item
                for idd in propertyIds:
                    pd = pds.get(idd)
                    if pd is not None:
                        self.addItemProperty(pd.getName(), pd.createProperty(bean))
        else:
            raise ValueError, 'invalid number of arguments'


    @classmethod
    def getPropertyDescriptors(cls, beanClass):
        """<p>
        Perform introspection on a Java Bean class to find its properties.
        </p>

        <p>
        Note : This version only supports introspectable bean properties and
        their getter and setter methods. Stand-alone <code>is</code> and
        <code>are</code> methods are not supported.
        </p>

        @param beanClass
                   the Java Bean class to get properties for.
        @return an ordered map from property names to property descriptors
        """
        pdMap = dict()

        # Try to introspect, if it fails, we just have an empty Item
        try:
            propertyDescriptors = cls.getBeanPropertyDescriptor(beanClass)
            # Add all the bean properties as MethodProperties to this Item
            # later entries on the list overwrite earlier ones
            for pd in propertyDescriptors:
                getMethod = pd.getReadMethod()
                if getMethod is not None and getMethod.__class__() != cls.Object:  # FIXME: getDeclaringClass
                    vaadinPropertyDescriptor = MethodPropertyDescriptor(pd.getName(),
                                                                        pd.getPropertyType(),
                                                                        pd.getReadMethod(),
                                                                        pd.getWriteMethod())
                    pdMap[pd.getName()] = vaadinPropertyDescriptor
        except Exception:  ## FIXME: IntrospectionException
            pass

        return pdMap


    @classmethod
    def getBeanPropertyDescriptor(cls, beanClass):
        """Returns the property descriptors of a class or an interface.

        For an interface, superinterfaces are also iterated as Introspector does
        not take them into account (Oracle Java bug 4275879), but in that case,
        both the setter and the getter for a property must be in the same
        interface and should not be overridden in subinterfaces for the discovery
        to work correctly.

        For interfaces, the iteration is depth first and the properties of
        superinterfaces are returned before those of their subinterfaces.

        @param beanClass
        @return
        @throws IntrospectionException
        """
        # Oracle bug 4275879: Introspector does not consider superinterfaces of
        # an interface
        if beanClass.isInterface():  # FIXEM isInterface
            propertyDescriptors = list()
            for cls in beanClass.getInterfaces():
                propertyDescriptors.addAll(cls.getBeanPropertyDescriptor(cls))
#            info = Introspector.getBeanInfo(beanClass)
#            propertyDescriptors.addAll(Arrays.asList(info.getPropertyDescriptors()))
            return propertyDescriptors
        else:
#            info = Introspector.getBeanInfo(beanClass)  # FIXME: Introspector
#            return Arrays.asList(info.getPropertyDescriptors())
            pass


    def getBean(self):
        """Gets the underlying JavaBean object.

        @return the bean object.
        """
        return self._bean
