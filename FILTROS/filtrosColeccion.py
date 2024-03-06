import cv2 as cv
from scipy.ndimage import minimum_filter, maximum_filter
from filtroConstructor import Filtro
import numpy as np

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