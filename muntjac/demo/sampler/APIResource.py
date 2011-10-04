
from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource


class APIResource(NamedExternalResource):
    """A NamedExternalResource pointing to the javadoc for the given class.
    Knows where the javadocs are located for some common APIs, but one can also
    specify a javadoc baseurl. The name will be set to the class simpleName.
    """

    _VAADIN_BASE = 'http://www.vaadin.com/api'
    _JAVA_BASE = 'http://java.sun.com/javase/6/docs/api/'
    _SERVLET_BASE = 'http://java.sun.com/products/servlet/2.5/docs/servlet-2_5-mr2'
    _PORTLET_BASE = 'http://developers.sun.com/docs/jscreator/apis/portlet'

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            clazz, = _0
            self.__init__(self.resolveBaseUrl(clazz), clazz)
        elif _1 == 2:
            baseUrl, clazz = _0
            super(APIResource, self)(self.resolveName(clazz), self.getJavadocUrl(baseUrl, clazz))
        else:
            raise ValueError

    @classmethod
    def getJavadocUrl(cls, baseUrl, clazz):
        if not baseUrl.endswith('/'):
            baseUrl += '/'
        path = clazz.getName().replaceAll('\\.', '/')
        path = path.replaceAll('\\$', '.')
        return baseUrl + path + '.html'

    @classmethod
    def resolveBaseUrl(cls, clazz):
        """Tries to resolve the javadoc baseurl for the given class by looking at
        the packagename.

        @param clazz
        @return
        """
        name = clazz.getName()
        if name.startswith('javax.servlet.'):
            return cls._SERVLET_BASE
        elif name.startswith('javax.portlet.'):
            return cls._PORTLET_BASE
        elif name.startswith('java.') or name.startswith('javax.'):
            return cls._JAVA_BASE
        return cls._VAADIN_BASE

    @classmethod
    def resolveName(cls, clazz):
        ec = clazz.getEnclosingClass()
        return (ec.__name__ + '.' if ec is not None else '') + clazz.__name__
