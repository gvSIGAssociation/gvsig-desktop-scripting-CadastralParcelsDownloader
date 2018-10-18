# encoding: utf-8

import gvsig
import csv
import os
from gvsig import geom

from org.gvsig.fmap.dal import DALLocator
from org.gvsig.fmap.dal import DataTypes

from org.gvsig.app import ApplicationLocator

import addons.CadastralParcelsDownloader.data
reload(addons.CadastralParcelsDownloader.data)
from addons.CadastralParcelsDownloader.data import data

def main(*args):
  #a = getMunicipiosFeatureSet(u"A CORUÑA")
  #createNewDataBaseBasicPronviciasMunicipios()
  #createNewEmptyMunicipalities()
  pass
  
def getProvinciasFeatureSet():
  manager = DALLocator.getDataManager()
  storeParameters = manager.createStoreParameters("H2Spatial")
  database_file = gvsig.getResource(__file__,"data","catastroInfo.mv.db")
  storeParameters.setDynValue("database_file",database_file)
  storeParameters.setDynValue("Table","Provincias")
  
  store = manager.openStore("H2Spatial",storeParameters)
  featureSet = store.getFeatureSet()
  return featureSet
  
def getMunicipiosFeatureSet(provincia):
  manager = DALLocator.getDataManager()
  storeParameters = manager.createStoreParameters("H2Spatial")
  database_file = gvsig.getResource(__file__,"data","catastroInfo.mv.db")
  storeParameters.setDynValue("database_file",database_file)
  storeParameters.setDynValue("Table","Municipios")
  
  store = manager.openStore("H2Spatial",storeParameters)
  #try:  query = u"""CODPROV='{0}'""".format(provincia)
  #  featureSet = store.getFeatureSet(query)
  #except:
  featureSet = store.getFeatureSet()
  return featureSet
  
def createNewEmptyMunicipalities():
  database_file = gvsig.getTempFile("/home/osc/temp/h2/municipalities",".mv.db")
  print "** DATABASE FILE_: ", database_file
  # Create store
  manager = DALLocator.getDataManager()
  serverParameters = manager.createServerExplorerParameters("H2Spatial")
  serverParameters.setDynValue("database_file",database_file)
  serverExplorer = manager.openServerExplorer("H2Spatial",serverParameters)
  p = serverExplorer.getAddParameters()
  p.setDynValue("Table","Muni")
  ft = manager.createFeatureType()
  # "CODPROV","PROV","CODMUN","MUN","ID"
  ft.add("CODPROV", DataTypes.STRING)
  ft.add("PROV", DataTypes.STRING)
  ft.add("CODMUN", DataTypes.STRING)
  ft.add("MUN", DataTypes.STRING)
  ft.add("ID", DataTypes.STRING)
  ft.add("gml_id", DataTypes.STRING)
  ft.add("GEOMETRY", DataTypes.GEOMETRY) #Geometry.TYPES.CURVE)
  ft.get("GEOMETRY").setGeometryType(geom.POLYGON, geom.D2)
  ft.get("GEOMETRY").setSRS(gvsig.currentView().getProjection())
  p.setDefaultFeatureType(ft)
  serverExplorer.add("H2Spatial", p, True)
  
def createNewDataBaseBasicPronviciasMunicipios():
  database_file = gvsig.getTempFile("/home/osc/temp/h2/catas",".mv.db")
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
  ft.add("CODPROV", DataTypes.STRING)
  ft.add("PROV", DataTypes.STRING)
  ft.add("CODMUN", DataTypes.STRING)
  ft.add("MUN", DataTypes.STRING)
  ft.add("ID", DataTypes.STRING)
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

  csvFilePath = gvsig.getResource(__file__,"data","dataMunicipalities.csv")
  if not os.path.exists(csvFilePath):
    print "not found"
    return None
  with open(csvFilePath, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',') #, quotechar='|')
    for row in spamreader:
      d = {}
      d["CODPROV"]=row[0].decode('utf-8')
      d["PROV"]=row[1].decode('utf-8')
      d["CODMUN"]=row[2].decode('utf-8')
      d["MUN"]=row[3].decode('utf-8')
      d["ID"]=row[4].decode('utf-8')
      store.append(d)
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