# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.upload.UploadBasic import (UploadBasic,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
# from com.vaadin.ui.Upload import (Upload,)
Version = Feature.Version


class UploadWithProgressMonitoring(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getDescription(self):
        return 'Uploads can be monitored with several different listeners ' + 'and the upload data can be processed during the upload. ' + 'The upload does not block the entire UI so users can ' + 'navigate to other views in the application while the ' + 'upload is progressing. Other advanced upload features ' + 'used in this demo:<ul>' + '<li>Process the file during the upload</li>' + '<li>Track events that occure during the upload</li></ul>'

    def getName(self):
        return 'Upload processing'

    def getRelatedAPI(self):
        return [APIResource(Upload), APIResource(ProgressIndicator)]

    def getRelatedFeatures(self):
        return [UploadBasic]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
