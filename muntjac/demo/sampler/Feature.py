
from muntjac.util import fullname
from muntjac.util import loadClass
from muntjac.demo.sampler.SamplerApplication import SamplerApplication

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

        @return
        """
        raise NotImplementedError


    def getDescription(self):
        """Gets the description for this feature. Should describe what the
        example intends to showcase. May contain HTML. 100 words should be
        enough, and about 7 rows...

        @return the description
        """
        raise NotImplementedError


    def getRelatedResources(self):
        """Gets related resources, i.e links to resources related to the
        example.

        Good candidates are resources used to make the example (CSS, images,
        custom layouts), documentation links (reference manual), articles
        (e.g. pattern description, usability discussion).

        May return null, if the example has no related resources.

        The name of the NamedExternalResource will be shown in the UI. <br/>
        Note that Javadoc should be referenced via {@link #getRelatedAPI()}.

        @see #getThemeBase()
        @return related external stuff
        """
        raise NotImplementedError


    def getRelatedAPI(self):
        """Gets related API resources, i.e links to javadoc of used classes.

        Good candidates are Vaadin classes being demoed in the example, or
        other classes playing an important role in the example.

        May return null, if the example uses no interesting classes.

        @return
        """
        raise NotImplementedError


    def getRelatedFeatures(self):
        """Gets related Features; the classes returned should extend Feature.

        Good candidates are Features similar to this one, Features using the
        functionality demoed in this one, and Features being used in this one.

        May return null, if no other Features are related to this one.

        @return
        """
        raise NotImplementedError


    def getIconName(self):
        """Gets the name of the icon for this feature, usually simpleName +
        extension.

        @return
        """
        icon = self.__class__.__name__ + '.gif'
        return icon


    def getExample(self):
        """Get the example instance. Override if instantiation needs
        parameters.

        @return
        """
        className = fullname(self) + 'Example'
        try:
            classObject = loadClass(className)
            return classObject()
        except Exception:
            return None


    def getSource(self):
        if self._pythonSource is None:
            try:
                # Use package name + class name so the class loader won't
                # have to guess the package name.
                resourceName = '/' + fullname(self.getExample())
                resourceName = resourceName.replace('.', '/') + '.py'
                fd = open(resourceName, 'rb')
                self._pythonSource = fd.read()
                fd.close()
            except Exception:
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

        @return
        """
        return self.__class__.__name__


    def getSinceVersion(self):
        """Returns the Vaadin version number in which this feature was added
        to Sampler. Usually features should only be added in major and minor
        version, not in maintenance versions.

        Uses int internally for easy comparison: version 6.1.4 -> 61
        (maintenance version number is ignored)

        Override in each feature. Returns Version.OLD otherwise.

        @return Version Vaadin version when this feature was added to Sampler
        """
        raise NotImplementedError


    @classmethod
    def getThemeBase(cls):
        """Gets the base url used to reference theme resources.

        @return
        """
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


class Version(object):

    OLD = [0]
    BUILD = [int(AbstractApplicationServlet.VERSION_MAJOR + ''
            + AbstractApplicationServlet.VERSION_MINOR)]
    V62 = [62]
    V63 = [63]
    V64 = [64]
    V65 = [65]
    V66 = [66]

    def __init__(self, version):
        self._version = version


    def isNew(self):
        """Checks whether this version is newer or as new as the build that it
        is included in.

        You can use Version.BUILD if you wish for a Feature to always appear
        as new.

        @return
        """
        return self.BUILD.version <= self._version

    _enum_values = [OLD, BUILD, V62, V63, V64, V65, V66]

    @classmethod
    def values(cls):
        return cls._enum_values[:]

Version._enum_values = [Version(*v) for v in Version._enum_values]
