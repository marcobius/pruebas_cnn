# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 11:19:50 2016

@author: dpbou

Uilidades varias para manejo de archivos de imagenes y directorios
"""
import fnmatch
import os
import random
import cv2

# Funcion que recorre el directorio dado y genera n sub-imagenes por cada una econtrada
#   n dependera del tamaño de las imagenes originales y 
#   de las dimensiones solicitadas para las nuevas
#   pref es el prefijo a añadir a las imágenes generadas
def genera_subimagenes_directorio(directorio, dimx, dimy, pref="gen_"):
    #Obtener lista imagenes
    if directorio[-1]=='/': 
        miDir = directorio[:-1]
    else:
        miDir = directorio
    lista_arc = lista_imagenes_directorio(directorio)
    #Para cada imagen genero las subimagenes
    lista_img = []
    lista_errores = []
    for i in lista_arc:
        ok, error = lista_img.append(genera_subimagenes_archivo(i, dimx, dimy, miDir + "/" + pref))
        if ok==False: 
            lista_errores.append(error)
    return lista_errores


def genera_subimagenes_archivo(archivo, dimx, dimy, pref="gen_"):
    #comprueba que existe archivo
    #carga archivo
    img = cv2.imread(archivo)
    #comprueba cuantas fotos podemos sacar MAS O MENOS
    altura, anchura, profundidad = img.shape
    if altura < dimy or anchura < dimx:
        return False, archivo + "\n--> Dimensiones de imagen (%d, %d) incompatibles con dimensiones solicitadas (%d, %d)" % (anchura, altura, dimx, dimy)
    nfotos = (altura // dimy) * (anchura // dimx)
    #genera fotos
    lista_img=[]
    j = 0
    for i in range (nfotos):
        j=j+1
        x = random.randrange(0, anchura - dimx)
        y = random.randrange(0, altura - dimy)
        crop_img = img[y:y+dimy, x:x+dimx]
        lista_img.append(crop_img)
        cv2.imwrite(pref + "imagen_%d.png" %(j), crop_img)
    #devuelve imagenes
    return True, None
    
    
#Lista todos los archivos de imagenes que OpenCV es capaz de cargar
def lista_imagenes_directorio(directorio):
    assert directorio!=None
    if directorio[-1]=='/': 
        miDir = directorio[:-1]
    else:
        miDir = directorio
    lista_imagenes = []
    for file in os.listdir(miDir):
        if fnmatch.fnmatch(file, '*.bmp'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.dib'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.jpeg'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.jpg'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.jp2'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.png'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.webp'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.pbm'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.pgm'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.ppm'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.sr'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.ras'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.tiff'):
            lista_imagenes.append(file)
        if fnmatch.fnmatch(file, '*.tif'):
            lista_imagenes.append(file)
    #Añado el path delante a las imagenes a cargar
    for i in range(len(lista_imagenes)):
        lista_imagenes[i] = miDir + '/' + lista_imagenes[i]
    return lista_imagenes
