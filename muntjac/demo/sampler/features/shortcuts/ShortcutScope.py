
from muntjac.demo.sampler.Feature import Feature, Version


class ShortcutScope(Feature):

    def getSinceVersion(self):
        return Version.V63


    def getName(self):
        return 'Shortcuts, scope'


    def getDescription(self):
        return ('Here, identical shortcuts work independently'
            ' within each panel; they are <i>scoped</i>'
            ' to the panel.'
            '<p>ALT-SHIFT-1 focuses the first panel, ALT-SHIFT-2'
            ' the second, and within the panels arrow-down'
            ' advances and ALT-SHIFT-F/ALT-SHIFT-L focuses'
            ' firstname/lastname respectively. '
            'ALT-SHIFT-S saves each panel.')


    def getRelatedAPI(self):
        return []


    def getRelatedFeatures(self):
        return []


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
