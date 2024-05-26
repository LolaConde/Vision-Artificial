#!/usr/bin/env python

import cv2 as cv
import numpy as np

NOMBRE_VENTANA = 'Selecciona 2 puntos'

# Calcular distancia entre 2 puntos
def distancia(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Leer las coordenadas de un archivo
def leerCoordenadas(nombre_archivo):
    archivo = open(nombre_archivo, 'r')
    lineas = archivo.readlines()
    puntos = []
    for linea in lineas:
        x, y = linea.strip().split(",")
        puntos.append((float(x), float(y)))
    archivo.close()
    return puntos

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

# Obtenemos la imagen
nombre = input("Introduce el nombre de la imagen (y su ruta): ")
img = cv.imread(nombre)
if img is None:
    print('Error: No se ha podido cargar la imagen.')
    exit()

# Obtenemos las coordenadas reales
nombre_archivo = input("Introduce el nombre del archivo (y su ruta) con las coordenadas reales de los puntos: ")
puntos_reales = leerCoordenadas(nombre_archivo)

# Obtenemos las coordenadas en la imagen
nombre_archivo = input("Introduce el nombre del archivo (y su ruta) con las coordenadas en la imagen: ")
puntos_imagen = leerCoordenadas(nombre_archivo)

# Obtenemos la homografía
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
                img = cv.imread(nombre)
            puntos.append((x, y))
            cv.circle(img, (x, y), 5, (255, 0, 255), -1)
            cv.imshow(NOMBRE_VENTANA, img)
            
    puntos = []
    cv.setMouseCallback(NOMBRE_VENTANA, click)
    while len(puntos) < 2:
        cv.waitKey(5)
    cv.setMouseCallback(NOMBRE_VENTANA, lambda *args : None)

    # Calcula los puntos en la imagen rectificada
    puntos_real = htrans(H, puntos)

    # Calcula la distancia entre los puntos
    distancia_puntos = distancia(puntos_real[0], puntos_real[1])
    medio_linea = (int((puntos[0][0] + puntos[1][0]) / 2), int((puntos[0][1] + puntos[1][1]) / 2))
    cv.putText(img, str(round(distancia_puntos, 2)), medio_linea, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv.line(img, np.array([int(i) for i in puntos[0]]), np.array([int(i) for i in puntos[1]]), (255, 0, 255), 2)