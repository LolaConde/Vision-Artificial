#!/usr/bin/env python

import cv2 as cv # OpenCV
from umucv.stream import autoStream # Mostrar la cámara
from umucv.util import putText, ROI # Región de interés y añadir texto a la imagen mostrada
from scipy.ndimage import minimum_filter, maximum_filter # Filtros de mínimo y máximo
from umucv.util import Help # Para mostrar la ayuda
import numpy as np

cv.namedWindow("filtros.py") # Crea una ventana llamada "filtros.py"
cv.moveWindow("filtros.py", 0, 0) # Mueve la ventana a la posición (0, 0), es decir, a la esquina superior izquierda
region = ROI("filtros.py") # Crea una región de interés en la ventana "filtros.py"
filtroActual = "0" # Filtro actual (0, 1, ...)
color = True # Si es true, la imagen es en color, si es false, en blanco y negro
showHelp = True # Si es true, muestra la ayuda, si es false, la oculta
onlyRoi = False # Si es true, solo muestra el roi, si es false, lo muestra todo

# Ayuda
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
7: Transformación de valor
8: Ecualizador de histograma
9: CLAHE
a: Opening

c: color/monochrome
r: only roi

h: show/hide help
""")
Help.show(help) # Inicia enseñando la ayuda

def frameToGray(frame):
    # Primero se pasa a gris
    gris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Después hace que vuelva a tener 3 canales (BGR)
    return cv.cvtColor(gris, cv.COLOR_GRAY2BGR)

def frameToBox(frame, valor):
    # Le aplica el filtro box, que suaviza la imagen.
    # El primer parámetro es la imagen, el segundo es el tipo de salida (si es -1, la salida es la misma que la entrada), y cuanto más grande sea el tercero (el tamaño del kernel), más suavizada estará la imagen
    return cv.boxFilter(frame, -1, (valor,valor))

def frameToGaussian(frame, desvEst):
    auto = (0,0) # tamaño de la máscara automático, dependiendo de desvEst (la desviación estándar de la distribución gaussiana)
    # A cuanto mayor valor de desviación, más suavizada estará la imagen. 
    return cv.GaussianBlur(frame, auto, desvEst)

def frameToMedian(frame, valor):
    # El valor es el tamaño del kernel
    # A más valor, más suavizada está la imagen. Si subo de 17, da error
    return cv.medianBlur(frame, valor)

def frameToBilateral(frame, sigmaColor, sigmaSpace):
    # Promedia los píxeles cercanos que además tienen un valor similar
    # Cuanto más grande es el sigmaColor, píxeles con valores más alejados se promedian
    # Cuanto más grande es el sigmaSpace, píxeles más alejados se promedian
    return cv.bilateralFilter(frame, 0, sigmaColor, sigmaSpace)

def frameToMin(frame, valor):
    # Filtro de mínimo. El valor modifica la cantidad de vecinos que se tienen en cuenta
    return minimum_filter(frame, valor)

def frameToMax(frame, valor):
    # Filtro de máximo. El valor modifica la cantidad de vecinos que se tienen en cuenta
    return maximum_filter(frame, valor)

def transformacionDeValor(frame, valor):
    # Transforma el valor de luminancia de cada píxel independientemente de su entorno, sumándole "valor".
    yuv = cv.cvtColor(frame, cv.COLOR_BGR2YUV)
    yuv[:,:,0] = yuv[:,:,0] + valor
    # Se pasa de YUV a BGR para que la imagen vuelva a tener el mismo formato que al principio
    return cv.cvtColor(yuv, cv.COLOR_YUV2BGR)

def normalizacionDeContraste(frame):
    # Normalización de contraste mediante ecualizador de histograma.
    # Se normaliza el contraste de la componente de luminancia (Y).
    yuv = cv.cvtColor(frame, cv.COLOR_BGR2YUV)
    yuv[:,:,0] = cv.equalizeHist(yuv[:,:,0])
    return cv.cvtColor(yuv, cv.COLOR_YUV2BGR)

def clahe(frame):
    # CLAHE. Normaliza el contraste de una imagen. Se aplica CLAHE a la componente de luminancia.
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    yuv = cv.cvtColor(frame, cv.COLOR_BGR2YUV)
    yuv[:,:,0] = clahe.apply(yuv[:,:,0])
    return cv.cvtColor(yuv, cv.COLOR_YUV2BGR)

def opening(frame):
    # Este filtro realiza una erosión seguida de una dilatación. Se usa para eliminar ruido. 
    # Se aplica a la componente de luminancia.
    yuv = cv.cvtColor(frame, cv.COLOR_BGR2YUV)
    yuv[:,:,0] = cv.morphologyEx(yuv[:,:,0], cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    return cv.cvtColor(yuv, cv.COLOR_YUV2BGR)

trozo = None # Trozo de imagen
# Recorrer todos los fotogramas del flujo de entrada
for key, frame in autoStream():
    trozo = None # Empieza con la region roi vacía
    H,W,_ = frame.shape # Alto y ancho de la imagen
    
    # Es mejor trabajar con imagen espejo
    imagecam = cv.flip(frame, 1) # Con modo espejo
    
    if region.roi:
        [x1, y1, x2, y2] = region.roi # Coordenadas de la región de interés
        trozo = frame[y1:y2+1, x1:x2+1]
        
        # Si ha pulsado una tecla para indicar un filtro, se guarda cual ha sido
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
        if key == ord('7'):
            filtroActual = "7" # Transformación de valor
        if key == ord('8'):
            filtroActual = "8" # Equalizador de histograma
        if key == ord('9'):
            filtroActual = "9" # CLAHE
        if key == ord('a'):
            filtroActual = "a" # opening
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
            trozo = frameToMin(trozo, 11)
        elif filtroActual == "6":
            trozo = frameToMax(trozo, 11)
        elif filtroActual == "7":
            trozo = transformacionDeValor(trozo, 100)
        elif filtroActual == "8":
            trozo = normalizacionDeContraste(trozo)
        elif filtroActual == "9":
            trozo = clahe(trozo)
        elif filtroActual == "a":
            trozo = opening(trozo)
        elif filtroActual == "0":
            pass
        frame[y1:y2+1, x1:x2+1] = trozo
        # Se muestra un rectángulo rodeando la región de interés
        cv.rectangle(frame, (x1,y1), (x2,y2), color=(10,10,10), thickness=2)
        
    # Muestra el fotograma, y si se ha pulsado la recla r y había seleccionada una región de interés, muestra solo esa región. Si se había pulsado pero no había región de interés, muestra todo (deberá marcar ROI de nuevo y después pulsar r)
    if (onlyRoi):
        if (trozo is not None):
            cv.imshow("filtros.py", trozo)
        else:
            onlyRoi = False
    if(not onlyRoi):
        cv.imshow("filtros.py", frame)