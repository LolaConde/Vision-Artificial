#!/usr/bin/env python

import cv2 as cv
import numpy as np
from umucv.stream import sourceArgs # Para obtener los argumentos
import argparse, sys # Para obtener los argumentos

NOMBRE_VENTANA = 'Selecciona 2 puntos'

def distancia(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def leerCoordenadas(nombre_archivo):
    # Formato:
    # x1 , y1 - x2 , y2
    # x3 , y3 - x4 , y4
    # ...
    #
    # Los puntos de la izquierda se devuelven en una lista y los de la derecha en otra lista (en el mismo orden)
    archivo = open(nombre_archivo, 'r')
    lineas = archivo.readlines()
    puntos1 = []
    puntos2 = []
    for linea in lineas:
        p1, p2 = linea.split("-")
        x1, y1 = p1.strip().split(",")
        x2, y2 = p2.strip().split(",")
        puntos1.append((float(x1), float(y1)))
        puntos2.append((float(x2), float(y2)))
    archivo.close()
    return puntos1, puntos2

# Calcular la transformación entre coordenadas homogéneas y tradicionales
def homog(x):
    ax = np.array(x)
    uc = np.ones(ax.shape[:-1]+(1,))
    return np.append(ax,uc,axis=-1)
def inhomog(x):
    ax = np.array(x)
    return ax[..., :-1] / ax[...,[-1]]

# Aplica una transformación homogénea h a un conjunto de puntos ordinarios, almacenados como filas
def htrans(h,x):
    return inhomog(homog(x) @ h.T)

# Obtenemos los argumentos de entrada
parser = argparse.ArgumentParser()
parser.add_argument('--imagen', help='Ruta de la imagen', type=str, default=None)
parser.add_argument('--coordenadas', help='Ruta del archivo con las coordenadas', type=str, default=None)
sourceArgs(parser)
args, rest = parser.parse_known_args(sys.argv)

assert len(rest)==1, 'Parámetros desconocidos: '+str(rest[1:])
if args.imagen is None or args.coordenadas is None:
    print("Falta alguno de los parámetros obligatorios")
    sys.exit(1)

img = cv.imread(args.imagen)
if img is None:
    print('Error: No se ha podido cargar la imagen.')
    exit()

puntos_imagen, puntos_reales = leerCoordenadas(args.coordenadas)

# Calculamos la homografía
H, _ = cv.findHomography(np.array(puntos_imagen), np.array(puntos_reales))

# Pedimos que seleccione 2 puntos
print('Selecciona 2 puntos en la imagen para saber la distancia real entre ellos.')
while True:
    # Selecciona 2 puntos
    puntos = []
    cv.imshow(NOMBRE_VENTANA, img)

    def click(event, x, y, flags, param):
        global puntos, img, NOMBRE_VENTANA
        if event == cv.EVENT_LBUTTONDOWN:
            if len(puntos) == 0:
                img = cv.imread(args.imagen)
            puntos.append((x, y))
            cv.circle(img=img, center=(x, y), radius=5, color=(255, 0, 255), thickness=-1)
            cv.imshow(NOMBRE_VENTANA, img)
            
    puntos = []
    cv.setMouseCallback(NOMBRE_VENTANA, click)
    while len(puntos) < 2:
        cv.waitKey(5)
    cv.setMouseCallback(NOMBRE_VENTANA, lambda *args : None)

    # Calcula los puntos en la imagen rectificada
    puntos_real = htrans(H, puntos)

    # Dibuja la distancia entre los puntos
    inicio_linea = np.array([int(i) for i in puntos[0]])
    final_linea = np.array([int(i) for i in puntos[1]])
    medio_linea = (int((inicio_linea[0] + final_linea[0]) / 2), int((inicio_linea[1] + final_linea[1]) / 2))
    distancia_puntos = str(round(distancia(puntos_real[0], puntos_real[1]), 2))
    cv.putText(img=img, text=distancia_puntos, org=medio_linea, fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
    cv.line(img=img, pt1=inicio_linea, pt2=final_linea, color=(255, 0, 255), thickness=2)