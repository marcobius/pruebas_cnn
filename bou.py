# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 10:25:15 2016

@author: dpbou
"""
#Parser de argumentos
# Lo coloco antes para evitar la carga innecesaria de librerías
import argparse
ap = argparse.ArgumentParser(
    description = "Clasificador de imagenes. Es necesario incluir en linea de comando la imagen o directorio a procesar.")
grupo =  ap.add_mutually_exclusive_group(required=True)
grupo.add_argument("-i", "--imagen", help="path de la imagen a procesar")
grupo.add_argument("-d", "--directorio", help="path del directorio a procesar")

args = vars(ap.parse_args())

#Imports
from keras.preprocessing import image as image_utils
from imagenet_utils import decode_predictions
from imagenet_utils import preprocess_input
from vgg16 import VGG16
import numpy as np
import cv2
import fnmatch
import os
import time

# PREPROCESADOR
#-------------------------------------------------------------------------
lista_imagenes = []
if args['imagen'] == None : #Imanen nula --> directorio
    #Listo todos los tios de imagenes que OpenCV es capaz de cargar
    for file in os.listdir(args['directorio']):
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
        lista_imagenes[i] = args['directorio'] + '/' + lista_imagenes[i]
else: #Imagen no es nulo
    lista_imagenes.append(args['imagen'])
    
print("[BOU-INFO] Lista de imágenes a procesar:")
print (lista_imagenes)

# carga la red VGG16
print("[BOU-ESTADO] cargando red neuronal...")
model = VGG16(weights="imagenet")

#Empieza el procesado de la lista de imágenes
for imagen in lista_imagenes:
    hora_inicio = time.clock()
    print("[BOU-ESTADO] carga y preproceso de " + imagen)
    #Carga de la imagen solo para escribir luego lo que es
    orig = cv2.imread(imagen)
    #Ahora si, carga de la imagen de trabajo y la prepara para que
    #la pueda procesar la red neuronal (cambios de tamaño y formato)
    image = image_utils.load_img(imagen, target_size=(224, 224))
    image = image_utils.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
# VGG16
#-------------------------------------------------------------------------
    # clasificación de la imagen
    print("[BOU-ESTADO] clasificando imagen...")
    preds = model.predict(image)
# POSTPROCESADOR
#-------------------------------------------------------------------------
    #print("[BOU-INFO] la clasificación del modelo da: " + preds)
    (inID, label) = decode_predictions(preds)[0]
    duracion = time.clock() - hora_inicio
    # ahora pinta en la imagen original la etiqueta y la muestra
    print("[BOU-INFO] ImageNet ID: {}, Etiqueta: {}, Tiempo {}".format(inID, label, duracion))
    #cv2.putText(orig, "E
    tiqueta: {}".format(label), (10, 30),
    #cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    #cv2.imshow("Cladificacion", orig)
    #cv2.waitKey(0)
    
print ("[BOU-ESTADO] Fin ejecución")


