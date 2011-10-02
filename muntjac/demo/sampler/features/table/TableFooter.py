# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.table.TableFooterExample import (TableFooterExample,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TableFooter(Feature):

    def getDescription(self):
        return 'The Table footers can be used to add captions below each column.'

    def getName(self):
        return 'Table, column footers'

    def getRelatedAPI(self):
        return [APIResource(Table)]

    def getRelatedFeatures(self):
        return [FeatureSet.Tables]

    def getRelatedResources(self):
        return None

    def getSinceVersion(self):
        return Version.V64

    def getExample(self):
        return TableFooterExample()
