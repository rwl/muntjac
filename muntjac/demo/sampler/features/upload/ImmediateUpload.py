# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.upload.UploadBasic import (UploadBasic,)
from com.vaadin.demo.sampler.features.upload.UploadWithProgressMonitoring import (UploadWithProgressMonitoring,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class ImmediateUpload(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getDescription(self):
        return 'The upload component can be configured to work as a single-click upload, that starts right after the user has selected the file to upload.<br /><br />In this sample the upload is deliberately slow, so that even small files show the progress indicator.'

    def getName(self):
        return 'Single-click upload'

    def getRelatedAPI(self):
        return [APIResource(Upload), APIResource(ProgressIndicator)]

    def getRelatedFeatures(self):
        return [UploadBasic, UploadWithProgressMonitoring]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
