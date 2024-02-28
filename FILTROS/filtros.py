#!/usr/bin/env python

import cv2 as cv # OpenCV
from umucv.stream import autoStream # Mostrar la cámara
from umucv.util import putText, ROI # Región de interés y añadir texto a la imagen mostrada
from scipy.ndimage import minimum_filter, maximum_filter # Filtros de mínimo y máximo
from umucv.util import Help # Para mostrar la ayuda
import numpy as np

# Crea la ventana por primera vez
nombreVentana = "filtros.py" 
cv.namedWindow(nombreVentana)
cv.moveWindow(nombreVentana, 0, 0)
# Crea la región de interés
region = ROI(nombreVentana)

color = True # ¿Imagen a color?
showHelp = True # ¿Mostrar la ayuda?
onlyRoi = False # ¿Mostrar solo la región de interés?

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

class Filtro:
    def __init__(self, nombre, id): # Constructor
        self.nombre = nombre
        self.id = id
    def applyFilter(self, frame): # Aplica el filtro a un frame
        return frame
    def crearTrackbar(self, nombreVentana): # Crea los trackbars necesarios para el filtro
        return

class NoFiltro(Filtro):
    def __init__(self):
        super().__init__("Sin filtro", "0")

class Gaussian(Filtro):
    def __init__(self):
        self.desvEst = 3
        super().__init__("Gaussian", "2")
    
    def applyFilter(self, frame):
        auto = (0,0)
        return cv.GaussianBlur(frame, auto, self.desvEst)
    
    def crearTrackbar(self, nombreVentana):
        def guardarValorTrackbar(valor):
            if valor == 0: valor = 1
            self.desvEst = valor
        cv.createTrackbar("DesvEst",  nombreVentana, self.desvEst, 30, guardarValorTrackbar)

class Box(Filtro):
    def __init__(self):
        self.tamKernel = 11
        super().__init__("Box", "1")
    
    def applyFilter(self, frame):
        return cv.boxFilter(frame, -1, (self.tamKernel,self.tamKernel))
    
    def crearTrackbar(self, nombreVentana):
        def guardarValorTrackbar(valor):
            if valor == 0: valor = 1
            self.tamKernel = valor
        cv.createTrackbar("Tam kernel",  nombreVentana, self.tamKernel, 30, guardarValorTrackbar)

class Median(Filtro):
    def __init__(self):
        self.tamKernel = 17
        super().__init__("Median", "3")
    
    def applyFilter(self, frame):
        return cv.medianBlur(frame, self.tamKernel)
    
    def crearTrackbar(self, nombreVentana):
        def guardarValorTrackbar(valor):
            if valor % 2 == 0: valor += 1
            self.tamKernel = valor
        cv.createTrackbar("Tam kernel",  nombreVentana, self.tamKernel, 30, guardarValorTrackbar)

class Bilateral(Filtro):
    def __init__(self):
        self.sigmaColor = 15
        self.sigmaSpace = 15
        super().__init__("Bilateral", "4")
    
    def applyFilter(self, frame):
        return cv.bilateralFilter(frame, 0, self.sigmaColor, self.sigmaSpace)
    
    def crearTrackbar(self, nombreVentana):
        def guardarValorTrackbar(valor):
            self.sigmaColor = valor
        def guardarValorTrackbar2(valor):
            self.sigmaSpace = valor
        cv.createTrackbar("Sigma color", nombreVentana, self.sigmaColor, 50, guardarValorTrackbar)
        cv.createTrackbar("Sigma space", nombreVentana, self.sigmaSpace, 50, guardarValorTrackbar2)

class Min(Filtro):
    def __init__(self):
        self.tamKernel = 11
        super().__init__("Min", "5")
    
    def applyFilter(self, frame):
        return minimum_filter(frame, self.tamKernel)
    
    def crearTrackbar(self, nombreVentana):
        def guardarValorTrackbar(valor):
            if valor == 0: valor = 1
            self.tamKernel = valor
        cv.createTrackbar("Tam kernel",  nombreVentana, self.tamKernel, 30, guardarValorTrackbar)

class Max(Filtro):
    def __init__(self):
        self.tamKernel = 11
        super().__init__("Max", "6")
    
    def applyFilter(self, frame):
        return maximum_filter(frame, self.tamKernel)
    
    def crearTrackbar(self, nombreVentana):
        def guardarValorTrackbar(valor):
            if valor == 0: valor = 1
            self.tamKernel = valor
        cv.createTrackbar("Tam kernel",  nombreVentana, self.tamKernel, 30, guardarValorTrackbar)

class TransformacionDeValor(Filtro):
    def __init__(self):
        self.valor = 50
        super().__init__("Transformación de valor", "7")
    
    def applyFilter(self, frame):
        # Transforma el valor de luminancia de cada píxel independientemente de su entorno, sumándole "valor".
        yuv = cv.cvtColor(frame, cv.COLOR_BGR2YUV)
        yuv[:,:,0] = yuv[:,:,0] + self.valor
        return cv.cvtColor(yuv, cv.COLOR_YUV2BGR)
    
    def crearTrackbar(self, nombreVentana):
        def guardarValorTrackbar(valor):
            self.valor = valor
        cv.createTrackbar("Valor",  nombreVentana, self.valor, 100, guardarValorTrackbar)

class EcualizadorDeHistograma(Filtro):
    def __init__(self):
        super().__init__("Ecualizador de histograma", "8")
    
    def applyFilter(self, frame):
        # Normalización de contraste mediante ecualizador de histograma.
        # Se normaliza el contraste de la componente de luminancia (Y).
        yuv = cv.cvtColor(frame, cv.COLOR_BGR2YUV)
        yuv[:,:,0] = cv.equalizeHist(yuv[:,:,0])
        return cv.cvtColor(yuv, cv.COLOR_YUV2BGR)

class CLAHE(Filtro):
    def __init__(self):
        super().__init__("CLAHE", "9")
    
    def applyFilter(self, frame):
        # Normaliza el contraste de una imagen. Se aplica CLAHE a la componente de luminancia.
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        yuv = cv.cvtColor(frame, cv.COLOR_BGR2YUV)
        yuv[:,:,0] = clahe.apply(yuv[:,:,0])
        return cv.cvtColor(yuv, cv.COLOR_YUV2BGR)

class Opening(Filtro):
    def __init__(self):
        super().__init__("Opening", "a")
    
    def applyFilter(self, frame):
        # Este filtro realiza una erosión seguida de una dilatación. Se usa para eliminar ruido. 
        # Se aplica a la componente de luminancia.
        yuv = cv.cvtColor(frame, cv.COLOR_BGR2YUV)
        yuv[:,:,0] = cv.morphologyEx(yuv[:,:,0], cv.MORPH_OPEN, np.ones((5,5),np.uint8))
        return cv.cvtColor(yuv, cv.COLOR_YUV2BGR)

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