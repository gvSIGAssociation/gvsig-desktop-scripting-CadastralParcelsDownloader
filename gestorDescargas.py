# encoding: utf-8

import gvsig
from org.gvsig.andami import Utilities
from java.lang import Thread
import threading

import os

import pprint, os, urllib2, base64

def download(url):
    request = urllib2.Request(url)
    #base64string = base64.b64encode('%s:%s' % (username, password))
    #request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib2.urlopen(request)
    return result
    
"""
class SentinelThread(Thread):
  def __init__(self):
    pass
    
  def run(self, args):
    self.ui._updateListValues()

def main(*args):
    m = Mythread()
    m.start()
"""

class CatastroDownloadManager():
    def __init__(self, app=None):
      self.app = app
      self.st = None
      self.downloadList={} #name, url
      self.downloaded={}
      self.working=False
      self.stopThread=False
      
    def getDownloaded(self):
      return self.downloaded
      
    def addDownload(self, value, url):
       self.downloadList[value]=url
       if self.working==False: 
          self.working=True
          self.setWorking()
       
    def getDownloadPath(self):
      return Utilities.TEMPDIRECTORYPATH
    
    def getNewThread(self):
      #self.st= SentinelThread()
      pass
    def download(self, value, url):
      print "Downloading... ", value
      self.setWorking(True)
      f = download(url)
      total_size = int(f.headers["Content-Length"])
      MB_size = round(total_size/1048576, 2)
      block_size = 1024 * 1024
      outputPathFull=os.path.join(self.getDownloadPath(),value+".gml")
      with open(outputPathFull, "wb") as file:
        while True:
          block = f.read(block_size)
          dSize =  round(int(os.stat(outputPathFull).st_size)/1048576, 2)
          statusText = " (" + str(dSize) + "/" + str(MB_size) + " MB) " + " Downloading.."+ value # +  url + "Downloading"
          if self.app != None:
            self.app.txtStatus.setText(statusText)
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
      print "** DONE"
      self.setDownloadFinished(value, url)
      
    def setStopThread(self, status=False):
      self.stopThread = status
      if self.app!=None:
          self.app.txtStatus.setText("")
      
    def setDownloadFinished(self, value, url):
      print "********* Finished: ", value
      print self.downloadList, value in self.downloadList
      print self.downloaded
      self.downloadList.pop(value)
      self.downloaded[value]=url
      print self.downloadList, value in self.downloadList
      print self.downloaded
      print "***"
      self.setWorking(False)

       
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
      url = self.downloadList[value]
      #self.downloadList.pop(value)
      threading.Thread(target=self.download, name="DownloadCatastro", args=(value, url)).start()

def main(*args):

    s = CatastroDownloadManager()
    print s.getDownloadPath()
    href="http://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx?service=wfs&request=getfeature&Typenames=cp.cadastralparcel&SRSname=EPSG::25830&bbox=233673,4015968,233761,4016008"
    s.addDownload("S1", href)
    