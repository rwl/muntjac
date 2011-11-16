
from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.util import clsname


class APIResource(NamedExternalResource):
    """A NamedExternalResource pointing to the API doc for the given class.
    Knows where the API docs are located for some common APIs, but one can also
    specify an API doc baseurl. The name will be set to the class simpleName.
    """

    _VAADIN_BASE = 'http://doc.muntiacus.org/api'
    _JAVA_BASE = 'http://java.sun.com/javase/6/docs/api/'
    _SERVLET_BASE = 'http://java.sun.com/products/servlet/2.5/docs/servlet-2_5-mr2'
    _PORTLET_BASE = 'http://developers.sun.com/docs/jscreator/apis/portlet'

    def __init__(self, *args):

        nargs = len(args)
        if nargs == 1:
            clazz, = args
            APIResource.__init__(self, self.resolveBaseUrl(clazz), clazz)
        elif nargs == 2:
            baseUrl, clazz = args
            super(APIResource, self).__init__(self.resolveName(clazz),
                    self.getJavadocUrl(baseUrl, clazz))
        else:
            raise ValueError

    @classmethod
    def getJavadocUrl(cls, baseUrl, clazz):
        if not baseUrl.endswith('/'):
            baseUrl += '/'
        #path = clazz.__name__.replace('\\.', '/')
        path = clsname(clazz)
        path = path.replace('\\$', '.')
        return baseUrl + path + '-class.html'

    @classmethod
    def resolveBaseUrl(cls, clazz):
        """Tries to resolve the API doc baseurl for the given class by looking
        at the packagename.
        """
        name = clazz.__name__
        if name.startswith('javax.servlet.'):
            return cls._SERVLET_BASE
        elif name.startswith('javax.portlet.'):
            return cls._PORTLET_BASE
        elif name.startswith('java.') or name.startswith('javax.'):
            return cls._JAVA_BASE
        return cls._VAADIN_BASE

    @classmethod
    def resolveName(cls, clazz):
        ec = None #clazz.getEnclosingClass()  # no inner classes
        return (ec.__name__ + '.' if ec is not None else '') + clazz.__name__
