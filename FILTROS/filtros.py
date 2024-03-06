#!/usr/bin/env python

import cv2 as cv # OpenCV
from umucv.stream import autoStream # Mostrar la cámara
from umucv.util import putText, ROI # Región de interés y añadir texto a la imagen mostrada
from scipy.ndimage import minimum_filter, maximum_filter # Filtros de mínimo y máximo
from umucv.util import Help # Para mostrar la ayuda
from filtroConstructor import Filtro # Clase de la que heredan todos los filtros, no se usa directamente
from filtrosColeccion import * # Importa todos los filtros (subclases de Filtro)

# Crea la ventana por primera vez
nombreVentana = "filtros.py" 
cv.namedWindow(nombreVentana)
cv.moveWindow(nombreVentana, 0, 0)
# Crea la región de interés
region = ROI(nombreVentana)

color = True # ¿Imagen a color?
showHelp = True # ¿Mostrar la ayuda?
onlyRoi = False # ¿Mostrar solo la región de interés?

def setFiltro(idFiltro): # Si no existe, sigue con el filtro que estaba
    global filtroActual
    global filtros
    if filtroActual.id == idFiltro: return
    for filtro in filtros:
        if filtro.id == idFiltro:
            volver_a_crear_Ventana()
            filtroActual = filtro
            filtroActual.crearTrackbar(nombreVentana)
            return

# Inicializa el filtro actual
filtroActual = NoFiltro()
# Crea una lista con todos los filtros
subclasesDeFiltro = Filtro.__subclasses__()
filtros = []
for subclase in subclasesDeFiltro:
    filtros.append(subclase())

def frameToGray(frame):
    # Primero se pasa a gris
    gris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Después hace que vuelva a tener 3 canales (BGR)
    return cv.cvtColor(gris, cv.COLOR_GRAY2BGR)

def volver_a_crear_Ventana():
    cv.destroyWindow(nombreVentana)
    cv.namedWindow(nombreVentana)
    global region
    region = ROI(nombreVentana)
    region.roi = [x1, y1, x2, y2]

# Ayuda
ayudaString = """""" # String con todos los filtros y sus teclas
for filtro in filtros:
    ayudaString += filtro.id + ": " + filtro.nombre + "\n"
help = Help(
"""
BLUR FILTERS

""" + ayudaString + """

c: color/monochrome
r: only roi

h: show/hide help
""")
Help.show(help) # Inicia enseñando la ayuda

# Recorrer todos los fotogramas del flujo de entrada
for key, frame in autoStream():
    trozo = None

    imagecam = cv.flip(frame, 1) # Con modo espejo
    
    # Si ha pulsado una tecla para indicar un filtro, se guarda cual ha sido
    setFiltro(chr(key))
    if key == ord('c'):
        color = not color
    if key == ord('r'):
        onlyRoi = not onlyRoi
    help.show_if(key, ord('h'))
    
    if region.roi:
        # Guarda la región de interés
        [x1, y1, x2, y2] = region.roi
        trozo = frame[y1:y2+1, x1:x2+1]
        
        # Si no está en color, lo pasa a gris
        if not color: trozo = frameToGray(trozo)

        # Se aplica el filtro correspondiente y se muestra el nombre del filtro
        trozo = filtroActual.applyFilter(trozo)
        putText(trozo, filtroActual.nombre, (15, 20))
        frame[y1:y2+1, x1:x2+1] = trozo
        
        # Se muestra un rectángulo rodeando la región de interés
        cv.rectangle(frame, (x1,y1), (x2,y2), color=(10,10,10), thickness=2)
        
    if (onlyRoi):
        if (trozo is not None): cv.imshow(nombreVentana, trozo)
        else: onlyRoi = False
    if(not onlyRoi):
        cv.imshow(nombreVentana, frame)