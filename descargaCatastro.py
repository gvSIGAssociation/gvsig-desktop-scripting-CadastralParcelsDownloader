# encoding: utf-8

import gvsig
from gvsig.libs.formpanel import FormPanel

import dataCatastro
reload(dataCatastro)
from dataCatastro import getProvinciasFeatureSet, getMunicipiosFeatureSet

from gestorDescargas import CatastroDownloadManager

class Panel(FormPanel):
  def __init__(self):
    FormPanel.__init__(self, gvsig.getResource(__file__, "CadastralParcels.xml"))
    self.dm = CatastroDownloadManager(self)
    fset = getProvinciasFeatureSet()
    for provincia in fset:
      value = provincia.get("PROVINCIA")#.encode("utf-8")
      self.cboProvinces.addItem(value)
    self.cboProvinces.setSelectedIndex(5)
      
  def cboProvinces_change(self, *args):
    selected = self.cboProvinces.getSelectedItem()
    enc = selected#.decode('utf-8')
    if True: #try
      self.cboMunicipalities.removeAllItems()
      fset = getMunicipiosFeatureSet(enc)
      for f in fset:
        value = f.get("MUNICIPIO")
        if f.get("PROVINCIA")==enc:
          self.cboMunicipalities.addItem(value)
    #except:
    #  self.cboMunicipalities.addItem("---")
    
def main(*args):
    l = Panel()
    l.showTool("Descarga Catastro")
    pass