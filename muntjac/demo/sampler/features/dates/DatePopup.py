
from muntjac.api import DateField, PopupDateField

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class DatePopup(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Pop-up date selection'


    def getDescription(self):
        return ('In this example, the resolution is set to be one day'
            ' and the DateField component is shown as a calendar pop-up.')


    def getRelatedAPI(self):
        return [APIResource(DateField), APIResource(PopupDateField)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.dates.DateInline import DateInline
        from muntjac.demo.sampler.features.dates.DateLocale import DateLocale

        from muntjac.demo.sampler.features.dates.DateResolution import \
            DateResolution

        from muntjac.demo.sampler.features.dates.DatePopupInputPrompt import \
            DatePopupInputPrompt

        return [DatePopupInputPrompt, DateInline, DateLocale, DateResolution]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
