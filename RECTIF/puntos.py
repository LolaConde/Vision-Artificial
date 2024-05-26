#!/usr/bin/env python

import cv2 as cv
import numpy as np
from umucv.stream import sourceArgs # Para obtener los argumentos
import argparse, sys # Para obtener los argumentos

NOMBRE_VENTANA = 'Selecciona 4 puntos'

# Obtenemos la imagen
parser = argparse.ArgumentParser()
parser.add_argument('--imagen', help='Ruta de la imagen', type=str, default=None)
sourceArgs(parser)
args, rest = parser.parse_known_args(sys.argv)

assert len(rest)==1, 'Parámetros desconocidos: '+str(rest[1:])
if args.imagen is None:
    print("Falta la imagen")
    sys.exit(1)

img = cv.imread(args.imagen)
if img is None:
    print('Error: No se ha podido cargar la imagen.')
    exit()

# Pedimos que seleccione 4 puntos
print('Selecciona 4 puntos en la imagen para saber sus coordenadas.')

# Selecciona 4 puntos
puntos = []
cv.imshow(NOMBRE_VENTANA, img)

def click(event, x, y, flags, param):
    global puntos, img, NOMBRE_VENTANA
    if event == cv.EVENT_LBUTTONDOWN:
        puntos.append((x, y))
        cv.circle(img=img, center=(x, y), radius=5, color=(255, 0, 255), thickness=-1)
        cv.imshow(NOMBRE_VENTANA, img)
        
cv.setMouseCallback(NOMBRE_VENTANA, click)
while len(puntos) < 4:
    cv.waitKey(5)
cv.setMouseCallback(NOMBRE_VENTANA, lambda *args : None)

# Mostramos los puntos
print('Los puntos seleccionados son:')
for i, p in enumerate(puntos):
    print(f'P{i+1}: {p}')

exit()