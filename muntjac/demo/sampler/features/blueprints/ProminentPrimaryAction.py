
from muntjac.api import Button, Link

from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class ProminentPrimaryAction(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Prominent primary action'


    def getDescription(self):
        return ('A primary action is an action that is clearly the'
            + ' default, and it should be visually more prominent'
            + ' than the secondary actions.<br/>Good candidates'
            + ' include <i>Save</i>, <i>Submit</i>, <i>Continue</i>, <i>Next</i>,'
            + ' <i>Finish</i> and so on.<br/>Note that \'dangerous\' actions'
            + ' that can not be undone should not be primary, and that it\'s'
            + ' not always possible to identify a primary action'
            + ' - don\'t force it if it\'s not obvious.')


    def getRelatedAPI(self):
        return [APIResource(Button), APIResource(Link)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.buttons.ButtonLink import ButtonLink
        from muntjac.demo.sampler.features.buttons.ButtonPush import ButtonPush

        return [ButtonPush, ButtonLink]


    def getRelatedResources(self):
        return [
            NamedExternalResource('CSS for \'Sign up\' button',
                self.getThemeBase() + 'prominentprimaryaction/styles.css'),
            NamedExternalResource(('Article: Primary & Secondary Actions '
                'in Web Forms (LukeW)'),
                'http://www.lukew.com/resources/articles/psactions.asp'),
            NamedExternalResource(('Article: Primary & Secondary Actions '
                '(UI Pattern Factory)'),
                'http://uipatternfactory.com/p=primary-and-secondary-actions/')]
