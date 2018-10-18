# encoding: utf-8

import gvsig
from gvsig import getResource

import actions
reload(actions)

from org.gvsig.tools import ToolsLocator
from java.io import File

from patchs.fixformpanel import fixFormPanelResourceLoader

def main(*args):
  fixFormPanelResourceLoader()
  i18nManager = ToolsLocator.getI18nManager()
  i18nManager.addResourceFamily("text",File(getResource(__file__,"i18n")))
  
  actions.selfRegister()
    