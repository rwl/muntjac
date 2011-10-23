
from muntjac.api import DateField, InlineDateField

from muntjac.demo.sampler.features.dates.DatePopup import DatePopup
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class DateResolution(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Date selection, resolution'


    def getDescription(self):
        return ('In this example, you can select a different resolution'
            ' from the combo box and see how the calendar component'
            ' changes.')


    def getRelatedAPI(self):
        return [APIResource(DateField), APIResource(InlineDateField)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.dates.DateInline import DateInline
        from muntjac.demo.sampler.features.dates.DateLocale import DateLocale

        from muntjac.demo.sampler.features.dates.DatePopupInputPrompt import \
            DatePopupInputPrompt

        return [DateInline, DatePopup, DatePopupInputPrompt, DateLocale]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
