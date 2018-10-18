# encoding: utf-8

import gvsig
from gvsig.libs.formpanel import FormPanel

#import dataCatastro
#reload(dataCatastro)

from dataCatastro import getProvinciasFeatureSet, getMunicipiosFeatureSet
from org.gvsig.fmap.dal import DALLocator
from cadastralDownloaderManager import CadastralDownloaderManager
from java.lang import Object
from javax.swing.table import DefaultTableModel
class ObjectListProvince(Object):
  def __init__(self, province, cod):
    self.province = province
    self.code = cod
  def getCode(self):
    return self.code
  def toString(self):
    return self.province
    
class ObjectListMunicipality(Object):
  def __init__(self,f):
    self.codprov = f.get("CODPROV")
    self.prov = f.get("PROV")
    self.codmun = f.get("CODMUN")
    self.mun = f.get("MUN")
    self.id = f.get("ID")
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
    
class CadastralDownloaderPanel(FormPanel):
  def __init__(self):
    FormPanel.__init__(self, gvsig.getResource(__file__, "CadastralParcels.xml"))
    self.dm = CadastralDownloaderManager(gvsig.currentView(), self)
    fset = getProvinciasFeatureSet()
    for provincia in fset:
      p = provincia.get("PROVINCIA")#.encode("utf-8")
      v = provincia.get("CODIGO")
      prv = ObjectListProvince(p, v)
      self.cboProvinces.addItem(prv)
    #self.cboProvinces.setSelectedIndex(5)
    # Tabla
    model = self.tblMunicipalities.getModel()
    model.addColumn("Municipio")
    model.addColumn("Codigo")
    model.addColumn("Fecha")
    self.updateTable()

  def updateTable(self):
    model = DefaultTableModel() #self.tblMunicipalities.getModel()
    manager = DALLocator.getDataManager()
    model.addColumn("CODMUN")
    model.addColumn("MUN")
    model.addColumn("FECHA")
    storeParameters = manager.createStoreParameters("H2Spatial")
    database_file=gvsig.getResource(__file__, "data", "municipalities.mv.db")
    storeParameters.setDynValue("database_file",database_file)
    storeParameters.setDynValue("Table","Muni")
    storeH2 = manager.openStore("H2Spatial",storeParameters)
    muns = {}
    for f in storeH2:
        if not f.get("CODMUN") in muns.keys():
          muns[f.get("CODMUN")] = [f.get("MUN"),f.get("CODMUN"),'']
    for k in muns.keys():
      model.addRow(muns[k])

    self.tblMunicipalities.setModel(model)

  def btnUpdateMunicipality(self,*args):
    self.updateTable()
    
  def cboProvinces_change(self, *args):
    selected = self.cboProvinces.getSelectedItem()
    enc = selected.getCode()#.decode('utf-8')
    if True: #try
      self.cboMunicipalities.removeAllItems()
      fset = getMunicipiosFeatureSet(enc)
      for f in fset:
        itemM = ObjectListMunicipality(f)
        if f.get("CODPROV")==enc:
          self.cboMunicipalities.addItem(itemM)
    #except:
    #  self.cboMunicipalities.addItem("---")
  def btnDownloadMunicipality_click(self, *args):
    #province = self.cboProvinces.getSelectedItem()
    municipality = self.cboMunicipalities.getSelectedItem()
    url = self.dm.getCadastralLink(municipality)
    self.dm.addDownload(municipality.getCodMun(), url, municipality)
    
    
def main(*args):
    l = CadastralDownloaderPanel()
    l.showTool("_Cadastral_Downloader")
    pass