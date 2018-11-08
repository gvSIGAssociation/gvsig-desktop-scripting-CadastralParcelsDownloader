# encoding: utf-8

import gvsig

import os.path

from os.path import join, dirname

from gvsig import currentView
from gvsig import currentLayer

from java.io import File

from org.gvsig.app import ApplicationLocator
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools.swing.api import ToolsSwingLocator

from cadastralDownloader import CadastralDownloaderPanel

from org.gvsig.tools import ToolsLocator

class CadastralDownloaderExtension(ScriptingExtension):
  def __init__(self):
    pass

  def isVisible(self):
    return True

  def isLayerValid(self, layer):
    return True
    
  def isEnabled(self):
    layer = currentLayer()
    if not self.isLayerValid(layer):
      return False
    return True

  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "settool-cadastralparcelsdownloader":
      #print "### QuickinfoExtension.execute(%s)" % repr(actionCommand)
      layer = currentLayer()
      if not self.isLayerValid(layer):
        return
      viewPanel = currentView().getWindowOfView()
      mapControl = viewPanel.getMapControl()
      cadastral = CadastralDownloaderPanel()
      #cadastral.setTool(mapControl)
      cadastral.showTool("_Cadastral_Parcels_Downloader")

def selfRegister():
  i18n = ToolsLocator.getI18nManager()
  application = ApplicationLocator.getManager()
  actionManager = PluginsLocator.getActionInfoManager()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()

  cadastralparcelsdownloader_icon = File(gvsig.getResource(__file__,"images","cadastralparcelsdownloader.png")).toURI().toURL()
  iconTheme.registerDefault("scripting.cadastralparcelsdownloader", "action", "tools-cadastralparcelsdownloader", None, cadastralparcelsdownloader_icon)

  cadastralparcelsdownloader_extension = CadastralDownloaderExtension()
  cadastralparcelsdownloader_action = actionManager.createAction(
    cadastralparcelsdownloader_extension,
    "tools-cadastralparcelsdownloader",   # Action name
    "Show cadastral parcels downloader",   # Text
    "settool-cadastralparcelsdownloader", # Action command
    "tools-cadastralparcelsdownloader",   # Icon name
    None,                # Accelerator
    1009000000,          # Position
    i18n.getTranslation("_Show_cadastral_parcels_downloader")    # Tooltip
  )
  cadastralparcelsdownloader_action = actionManager.registerAction(cadastralparcelsdownloader_action)

  # Añadimos la entrada "Quickinfo" en el menu herramientas
  application.addMenu(cadastralparcelsdownloader_action, "tools/_cadastralparcelsdownloader")
  # Añadimos el la accion como un boton en la barra de herramientas "Quickinfo".
  application.addSelectableTool(cadastralparcelsdownloader_action, "CadastralParcelsDownloader")

def main(*args):
  selfRegister()
  