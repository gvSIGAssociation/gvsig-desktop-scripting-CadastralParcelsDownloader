# encoding: utf-8

import gvsig
from org.gvsig.fmap.dal import DALLocator
from org.gvsig.fmap.dal import DataTypes

from org.gvsig.app import ApplicationLocator

import addons.DescargaCatastro.data
reload(addons.DescargaCatastro.data)
from addons.DescargaCatastro.data import data

def main(*args):
  #a = getMunicipiosFeatureSet(u"A CORUÑA")
  createNewDataBaseBasicPronviciasMunicipios()
def getProvinciasFeatureSet():
  manager = DALLocator.getDataManager()
  storeParameters = manager.createStoreParameters("H2Spatial")
  database_file = gvsig.getResource(__file__,"data","catastroInfo1.mv.db")
  storeParameters.setDynValue("database_file",database_file)
  storeParameters.setDynValue("Table","Provincias")
  
  store = manager.openStore("H2Spatial",storeParameters)
  featureSet = store.getFeatureSet()
  return featureSet
  
def getMunicipiosFeatureSet(provincia):
  manager = DALLocator.getDataManager()
  storeParameters = manager.createStoreParameters("H2Spatial")
  database_file = gvsig.getResource(__file__,"data","catastroInfo1.mv.db")
  storeParameters.setDynValue("database_file",database_file)
  storeParameters.setDynValue("Table","Municipios")
  #try:
  store = manager.openStore("H2Spatial",storeParameters)
  query = u"""PROVINCIA='{0}'""".format(provincia)
  featureSet = store.getFeatureSet(query)
  #except:
  #featureSet = store.getFeatureSet()
  return featureSet
  
def createNewDataBaseBasicPronviciasMunicipios():
  database_file = gvsig.getTempFile("/home/osc/temp/h2/catastroInfo",".mv.db")
  print "** DATABASE FILE_: ", database_file
  # Create store
  manager = DALLocator.getDataManager()
  serverParameters = manager.createServerExplorerParameters("H2Spatial")
  serverParameters.setDynValue("database_file",database_file)
  serverExplorer = manager.openServerExplorer("H2Spatial",serverParameters)
  p = serverExplorer.getAddParameters()
  p.setDynValue("Table","Provincias")
  ft = manager.createFeatureType()
  ft.add("CODIGO", DataTypes.STRING)
  ft.add("PROVINCIA", DataTypes.STRING)
  p.setDefaultFeatureType(ft)
  serverExplorer.add("H2Spatial", p, True)
  
  p = serverExplorer.getAddParameters()
  p.setDynValue("Table","Municipios")
  ft = manager.createFeatureType()
  ft.add("PROVINCIA", DataTypes.STRING)
  ft.add("MUNICIPIO", DataTypes.STRING)
  p.setDefaultFeatureType(ft)
  serverExplorer.add("H2Spatial", p, True)

  
  # Open Store
  storeParameters = manager.createStoreParameters("H2Spatial")
  storeParameters.setDynValue("database_file",database_file)
  storeParameters.setDynValue("Table","Provincias")
  
  store = manager.openStore("H2Spatial",storeParameters)
  store.edit()
  for p in data.getProvincias():
    value = p[1] #.encode('utf-8')
    store.append({ "CODIGO":p[0], "PROVINCIA":value})
  store.commit()
  

  #for i in store.getFeatureSet():
  #  print i.get('PROVINCIA=')#.encode("utf-8")
  
  
  storeParameters = manager.createStoreParameters("H2Spatial")
  storeParameters.setDynValue("Table","Municipios")
  storeParameters.setDynValue("database_file",database_file)
  
  store = manager.openStore("H2Spatial",storeParameters)
  store.edit()
  provincias = data.getProvincias()
  for p in provincias:
    provincia = p[1]#.encode('utf-8')
    print provincia
    try: #if True:
      municipios = data.getMunicipios(provincia)
      for m in municipios:
        store.append({ "PROVINCIA":provincia, "MUNICIPIO":m})
    except:
      print "** Error url: ", provincia
  store.commit()
  
  for n,f in enumerate(store):
    print f
    if n==100:
      break
  #Create layer
  return
  application = ApplicationLocator.getManager()
  mapcontextmanager = application.getMapContextManager()
  layer = mapcontextmanager.createLayer("Layer H2",store)