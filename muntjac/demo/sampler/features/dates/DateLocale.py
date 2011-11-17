
from muntjac.api import DateField, InlineDateField

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class DateLocale(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Date selection, locale'


    def getDescription(self):
        return ('In this example, you can select a different locale'
            ' from the combo box and see how the calendar component'
            ' is localized.')


    def getRelatedAPI(self):
        return [
            APIResource(DateField),
            APIResource(InlineDateField)
        ]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.dates.DatePopupInputPrompt import \
            DatePopupInputPrompt

        from muntjac.demo.sampler.features.dates.DateInline import DateInline
        from muntjac.demo.sampler.features.dates.DatePopup import DatePopup

        from muntjac.demo.sampler.features.dates.DateResolution import \
            DateResolution

        return [
            DateInline,
            DatePopup,
            DatePopupInputPrompt,
            DateResolution
        ]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
