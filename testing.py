# encoding: utf-8

import gvsig
from org.gvsig.fmap.dal import DALLocator

def main(*args):

    manager = DALLocator.getDataManager()
    storeParameters = manager.createStoreParameters("H2Spatial")
    database_file=gvsig.getResource(__file__, "data", "municipalities.mv.db")
    storeParameters.setDynValue("database_file",database_file)
    storeParameters.setDynValue("Table","Muni")
    storeH2 = manager.openStore("H2Spatial",storeParameters)
    print storeH2, dir(storeH2)