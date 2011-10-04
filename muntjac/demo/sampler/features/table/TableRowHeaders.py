# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.table.TableMainFeaturesExample import (TableMainFeaturesExample,)
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TableRowHeaders(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Table, row headers'

    def getExample(self):
        return TableMainFeaturesExample()

    def getDescription(self):
        return 'A Table can have row headers, which support different modes' + ' with automatic or explicitly set caption and/or icon.'

    def getRelatedAPI(self):
        return [APIResource(Table)]

    def getRelatedFeatures(self):
        return [FeatureSet.Tables]

    def getRelatedResources(self):
        return None
