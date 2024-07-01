#!/usr/bin/env python

from umucv.stream   import autoStream
import cv2 as cv
import numpy as np
from umucv.contours import extractContours, redu
from umucv.htrans import homog, inhomog, htrans, rmsreproj, jc, desp

# Objeto 3D a dibujar (una casa salvo que se especifique otro objeto)
objeto = np.array([[-0.5, -0.5, 0.0],
                 [ 0.5, -0.5, 0.0],
                 [ 0.5,  0.5, 0.0],
                 [-0.5,  0.5, 0.0],
                 [-0.5, -0.5, 0.0],
                 [-0.5, -0.5, 1.0],
                 [ 0.5, -0.5, 1.0],
                 [ 0.5,  0.5, 1.0],
                 [-0.5,  0.5, 1.0],
                 [-0.5, -0.5, 1.0],
                 [ 0.5, -0.5, 1.0],
                 [ 0.5, -0.5, 0.0],
                 [ 0.5,  0.5, 0.0],
                 [ 0.5,  0.5, 1.0],
                 [-0.5,  0.5, 1.0],
                 [-0.5,  0.5, 0.0],
                 [-0.5,  0.5, 1.0],
                 [ 0.0,  0.0, 1.5],
                 [ 0.5,  0.5, 1.0],
                 [ 0.0,  0.0, 1.5],
                 [ 0.5, -0.5, 1.0],
                 [ 0.0,  0.0, 1.5],
                 [-0.5, -0.5, 1.0]])

# Pasar como argumento el tipo de objeto que será el objeto virtual
import time, argparse, sys
from umucv.stream import sourceArgs
parser = argparse.ArgumentParser()
parser.add_argument('--objeto', help='Objeto 3D: casa (por defecto), piramide, reloj-arena', type=str, default=None) # args.objeto
sourceArgs(parser)
args, rest = parser.parse_known_args(sys.argv)
if args.objeto is not None:
    if args.objeto == "piramide":
        objeto = np.array([[-0.5, -0.5, 0.0],
                           [ 0.5, -0.5, 0.0],
                           [ 0.5,  0.5, 0.0],
                           [-0.5,  0.5, 0.0],
                           [-0.5, -0.5, 0.0],
                           [0.0,   0.0, 0.5],
                           [0.5,  -0.5, 0.0],
                           [0.0,   0.0, 0.5],
                           [0.5,   0.5, 0.0],
                           [0.0,   0.0, 0.5],
                           [-0.5,  0.5, 0.0]])
    if args.objeto == "reloj-arena":
        objeto = np.array([[-0.5, -0.5, 0.0],
                           [ 0.5, -0.5, 0.0],
                           [ 0.5,  0.5, 0.0],
                           [-0.5,  0.5, 0.0],
                           [-0.5, -0.5, 0.0],
                           [0.0,   0.0, 0.5],
                           [0.5,  -0.5, 0.0],
                           [0.0,   0.0, 0.5],
                           [0.5,   0.5, 0.0],
                           [0.0,   0.0, 0.5],
                           [-0.5,  0.5, 0.0],
                           [0.0,   0.0, 0.5],
                           [-0.5,  -0.5, 1.0],
                           [ 0.5, -0.5, 1.0],
                           [ 0.5,  0.5, 1.0],
                           [-0.5,  0.5, 1.0],
                           [-0.5, -0.5, 1.0],
                           [0.0,   0.0, 0.5],
                           [0.5,  -0.5, 1.0],
                           [0.0,   0.0, 0.5],
                           [0.5,   0.5, 1.0],
                           [0.0,   0.0, 0.5],
                           [-0.5,  0.5, 1.0],
                           [0.0,   0.0, 0.5]])
    

# filtramos una lista de contornos con aquellos
# que quedan reducidos a n vértices con la precisión deseada.
def polygons(cs,n,prec=1):
    rs = [ redu(c,prec) for c in cs ]
    return [r for r in rs if len(r) == n]

# Se obtienen las rotaciones de un contorno
def rots(c):
    return [np.roll(c,k,0) for k in range(len(c))]

# Se calcula la pose de la cámara (posición y orientación) en el espacio. Devuelve el error y la matriz
def pose(K, image, model):
    ok,rvec,tvec = cv.solvePnP(model, image, K, (0,0,0,0))
    if not ok:
        return 1e6, None
    R,_ = cv.Rodrigues(rvec)
    M = K @ jc(R,tvec)
    rms = rmsreproj(image,model,M)
    return rms, M

