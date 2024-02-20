#!/usr/bin/env python

import cv2 as cv
import numpy as np
from umucv.stream import autoStream
from umucv.util import putText, ROI
import math # Calcula el arcotangente
import subprocess # Abre y cierra la terminal
import os
from scipy.ndimage import minimum_filter, maximum_filter
import matplotlib.pyplot as plt # Para poner las imágenes en gray

cv.namedWindow("filtros.py") # Crea una ventana llamada "filtros.py"
cv.moveWindow("filtros.py", 0, 0) # Mueve la ventana a la posición (0, 0), es decir, a la esquina superior izquierda
region = ROI("filtros.py") # Crea una región de interés en la ventana "filtros.py"
filtroActual = "0" # Filtro actual (a, b, ...)
color = True # Si es true, la imagen es en color, si es false, en blanco y negro
showHelp = True # Si es true, muestra la ayuda, si es false, la oculta
onlyRoi = False # Si es true, solo muestra el roi, si es false, lo muestra todo

# Ayuda
from umucv.util import Help
help = Help(
"""
BLUR FILTERS

0: do nothing
1: box
2: Gaussian
3: median
4: bilateral
5: min
6: max

c: color/monochrome
r: only roi

h: show/hide help
""")
Help.show(help) # Inicia enseñando la ayuda

def frameToGray(frame):
    # Primero se pasa a gris
    gris = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    # Después hace que vuelva a tener 3 canales (RGB)
    return cv.cvtColor(gris, cv.COLOR_GRAY2RGB)

def frameToBox(frame, valor):
    # Le aplica el filtro box, que suaviza la imagen.
    # El primer parámetro es la imagen, el segundo es el tipo de salida (si es -1, la salida es la misma que la entrada), y cuanto más grande sea el tercero, más suavizada estará la imagen
    return cv.boxFilter(frame, -1, (valor,valor))

def frameToGaussian(frame, sigma):
    auto = (0,0) # tamaño de la máscara automático, dependiendo de sigma
    # A cuanto más valor, más suavizada estará la imagen. 
    # En contraste con frameToBox, frameToBox añadía más ruido a la imagen que frameToGaussian.
    return cv.GaussianBlur(frame, auto, sigma)

def frameToMedian(frame, valor):
    # A más valor, más suavizada está la imagen, y si subo de 17, da error
    return cv.medianBlur(frame, valor)

def frameToBilateral(frame, sigmaColor, sigmaSpace):
    # Promedia los píxeles cercanos que además tienen un valor similar
    # Cuanto más grande es el sigmaColor, píxeles con valores más alejados se promedian
    # Cuanto más grande es el sigmaSpace, píxeles más alejados se promedian
    return cv.bilateralFilter(frame, 0, sigmaColor, sigmaSpace)

def frameToMin(frame):
    # Filtro de mínimo
    return minimum_filter(frame,11)

def frameToMax(frame):
    # Filtro de máximo
    return maximum_filter(frame,11)

def frameToGray2(frame):
    plt.imshow(frame, 'gray')

trozo = None # Trozo de imagen
# Recorrer todos los fotogramas del flujo de entrada
for key, frame in autoStream():
    trozo = None # Empieza con la region roi vacía
    H,W,_ = frame.shape # Alto y ancho de la imagen
    
    # Es mejor trabajar con imagen espejo
    imagecam = cv.flip(frame, 1) # Con modo espejo
    
    if region.roi:
        [x1, y1, x2, y2] = region.roi
        trozo = frame[y1:y2+1, x1:x2+1]
        
        # Si ha pulsado una tecla, se guarda cual ha sido
        if key == ord('0'):
            filtroActual = "0" # No hace nada
        if key == ord('1'):
            filtroActual = "1" # box
        if key == ord('2'):
            filtroActual = "2" # Gaussian
        if key == ord('3'):
            filtroActual = "3" # Median
        if key == ord('4'):
            filtroActual = "4" # Bilateral
        if key == ord('5'):
            filtroActual = "5" # Min
        if key == ord('6'):
            filtroActual = "6" # Max
        if key == ord('c'):
            color = not color # Color/monochrome
        if key == ord('r'):
            onlyRoi = not onlyRoi # Muestra solo roi / muestra todo
        
        help.show_if(key, ord('h')) # Muestra/oculta la ayuda
        
        # Si no está en color, lo pasa a gris
        if not color:
            trozo = frameToGray(trozo)
        
        # Se aplica el filtro correspondiente (0 no hace nada)
        if filtroActual == "1":
            trozo = frameToBox(trozo, 11)
        elif filtroActual == "2":
            trozo = frameToGaussian(trozo, 3)
        elif filtroActual == "3":
            trozo = frameToMedian(trozo, 17)
        elif filtroActual == "4":
            trozo = frameToBilateral(trozo, 20, 20)
        elif filtroActual == "5":
            trozo = frameToMin(trozo)
        elif filtroActual == "6":
            trozo = frameToMax(trozo)
        elif filtroActual == "0":
            pass
        frame[y1:y2+1, x1:x2+1] = trozo
        # Se muestra un rectángulo rodeando la región de interés
        #cv.rectangle(frame, (x1,y1), (x2,y2), color=(0,255,255), thickness=2)
        
    # Muestra el fotograma, y si se ha pulsado la recla r y había seleccionada una región de interés, muestra solo esa región. Si se había pulsado pero no había región de interés, muestra todo (deberá marcar ROI de nuevo y después pulsar r)
    if (onlyRoi):
        if (trozo is not None):
            cv.imshow("filtros.py", trozo)
        else:
            onlyRoi = False
    if(not onlyRoi):
        cv.imshow("filtros.py", frame)
frame