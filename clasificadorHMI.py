# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 11:26:45 2016

@author: dpbou

Clasificador de imagenes mediante intervención del usuario
"""



import argparse
ap = argparse.ArgumentParser(
    description = "Clasificador de imagenes. Es necesario incluir en linea de comando la imagen o directorio a procesar.")
grupo =  ap.add_mutually_exclusive_group(required=True)
grupo.add_argument("-i", "--imagen", help="path de la imagen a procesar")
grupo.add_argument("-d", "--directorio", help="path del directorio a procesar")
ap.add_argument("-o", "--output", help="path del archivo resultado")

args = vars(ap.parse_args())
opts = ap.parse_args()

import utilidades_archivos
import cv2
import json

# Muestra la imagen y solicita al usuario que indique si contiene una grieta o no
# imagen: string que contiene el path de la imagen
# retorna: bool, True si el usuario indica que contiene una imagen
def pedirClasificacion(imagen):
    orig = cv2.imread(imagen)
    cv2.putText(orig, "Contiene grieta (Si/No)?", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imshow("Clasificacion", orig)
    tecla = cv2.waitKey()
    if tecla==ord('S') or tecla==ord('s') or tecla==ord('Y') or tecla==ord('y'):
        return True
    else:
        return False

# Guarda a disco la lista de pares {imagen:str, esGrieta:bool}
def guardaLista(lista, archivoSalida):
    print(lista)
    with open(archivoSalida, 'w') as outfile:
        json.dump(lista, outfile)
        
#-------------------------------------------------------------------------
if __name__=="__main__":
    lista_imagenes = []
    if args['imagen'] == None : #Imanen nula --> directorio
        if opts.directorio[-1]=='/': 
            miDir = opts.directorio[:-1]
        else:
            miDir = opts.directorio    
        lista_imagenes = utilidades_archivos.lista_imagenes_directorio(miDir)
    else: #Imagen no es nulo
        lista_imagenes.append(args['imagen'])
    
print("[BOU-INFO] Lista de imágenes a procesar:")
print (lista_imagenes)

#Empieza el procesado de la lista de imágenes
listaClasificada = []
for imagen in lista_imagenes:
    esGrieta = pedirClasificacion(imagen)
    listaClasificada.append([imagen, esGrieta])

#guardar la lista en archivo
if opts.output==None:
    archivoSalida  = "clasificacion.json"
else:
    archivoSalida = opts.output
guardaLista(listaClasificada, archivoSalida)
#Fin main
    
