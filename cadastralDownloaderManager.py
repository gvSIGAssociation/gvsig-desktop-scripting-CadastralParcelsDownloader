# encoding: utf-8

import gvsig
from org.gvsig.andami import Utilities
from java.lang import Thread
import threading
import zipfile
import os

import pprint, os, urllib2, base64

from org.gvsig.fmap.dal import DALLocator
from java.lang import Object
from org.gvsig.app import ApplicationLocator

class OMunicipality(Object):
  def __init__(self,f):
    self.codprov = f[0]
    self.prov = f[1]
    self.codmun = f[2]
    self.mun = f[3]
    self.id = f[4]
  def getMun(self):
    return self.mun
  def getProv(self):
    return self.prov
  def getCodProv(self):
    return self.codprov
  def getCodMun(self):
    return self.codmun
  def getId(self):
    return self.id
  def toString(self):
    return self.mun
    
def download(url):
    request = urllib2.Request(url)
    #base64string = base64.b64encode('%s:%s' % (username, password))
    #request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib2.urlopen(request)
    return result
    

class CadastralDownloaderManager():
  def __init__(self, view, app=None):
    self.app = app
    self.view = view
    self.st = None
    self.downloadList={} #name, url
    self.downloaded={}
    self.working=False
    self.stopThread=False
    
  def getDownloaded(self):
    return self.downloaded
    
  def addDownload(self, value, url, oml):

     self.downloadList[value]=[url, oml]
     if self.working==False: 
        self.working=True
        self.setWorking()
     
  def getDownloadPath(self):
    return Utilities.TEMPDIRECTORYPATH
  
  def getNewThread(self):
    #self.st= SentinelThread()
    pass
    
  def download(self, value, url, oml):
    print "Downloading... ", value
    self.setWorking(True)
    f = download(url)
    total_size = int(f.headers["Content-Length"])
    MB_size = round(total_size/1048576, 2)
    block_size = 1024 * 1024
    outputPathFull=os.path.join(self.getDownloadPath(),value+".zip")
    with open(outputPathFull, "wb") as file:
      while True:
        block = f.read(block_size)
        dSize =  round(int(os.stat(outputPathFull).st_size)/1048576, 2)
        statusText = " (" + str(dSize) + "/" + str(MB_size) + " MB) " + " Downloading.."+ value # +  url + "Downloading"
        if self.app != None:
          self.app.txtDownloadStatus.setText(statusText)
        if self.stopThread==True:
          self.setStopThread()
          break
        else:
          print statusText
        if not block:
          break
        file.write(block)
        
    if self.stopThread==True:
      os.remove(outputPathFull)
    
    self.setDownloadFinished(value, url, oml, outputPathFull)
    
  def setStopThread(self, status=False):
    self.stopThread = status
    if self.app!=None:
        self.app.txtDownloadStatus.setText("")
    
  def setDownloadFinished(self, value, url, oml, outputPathFull):
    self.downloadList.pop(value)
    self.downloaded[value]=url
    self.setWorking(False)
    self.loadFileIntoH2(oml, outputPathFull)

  def loadFileIntoH2(self, oml, outputPathFull):
    print "done"
    path=gvsig.getTempFile(oml.getCodMun(),'')#os.path.join(self.getDownloadPath(),oml.get)
    print "PATH FOR GML:", path
    os.mkdir(path)
    
    zip_ref = zipfile.ZipFile(outputPathFull, 'r')
    zip_ref.extractall(path)
    zip_ref.close()
    gmlFile = 'A.ES.SDGC.CP.{0}.cadastralparcel.gml'.format(oml.getCodMun())
    gmlFilePath = os.path.join(path, gmlFile)
    if not os.path.exists(gmlFilePath):
      print "fail"
      return
    manager = DALLocator.getDataManager()
    storeParameters = manager.createStoreParameters("GMLDataStoreProvider")
    #storeParameters.setDynValue("connectionString",None)
    storeParameters.setDynValue("CRS",self.view.getProjection())
    #storeParameters.setDynValue("defaultGeometryField",None)
    storeParameters.setDynValue("file",gmlFilePath)
    #storeParameters.setDynValue("gfsSchema",None)
    storeParameters.setDynValue("ignoreSpatialFilter",True)
    storeParameters.setDynValue("layerName",oml.getCodMun())
    #storeParameters.setDynValue("ProviderName",None)
    #storeParameters.setDynValue("xsdSchema",None)
    store = manager.openStore("GMLDataStoreProvider",storeParameters)
    
    application = ApplicationLocator.getManager()
    mapcontextmanager = application.getMapContextManager()
    layer = mapcontextmanager.createLayer(oml.getId(),store)
    self.view.addLayer(layer)

    # Open Store
    storeParameters = manager.createStoreParameters("H2Spatial")
    database_file=gvsig.getResource(__file__, "data", "municipalities.mv.db")
    storeParameters.setDynValue("database_file",database_file)
    storeParameters.setDynValue("Table","Muni")
    storeH2 = manager.openStore("H2Spatial",storeParameters)
    storeH2.edit()
    for f in store:
      value = {
        'CODPROV': oml.getCodProv(),
        'PROV': oml.getProv(),
        'CODMUN': oml.getCodMun(),
        'MUN': oml.getMun(),
        'ID': oml.getId(),
        'gml_id': f.get('gml_id'),
        'GEOMETRY': f.getDefaultGeometry()
        }
      storeH2.append(value)
    storeH2.commit()
  
    
  def setWorking(self, state=None):
    self.working=True
    if state==False or state==None:
      if len(self.downloadList.keys())>0:
        self.working = True
        self.downloading()
      else:
        self.working = False
    elif state==True:
      self.working = True
    
  def downloading(self):
    value = self.downloadList.keys()[0]
    url = self.downloadList[value][0]
    oml = self.downloadList[value][1]
    #self.downloadList.pop(value)
    threading.Thread(target=self.download, name="DownloadCatastro", args=(value, url, oml)).start()

  def getCadastralLink(self, oml):
    #ObjectListMunicipality
    #"CODPROV","PROV","CODMUN","MUN","ID"
    v1 = oml.getCodProv()
    v2 = oml.getCodMun()
    v3 = oml.getMun()
    link = 'http://www.catastro.minhap.es/INSPIRE/CadastralParcels/{0}/{1}-{2}/A.ES.SDGC.CP.{1}.zip'.format(
      v1,
      v2,
      v3)
    return link
  
def main(*args):

  s = CadastralDownloaderManager(gvsig.currentView())
  print s.getDownloadPath()
  #href="http://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx?service=wfs&request=getfeature&Typenames=cp.cadastralparcel&SRSname=EPSG::25830&bbox=233673,4015968,233761,4016008"
  #s.addDownload("S1", href)
  href="http://www.catastro.minhap.es/INSPIRE/CadastralParcels/56/56101-MELILLA/A.ES.SDGC.CP.56101.zip"
  #href=prepareCadastralLink()
  oml=OMunicipality(['02','Albacete','02025','CAUDETE','02025-CAUDETE'])
  
  s.addDownload("S2", href, oml)