#!/usr/bin/env python

import cv2 as cv
import numpy as np

# Calcular distancia entre 2 puntos
def distancia(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

NOMBRE_VENTANA = 'Selecciona 4 puntos en la imagen'

# Obtenemos la imagen
nombre = input("Introduce el nombre de la imagen (y su ruta): ")
img = cv.imread(nombre)
if img is None:
    print('Error: No se ha podido cargar la imagen.')
    exit()

# Obtenemos el nombre del archivo con las coordenadas reales de los puntos
nombre_archivo_puntos = input("Introduce el nombre del archivo (y su ruta) con las coordenadas reales de los puntos: ")

# Decimos que seleccione 4 puntos por terminal
print('Selecciona los 4 puntos en la imagen en el mismo orden que en el archivo de coordenadas.')

# Si se hace click en la imagen, se guarda el punto
def click(event, x, y, flags, param):
    global puntos, img, NOMBRE_VENTANA
    if event == cv.EVENT_LBUTTONDOWN:
        puntos.append((x, y))
        cv.circle(img, (x, y), 5, (255, 0, 255), -1)
        cv.putText(img, str(len(puntos)), (x+10, y+10), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv.imshow(NOMBRE_VENTANA, img)

# Selecciona 4 puntos
puntos = []
cv.imshow(NOMBRE_VENTANA, img)
cv.setMouseCallback(NOMBRE_VENTANA, click)
while len(puntos) < 4:
    cv.waitKey(5)
cv.setMouseCallback(NOMBRE_VENTANA, lambda *args : None)

# Rectificamos la imagen
# 1. Leemos los puntos del archivo
archivo_puntos = open(nombre_archivo_puntos, 'r')
lineas = archivo_puntos.readlines()
puntos_reales = []
for linea in lineas:
    x, y = linea.strip().split(",")
    puntos_reales.append((float(x), float(y)))
# 2. Si los puntos tienen distancias muy largas entre ellos, los escalamos
distancias = []
for i in range(4):
    distancias.append(distancia(puntos[i], puntos[(i+1)%4]))
distancia_media = sum(distancias) / 4
distancias_reales = []
for i in range(4):
    distancias_reales.append(distancia(puntos_reales[i], puntos_reales[(i+1)%4]))
distancia_media_real = sum(distancias_reales) / 4
escala = (distancia_media_real / distancia_media)
for i in range(4):
    puntos_reales[i] = (float(puntos_reales[i][0] / escala), float(puntos_reales[i][1] / escala))
# 3. Calculamos la homografía
H,_ = cv.findHomography(np.array(puntos), np.array(puntos_reales))
# 4. Rectificamos la imagen
img_rect = cv.warpPerspective(cv.imread(nombre) , H, (img.shape[1], img.shape[0]))

# Mostramos la imagen rectificada y decimos que seleccione 2 puntos para medir la distancia real entre ellos
# 1. Mostramos la imagen rectificada
cv.imshow(NOMBRE_VENTANA, img_rect)
print("Pulsa 2 puntos para saber la distancia entre ellos.")
# 2. Si se hace click en la imagen, se guarda el punto
puntos_seleccionados = []
def click2(event, x, y, flags, param):
    global puntos_seleccionados, img_rect, NOMBRE_VENTANA
    if event == cv.EVENT_LBUTTONDOWN:
        puntos_seleccionados.append((x, y))
        cv.circle(img_rect, (x, y), 5, (255, 0, 255), -1)
        cv.imshow(NOMBRE_VENTANA, img_rect)
# 3. Selecciona 2 puntos
cv.setMouseCallback(NOMBRE_VENTANA, click2)
while len(puntos_seleccionados) < 2:
    cv.waitKey(5)
cv.setMouseCallback(NOMBRE_VENTANA, lambda *args : None)
# 4. Calcula la distancia entre los 2 puntos
distancia_puntos = distancia(puntos_seleccionados[0], puntos_seleccionados[1]) * escala
# 5. Dibuja la distancia en el medio de la linea que une los 2 puntos y muestra la distancia y la linea
medio_linea = (int((puntos_seleccionados[0][0] + puntos_seleccionados[1][0]) / 2), int((puntos_seleccionados[0][1] + puntos_seleccionados[1][1]) / 2))
print("La distancia real entre los 2 puntos seleccionados es de", distancia_puntos, ".")
# 6. Mostramos la imagen con la distancia real entre los 2 puntos seleccionados acotado a 2 decimales
cv.putText(img_rect, str(round(distancia_puntos, 2)), medio_linea, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv.line(img_rect, puntos_seleccionados[0], puntos_seleccionados[1], (255, 0, 255), 2)

# Mostramos la imagen con la distancia real entre los 2 puntos seleccionados
while True:
    cv.waitKey(5)
    cv.imshow(NOMBRE_VENTANA, img_rect)