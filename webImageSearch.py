# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 11:00:33 2016

@author: dpbou

MANUAL:
Modificar la lista de palabras clave y ejecutar a pelo, sin parametros. 
Cuidado con las dos constantes que definen el numero de fotos y el directorio destino.

Baja NUMERO_FOTOS_POR_BUSQUEDA por cada palabra existente en lista_palabras_clave
Las graba todas (con la extension mostrada en la URL) en la carpeta PATH_BD_FOTOS

Solo cazo las excepciones al hacer el download del archivo. Si salta alguna, simplemente 
la imprimo y sigo
"""

import urllib2
from googleapiclient.discovery import build
import sys

lista_palabras_clave = ["asfalto",
                        "asphalt",
                        "asphalt crack",
                        "grieta en asfalto"]

NUMERO_FOTOS_POR_BUSQUEDA = 100
PATH_BD_FOTOS = "/home/dpbou/DRONES/mnto_asfalto/pruebas_cnn/bdImagenes/"

def main():
    contador=0
    listaLinks = []
    for q in lista_palabras_clave:
        for pag in range(NUMERO_FOTOS_POR_BUSQUEDA // 10): #las busquedas de google van por paginas y cada pagina son solo 10 resultados
            res = disparaBusqueda(q, pag)
            i=0
            for item in res["items"]:
                i=i+1
                if i>NUMERO_FOTOS_POR_BUSQUEDA: 
                    break
                listaLinks.append(item["link"])
                contador = contador+1
            #fin_for
        #fin_for
    #fin_for
    print "[BOU-Info: Total imagenes encontradas: %s" % len(listaLinks)
    c = 0
    for i in listaLinks: 
        c = c+1
        fileName = str(c).zfill(8) #mete ceros por delante
        fileName = fileName + '.' + str(i).split('.')[-1]
        saveImageFile(i, fileName)
    #fin_for
                
  
def saveImageFile(imageURL, fileName):
    try:
        opener = urllib2.build_opener()
        opener.addheaders= [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36')]
        response = opener.open(imageURL)
        htmlData = response.read()
        f = open(PATH_BD_FOTOS + fileName, 'w')
        f.write(htmlData)
        f.close()
    except:
        print "[BOU-ERROR]: excepcion en saveImageFile: ", sys.exc_info()[0]
        #raise
    
    
def disparaBusqueda(consulta, pagina):
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  # https://console.developers.google.com/apis/dashboard?project=busquedaimagenes-141511&duration=PT1H
  service = build("customsearch", "v1",
            developerKey="AIzaSyDpmTrmWQbboayv_il_zGL4uEjZmUZ3mBQ") #clave que tengo como desarrollador en google
  res = service.cse().list(
      q = consulta,
      searchType = 'image',
      cx='017582315910912310424:wjdsjfiv_pc', # clave del motor de búsqueda que he dado de alta en google (https://cse.google.com/cse/all)
      start=(pagina*10)+1
    ).execute()
  print "[BOU-Info: Consulta realizada con %s resultados, query='%s'" % (res["searchInformation"]["totalResults"], consulta)
  return res    


if __name__ == '__main__':
    main()
    print "[BOU-ESTADO] FIN EJECUCION "