# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.table.TableMainFeaturesExample import (TableMainFeaturesExample,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TableColumnReordering(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Table, column drag&drop'

    def getExample(self):
        return TableMainFeaturesExample()

    def getDescription(self):
        return 'The columns can be rearranged with drag&drop - a feature' + ' which can be enabled or disabled.'

    def getRelatedAPI(self):
        return [APIResource(Table)]

    def getRelatedFeatures(self):
        return [FeatureSet.Tables]

    def getRelatedResources(self):
        return None
