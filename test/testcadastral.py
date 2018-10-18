# encoding: utf-8

import gvsig
from org.gvsig.fmap.dal import DALLocator
import os
def main(*args):
    """
    #Remove this lines and add here your code
    view = gvsig.currentView()
    gmlFilePath = "/tmp/tmp-gvsig/02025-5bc7e3530/A.ES.SDGC.CP.56101.cadastralparcel.gml"
    if not os.path.exists(gmlFilePath):
      print "fail"
      return
    manager = DALLocator.getDataManager()
    storeParameters = manager.createStoreParameters("GMLDataStoreProvider")
    #storeParameters.setDynValue("connectionString",None)
    storeParameters.setDynValue("CRS",view.getProjection())
    #storeParameters.setDynValue("defaultGeometryField",None)
    storeParameters.setDynValue("file",gmlFilePath)
    #storeParameters.setDynValue("gfsSchema",None)
    storeParameters.setDynValue("ignoreSpatialFilter",True)
    storeParameters.setDynValue("layerName","02025")
    #storeParameters.setDynValue("ProviderName",'GPE')
    #storeParameters.setDynValue("xsdSchema",None)
    store = manager.openStore("GMLDataStoreProvider",storeParameters)
    """
