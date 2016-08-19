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
grupo2 = ap.add_mutually_exclusive_group(required=False)
grupo2.add_argument("-top", "--include_top", dest="include_top", action="store_true",
                    help="Incluir las capas del clasificador")
grupo2.add_argument("-no_top", "--no_include_top", dest="include_top", action="store_false",
                    help="NO incluir las capas del clasificador")
args = vars(ap.parse_args())
opts = ap.parse_args()

#Imports
from keras.preprocessing import image as image_utils
from imagenet_utils import decode_predictions
from imagenet_utils import preprocess_input
from vgg16 import VGG16
import numpy as np
import cv2
import time
import utilidades_archivos

# PREPROCESADOR
#-------------------------------------------------------------------------
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

# carga la red VGG16
print("[BOU-ESTADO] cargando red neuronal con include_top={}...".format(opts.include_top))
print(args['include_top'])
model = VGG16(include_top=opts.include_top, weights="imagenet")
#model = VGG16(include_top=True, weights="imagenet")

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
    duracion = time.clock() - hora_inicio
    print("[BOU-INFO] tiempo de calculo {}".format(duracion)) 
    print("[BOU-INFO] datos averiguados de la variable preds:") 
    print(type(preds))
    print(preds.shape)
# POSTPROCESADOR
#-------------------------------------------------------------------------
    #print("[BOU-INFO] la clasificación del modelo da: " + preds)
    #(inID, label) = decode_predictions(preds)[0]
    #duracion = time.clock() - hora_inicio
    # ahora pinta en la imagen original la etiqueta y la muestra
    #print("[BOU-INFO] ImageNet ID: {}, Etiqueta: {}, Tiempo {}".format(inID, label, duracion))
    #cv2.putText(orig, "Etiqueta: {}".format(label), (10, 30),
    #cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    #cv2.imshow("Cladificacion", orig)
    #cv2.waitKey(0)
    
print ("[BOU-ESTADO] Fin ejecución")


