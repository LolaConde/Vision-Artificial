#!/usr/bin/env python

import cv2 as cv
from umucv.stream import autoStream
from collections import deque
import numpy as np
from umucv.util import putText


points = deque(maxlen=2)
DISTANCIA_FOCAL = 738
ANCHO_CAMARA = 640
ALTO_CAMARA = 360

def fun(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        points.append((x,y))

# Devuelve el vector que forma el rayo óptico que pasa por el punto p1 (desde el centro hasta el punto)
def pointToVector(punto):
    return np.array([punto[0] - ANCHO_CAMARA/2, punto[1] - ALTO_CAMARA/2, DISTANCIA_FOCAL])

# Devuelve el ángulo en grados entre los rayos ópticos que pasan por los puntos p1 y p2
def pointsDegrees(p1,p2):
    v1 = pointToVector(p1)
    v2 = pointToVector(p2)
    # u * v
    dividendo = np.dot(v1,v2)
    # |u| * |v|
    divisor = np.linalg.norm(v1) * np.linalg.norm(v2)
    # angulo en radianes
    angulo = np.arccos(dividendo/divisor)
    # angulo en grados
    return np.degrees(angulo)
    

cv.namedWindow("webcam")
cv.setMouseCallback("webcam", fun)

for key, frame in autoStream():
    for p in points:
        cv.circle(frame, p,3,(0,0,255),-1)
    if len(points) == 2:
        cv.line(frame, points[0],points[1],(0,0,255))
        c = np.mean(points, axis=0).astype(int)
        d = np.linalg.norm(np.array(points[1])-points[0])
        degrees = pointsDegrees(points[0], points[1]) # Ángulo en grados
        putText(frame,f'{d:.1f} pix, {degrees:.1f} grados',c) # Mostrar distancia y el ángulo entre los puntos

    cv.imshow('webcam',frame)
    
cv.destroyAllWindows()

