# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.table.TableMainFeaturesExample import (TableMainFeaturesExample,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TableColumnAlignment(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Table, column alignment'

    def getExample(self):
        return TableMainFeaturesExample()

    def getDescription(self):
        return 'Columns can be aligned left (default), center or right.'

    def getRelatedAPI(self):
        return [APIResource(Table)]

    def getRelatedFeatures(self):
        return [FeatureSet.Tables]

    def getRelatedResources(self):
        return None
