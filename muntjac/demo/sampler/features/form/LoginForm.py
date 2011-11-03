
from muntjac.ui import login_form

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class LoginForm(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Login form'


    def getDescription(self):
        return ('Using normal Muntjac components to build a login form is '
            'sometimes sufficient, but in many cases you\'ll want the '
            'browser to remember the credentials later on. Using the '
            'LoginForm helps in that case. You can override methods from '
            'LoginForm if you wish to specify the generated HTML yourself.')


    def getRelatedAPI(self):
        return [APIResource(login_form.LoginForm)]


    def getRelatedFeatures(self):
        return None


    def getRelatedResources(self):
        return None
