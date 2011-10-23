
from muntjac.demo.sampler.Feature import Feature, Version


class PackageIcons(Feature):

    def getSinceVersion(self):
        return Version.V62


    def getName(self):
        return 'Runo theme icons'


    def getDescription(self):
        return ('<p>The alternative built-in <i>Runo</i> theme contains many '
            'useful free icons. The icons are not restricted to the Runo '
            'theme and you can use them just as well in any other theme.</p>'
            '<p>The icons are located in the Runo theme folder '
            '<tt>VAADIN/themes/runo/icons</tt>; you can copy them to your '
            'own theme from there.</p>'
            '<p>The icons are available in three sizes: 16x16, 32x32, and '
            '64x64 pixels.</p>')


    def getRelatedAPI(self):
        return []


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.commons.Icons import Icons
        return [Icons]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
