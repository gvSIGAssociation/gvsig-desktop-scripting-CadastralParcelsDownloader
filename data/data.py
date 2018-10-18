# encoding: utf-8

import gvsig

# http://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx
import csv
import os
import urllib2
from xml.etree import ElementTree as ET

def getProvincias():
  provincias = [
                ['15',u'A CORUÑA'],
                ['03',u'ALACANT'],
                ['02',u'ALBACETE'],
                ['04',u'ALMERIA'],
                ['33',u'ASTURIAS'],
                ['05',u'AVILA'],
                ['06',u'BADAJOZ'],
                ['08',u'BARCELONA'],
                ['09',u'BURGOS'],
                ['10',u'CACERES'],
                ['11',u'CADIZ'],
                ['39',u'CANTABRIA'],
                ['12',u'CASTELLO'],
                ['51',u'CEUTA'],
                ['13',u'CIUDAD REAL'],
                ['14',u'CORDOBA'],
                ['16',u'CUENCA'],
                ['17',u'GIRONA'],
                ['18',u'GRANADA'],
                ['19',u'GUADALAJARA'],
                ['21',u'HUELVA'],
                ['22',u'HUESCA'],
                ['07',u'ILLES BALEARS'],
                ['23',u'JAEN'],
                ['26',u'LA RIOJA'],
                ['35',u'LAS PALMAS'],
                ['24',u'LEON'],
                ['25',u'LLEIDA'],
                ['27',u'LUGO'],
                ['28',u'MADRID'],
                ['29',u'MALAGA'],
                ['52',u'MELILLA'],
                ['30',u'MURCIA'],
                ['32',u'OURENSE'],
                ['34',u'PALENCIA'],
                ['36',u'PONTEVEDRA'],
                ['38',u'S.C. TENERIFE'],
                ['37',u'SALAMANCA'],
                ['40',u'SEGOVIA'],
                ['41',u'SEVILLA'],
                ['42',u'SORIA'],
                ['43',u'TARRAGONA'],
                ['44',u'TERUEL'],
                ['45',u'TOLEDO'],
                ['46',u'VALENCIA'],
                ['47',u'VALLADOLID'],
                ['49',u'ZAMORA'],
                ['50',u'ZARAGOZA']
                ]
  return provincias


def download(url):
    request = urllib2.Request(url)
    result = urllib2.urlopen(request)
    return result
    
def downloadXMLQuery(url):
    #try:
    outputPath=gvsig.getTempFile("municipioXML", ".xml") 
    f = download(url)
    #total_size = int(f.headers["Content-Length"])
    #MB_size = round(total_size/1048576, 2)
    block_size = 1024 * 1024
    with open(outputPath, "wb") as file:
      while True:
        block = f.read(block_size)
        dSize =  round(int(os.stat(outputPath).st_size)/1048576, 2)
        #print "(" + str(dSize) + "/" + str(MB_size) + " MB) " +  url + "Downloading"
        if not block:
          break
        file.write(block)
    return outputPath
    #except:
    #  return None


def xmlCatastroReader(xml):
  tree = ET.parse(xml)
  root = tree.getroot()
  products = []
  for child in root:
    #print "TAG:", child.tag#, child.attrib
    ### ENTRY
    childInfo = {}
    if child.tag=="{http://www.catastro.meh.es/}municipiero":
      for c in child:
        #print c.tag, c.attrib, c.text
        if c.tag=="{http://www.catastro.meh.es/}muni":
          for i in c:
            if i.tag=="{http://www.catastro.meh.es/}nm":
                products.append(i.text)
  return products
  
def getMunicipios(provincia):
  basicUrl = 'http://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx/ConsultaMunicipio?Provincia={0}&Municipio='
  url = basicUrl.format(provincia.encode("utf-8"))
  url = url.replace(" ","%20")
  print url
  
  query = downloadXMLQuery(url)
  reader = xmlCatastroReader(query)
  return reader

def getMinucipalitiesFromCsv():
  csvFilePath = gvsig.getResource(__file__,"dataMunicipalities.csv")
  if not os.path.exists(csvFilePath):
    print "not found"
    return None
  n = 0
  print n
  with open(csvFilePath, 'rb') as csvfile:
   spamreader = csv.reader(csvfile, delimiter=',') #, quotechar='|')
   for row in spamreader:
     print row
     for i in row:
        print i.decode('utf-8')
     print ', '.join(row)
     n+=1
     if n>20:
       break
  print n
def main(*args):
  #print getProvincias()
  #print getMunicipios(u"A CORUÑA")
  getMinucipalitiesFromCsv()

  