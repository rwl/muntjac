
from muntjac.api import DateField, InlineDateField


from muntjac.demo.sampler.features.dates.DateLocale import DateLocale
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.dates.DateResolution import DateResolution
from muntjac.demo.sampler.Feature import Feature, Version


class DateInline(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Inline date selection'


    def getDescription(self):
        return ('In this example, the resolution is set to be one day'
            ' and the DateField component is shown as an inline calendar'
            ' component.')


    def getRelatedAPI(self):
        return [
            APIResource(DateField),
            APIResource(InlineDateField)
        ]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.dates.DatePopupInputPrompt import \
            DatePopupInputPrompt

        from muntjac.demo.sampler.features.dates.DatePopup import DatePopup

        return [
            DatePopup,
            DatePopupInputPrompt,
            DateLocale,
            DateResolution
        ]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