# Probamos todas las asociaciones de puntos imagen (view) con modelo (model)
# y nos quedamos con la que produzca menos error, 
# devolviendo el error y la pose de la cámara
def bestPose(K,view,model):
    poses = [ pose(K, v.astype(float), model) for v in rots(view) ]
    return sorted(poses,key=lambda p: p[0])[0]

# Marcador a detectar
marker = (np.array([[0,   0 , 0 ],
                    [0,   1, 0  ],
                    [0.5, 1, 0  ],
                    [0.5, 0.5, 0],
                    [1,   0.5, 0],
                    [1,   0,  0]]))

# Matriz de calibración de la cámara
K_Matriz = (np.array([[432.0, 0, 310],
                      [0, 432, 252],
                      [0, 0, 1]]))

# Se crea la ventana
cv.namedWindow("source")

desplazamiento = [0.5, 0.5, 0] # Dónde se tiene que desplazar el cubo
actual = [0.5, 0.5, 0] # Dónde se encuentra el cubo

# Si se pulsa la pantalla, se guarda el punto
from collections import deque
pulsado = False
point = deque(maxlen=1)
def fun(event, x, y, flags, param):
    global pulsado
    if event == cv.EVENT_LBUTTONDOWN:
        pulsado = True
        point.append((x,y))
cv.setMouseCallback("source", fun)

start = time.time()

for key,frame in autoStream():
    now = time.time()
    
    # Nos quedamos con los contornos que tengan 6 vértices
    g = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    cs = extractContours(g, minarea=5)
    good = polygons(cs, n=6, prec=3)
    
    # Si hay algún contorno de 6 vértices
    if len(good) > 0:
        # Para buscar el marcador, se prueban todas las posibles asociaciones de puntos. 
        # La más probable se considera la que menos error de reproyección tenga
        err_min, M_Matriz = bestPose(K_Matriz, good[0], marker)
        best = good[0]
        for g in good:
            err, Me = bestPose(K_Matriz, g, marker)
            if err < err_min:
                err_min = err
                best = g
                M_Matriz = Me

        # Si el error es pequeño, se ha encontrado un marcador
        if best is not None and err_min < 4:
            # Se dibuja en rojo el marcador encontrado
            cv.drawContours(frame,[best.astype(int)], -1, (0,0,255), 3, cv.LINE_AA)
            
            if len(point) == 1:
                if M_Matriz is None:
                    continue
                if pulsado:  
                    # Si se ha pulsado la pantalla, se calcula el punto 3D correspondiente (desplazamiento)
                    Matriz_sin_3_columna = np.delete(M_Matriz, 2, axis=1)
                    M_matriz_inv = np.linalg.inv(Matriz_sin_3_columna)
                    point_3D = htrans(M_matriz_inv, point[0])
                    desplazamiento = [point_3D[0], point_3D[1], 0]
                    pulsado = False
                if desplazamiento != actual:
                    # Tiempo transcurrido la última vez que se ha desplazado el cubo
                    tiempo_transcurrido = now - start
                    # Calcular el desplazamiento que se tiene que hacer para llegar al punto
                    desplazar_todo = np.array([desplazamiento[0]-actual[0], desplazamiento[1]-actual[1], 0])
                    # Calculamos el desplazamiento que se tiene que hacer en ese frame
                    desplazar = desplazar_todo / np.linalg.norm(desplazar_todo) * tiempo_transcurrido/1.5
                    if np.linalg.norm(desplazar_todo) < np.linalg.norm(desplazar):
                        desplazar = desplazar_todo
                    # Actualizamos la posición actual
                    actual = [actual[0] + desplazar[0], actual[1] + desplazar[1], 0]
                    # Se dibuja en verde el cubo en la posición actual
                    cube_position = htrans(M_Matriz, htrans(desp(actual), objeto))
                    cv.drawContours(frame,[cube_position.astype(int)], -1, (0,255,0), 3, cv.LINE_AA)
                else:
                    # Se dibuja en verde el cubo en la posición actual
                    cube_position = htrans(M_Matriz, htrans(desp(actual), objeto))
                    cv.drawContours(frame,[cube_position.astype(int)], -1, (0,255,0), 3, cv.LINE_AA)
            else:
                # Se dibuja en verde el cubo encima del marcador (es la posición actual)
                cube_position = htrans(M_Matriz, htrans(desp(actual), objeto))
                cv.drawContours(frame,[cube_position.astype(int)], -1, (0,255,0), 3, cv.LINE_AA)
    start = now
    cv.imshow('source',frame)