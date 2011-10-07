
from muntjac.terminal.external_resource import ExternalResource


class NamedExternalResource(ExternalResource):

    def __init__(self, name, sourceURL):
        super(NamedExternalResource, self).__init__(sourceURL)
        self._name = name


    def getName(self):
        return self._name
