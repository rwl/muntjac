# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.table.TableMainFeaturesExample import (TableMainFeaturesExample,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TableActions(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Table, context menu'

    def getExample(self):
        return TableMainFeaturesExample()

    def getDescription(self):
        return 'Actions can be added to each row, and are show in a' + ' context menu when right-clicking.'

    def getRelatedAPI(self):
        return [APIResource(Table)]

    def getRelatedFeatures(self):
        return [FeatureSet.Tables]

    def getRelatedResources(self):
        return None
