# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 11:14:22 2016

@author: dpbou
"""

import argparse
import utilidades_archivos


# Genera subimagenes de una imagen o todas las de un directorio
if __name__ == "__main__":
    p = argparse.ArgumentParser("Genera subimágenes a partir de una imagen concreta o todas las imagenes de un directoro")
    grupo =  p.add_mutually_exclusive_group(required=True)
    grupo.add_argument("-i", "--imagen", 
                       action="store", help="path de la imagen a procesar")
    grupo.add_argument("-d", "--directorio", 
                       action="store", help="path del directorio a procesar") 
    p.add_argument("dimx",  type=int, 
                   action="store", help="X, anchura de las imagenes deseadas")
    p.add_argument("dimy", type=int, 
                   action="store", help="Y, altura de las imagenes deseadas")
    p.add_argument("-p" , "--prefijo", required=False,
                   action="store", help="Prefijo que se concatenará por delan te del nombre a las imagenes generadas, puede ser una carpeta")              
                   
    
    opts = p.parse_args()
    if opts.imagen == None : #Imagen nula --> directorio
        print ("hols!!")
        if opts.prefijo != None:
            lista_errores = utilidades_archivos.genera_subimagenes_directorio(opts.directorio, opts.dimx, opts.dimy, opts.prefijo)
        else: 
            lista_errores = utilidades_archivos.genera_subimagenes_directorio(opts.directorio, opts.dimx, opts.dimy)
    else:
        if opts.prefijo != None:
            lista_errores = utilidades_archivos.genera_subimagenes_archivo(opts.imagen, opts.dimx, opts.dimy, opts.prefijo)
        else:
            lista_errores = utilidades_archivos.genera_subimagenes_archivo(opts.imagen, opts.dimx, opts.dimy)
    print lista_errores
        
    
  