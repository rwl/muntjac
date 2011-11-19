
import inspect

from muntjac.util import fullname
from muntjac.util import loadClass

from muntjac.terminal.gwt.server.abstract_application_servlet import \
    AbstractApplicationServlet


class Feature(object):
    """Represents one feature or sample, with associated example.
    """

    PROPERTY_ICON = 'Icon'
    PROPERTY_NAME = 'Name'
    PROPERTY_DESCRIPTION = 'Description'

    _MSG_SOURCE_NOT_AVAILABLE = ('I\'m terribly sorry,'
            + ' but it seems the source could not be found.\n'
            + 'Please try adding the source folder to the classpath for your'
            + ' server, or tell the administrator to do so!')

    _MUTEX = object()

    def __init__(self):
        self._pythonSource = None


    def getName(self):
        """Gets the name of this feature. Try not to exceed 25 characters
        too much.
        """
        raise NotImplementedError


    def getDescription(self):
        """Gets the description for this feature. Should describe what the
        example intends to showcase. May contain HTML. 100 words should be
        enough, and about 7 rows...

        @return: the description
        """
        raise NotImplementedError


    def getRelatedResources(self):
        """Gets related resources, i.e links to resources related to the
        example.

        Good candidates are resources used to make the example (CSS, images,
        custom layouts), documentation links (reference manual), articles
        (e.g. pattern description, usability discussion).

        May return null, if the example has no related resources.

        The name of the NamedExternalResource will be shown in the UI.
        Note that API doc should be referenced via L{getRelatedAPI}.

        @see: L{getThemeBase}
        @return: related external stuff
        """
        raise NotImplementedError


    def getRelatedAPI(self):
        """Gets related API resources, i.e links to API doc of used classes.

        Good candidates are Muntjac classes being demoed in the example, or
        other classes playing an important role in the example.

        May return null, if the example uses no interesting classes.
        """
        raise NotImplementedError


    def getRelatedFeatures(self):
        """Gets related Features; the classes returned should extend Feature.

        Good candidates are Features similar to this one, Features using the
        functionality demoed in this one, and Features being used in this one.

        May return null, if no other Features are related to this one.
        """
        raise NotImplementedError


    def getIconName(self):
        """Gets the name of the icon for this feature, usually simpleName +
        extension.
        """
        icon = self.__class__.__name__ + '.gif'
        return icon


    def getExample(self):
        """Get the example instance. Override if instantiation needs
        parameters.
        """
        pkgName, className = fullname(self).rsplit('.', 1)
        canonicalName = pkgName + 'Example' + '.' + className + 'Example'
#        try:
        classObject = loadClass(canonicalName)
        return classObject()
#        except Exception:
#            return None


    def getSource(self):
        if self._pythonSource is None:
            try:
                ex = self.getExample()
                self._pythonSource = inspect.getsource(inspect.getmodule(ex))
            except IOError:
                print (self._MSG_SOURCE_NOT_AVAILABLE
                       + ' (' + self.getFragmentName() + ')')
                self._pythonSource = self._MSG_SOURCE_NOT_AVAILABLE

        return self._pythonSource


    def getSourceHTML(self):
        return self.getSource()


    def getFragmentName(self):
        """Gets the name used when resolving the path for this feature.
        Usually no need to override, but NOTE that this must be unique
        within Sampler.
        """
        return self.__class__.__name__


    def getSinceVersion(self):
        """Returns the Muntjac version number in which this feature was added
        to Sampler. Usually features should only be added in major and minor
        version, not in maintenance versions.

        Uses int internally for easy comparison: version 6.1.4 -> 61
        (maintenance version number is ignored)

        Override in each feature. Returns Version.OLD otherwise.

        @return: Muntjac version when this feature was added to Sampler
        """
        raise NotImplementedError


    @classmethod
    def getThemeBase(cls):
        """Gets the base url used to reference theme resources.
        """
        from muntjac.demo.sampler.SamplerApplication import SamplerApplication
        return SamplerApplication.getThemeBase()


    def __str__(self):
        return self.getName()


    def __eq__(self, obj):
        # A feature is uniquely identified by its class name
        if obj is None:
            return False
        return obj.__class__ == self.__class__


    def hashCode(self):
        # A feature is uniquely identified by its class name
        return hash(self.__class__)

    def __hash__(self):
        return self.hashCode()


class Version(object):

    OLD = None
    BUILD = None
    V62 = None
    V63 = None
    V64 = None
    V65 = None
    V66 = None

    def __init__(self, version):
        self.version = version


    def isNew(self):
        """Checks whether this version is newer or as new as the build that it
        is included in.

        You can use Version.BUILD if you wish for a Feature to always appear
        as new.
        """
        return self.BUILD.version <= self.version

    _enum_values = [OLD, BUILD, V62, V63, V64, V65, V66]

    @classmethod
    def values(cls):
        return cls._enum_values[:]


Version.OLD = Version(0)
Version.BUILD = Version(int('%d%d' % (AbstractApplicationServlet.VERSION_MAJOR,
        AbstractApplicationServlet.VERSION_MINOR)))
Version.V62 = Version(62)
Version.V63 = Version(63)
Version.V64 = Version(64)
Version.V65 = Version(65)
Version.V66 = Version(66)
