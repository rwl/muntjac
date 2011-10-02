# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.table.TableMainFeaturesExample import (TableMainFeaturesExample,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TableSorting(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Table, sorting'

    def getExample(self):
        return TableMainFeaturesExample()

    def getDescription(self):
        return 'The Table columns can (optionally) be sorted by clicking the' + ' column header - a sort direction indicator will appear.' + ' Clicking again will change the sorting direction.'

    def getRelatedAPI(self):
        return [APIResource(Table)]

    def getRelatedFeatures(self):
        return [FeatureSet.Tables]

    def getRelatedResources(self):
        return None
