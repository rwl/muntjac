# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.table.TableMainFeaturesExample import (TableMainFeaturesExample,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TableHeaderIcons(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Table, icons in headers'

    def getExample(self):
        return TableMainFeaturesExample()

    def getDescription(self):
        return 'A Table can have icons in the column- and rowheaders. ' + ' The rowheader icon can come from a item property, or be' + ' explicitly set.'

    def getRelatedAPI(self):
        return [APIResource(Table)]

    def getRelatedFeatures(self):
        return [FeatureSet.Tables]

    def getRelatedResources(self):
        return None
