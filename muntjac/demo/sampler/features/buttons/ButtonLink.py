
from muntjac.api import Button

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class ButtonLink(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Link button'


    def getDescription(self):
        return ('A link-styled button works like a push button, but looks like'
            + ' a Link.<br/> It does not actually link somewhere, but'
            + ' triggers a server-side event, just like a regular button.')


    def getRelatedAPI(self):
        return [APIResource(Button)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.FeatureSet import Links
        from muntjac.demo.sampler.features.buttons.ButtonPush import ButtonPush
        from muntjac.demo.sampler.features.buttons.CheckBoxes import CheckBoxes

        from muntjac.demo.sampler.features.blueprints.ProminentPrimaryAction import \
            ProminentPrimaryAction

        from muntjac.demo.sampler.features.link.LinkCurrentWindow import \
            LinkCurrentWindow

        return [ButtonPush, CheckBoxes, LinkCurrentWindow,
                ProminentPrimaryAction, Links]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
