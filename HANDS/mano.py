#!/usr/bin/env python

import cv2 as cv
import numpy as np
from umucv.stream import autoStream
from umucv.util import putText
import math # Calcula el arcotangente
import subprocess # Abre y cierra programa.py
import os

# Calcular distancia entre 2 puntos
def distancia(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Calcula el ángulo entre el vector que va de p1 a p2 (u1, u2) y el vector horizontal (v1, v2)
def angulo_orientacion(p1, p2):
    u1 = p2[0] - p1[0]
    u2 = p2[1] - p1[1]
    v1 = 0
    v2 = 1
    return int(math.acos((u1*v1 + u2*v2)/(math.sqrt(u1**2 + u2**2)*math.sqrt(v1**2 + v2**2)))*180/math.pi)

# Usar el detector de manos de mediapipe
import mediapipe as mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

programa_abierto = False # ¿programa.py está abierto?
proceso = None # Proceso de programa.py
dedosLevantados = 0 # ¿Cuántos dedos hay levantados?
distFocal = 738 # Distancia focal de la cámara en píxeles
anchoPalma = 9 # Ancho de la palma en la vida real (cm)

# Devuelve la distancia de la mano a la cámara en cm
def distanciaACamara(anchoManoPixeles):
    return (distFocal*anchoPalma)/anchoManoPixeles

for key, frame in autoStream():
    H,W,_ = frame.shape
    
    imagecam = cv.flip(frame, 1) # Con modo espejo
    
    image = cv.cvtColor(imagecam, cv.COLOR_BGR2RGB)
    
    results = hands.process(image)
    
    points = [] # Los puntos de la mano
    
    # Si detecta manos, procesa la primera
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Meter los "landmarks" en un array de numpy
            for k in range(21):
                x = hand_landmarks.landmark[k].x # Entre 0 y 1
                y = hand_landmarks.landmark[k].y
                points.append([int(x*W), int(y*H)]) # int para dibujar en cv. x*W e y*H para que esté en píxeles
            break

        points = np.array(points) # Mejor un array para poder operar matemáticamente
        
        # Calcula el centro de la palma
        center = np.mean(
            [
                points[5], 
                points[17], 
                points[0]
            ], 
            axis=0
        ) 
        
        # Dibuja un circulo en la palma de la mano
        cv.circle(
            img = imagecam,
            center = center.astype(int),
            radius = int(distancia(points[17], center)),
            color = (255,0,0),
            thickness=-1 # -1->Rellenar
        )  
        
        # Dibuja líneas en los dedos
        cv.line(imagecam, points[5], points[8], (0,0,155), thickness=3)
        cv.line(imagecam, points[9], points[12], (0,0,155), thickness=3)
        cv.line(imagecam, points[13], points[16], (0,0,155), thickness=3)
        cv.line(imagecam, points[17], points[20], (0,0,155), thickness=3)
        cv.line(imagecam, points[1], points[4], (0,0,155), thickness=3)
        
        # Qué dedos hay levantados:
        # 0: Pulgar, 1: Índice, 2: Corazón, 3: Anular, 4: Meñique
        fingers = [0, 0, 0, 0, 0]
        if distancia(points[4], points[0]) > distancia(points[5], points[0]) :
            fingers[0] = 1
        if distancia(points[8], points[0]) > distancia(points[5], points[0]) :
            fingers[1] = 1
        if distancia(points[12], points[0]) > distancia(points[9], points[0]) :
            fingers[2] = 1
        if distancia(points[16], points[0]) > distancia(points[13], points[0]) :
            fingers[3] = 1
        if distancia(points[20], points[0]) > distancia(points[17], points[0]) :
            fingers[4] = 1
        
        #Si pones ñ o tildes en el texto, sale ??
        # ¿Qué dedos hay levantados? Escribe el texto (cv.putText) sobre un rectángulo blanco (cv.rectangle)
        cv.rectangle(
            img = imagecam,
            pt1 = (1, 10),
            pt2 = (500, 40),
            color = (255,255,255),
            thickness = -1
        )
        cv.putText(
            img = imagecam,
            text = str(fingers) + " = [Pulgar, Indice, Corazon, Anular, Menique]",
            org = (10, 30), 
            fontFace = cv.FONT_HERSHEY_SIMPLEX, 
            fontScale = 0.5, 
            color = (10,10,10),
            thickness = 1,
            lineType = cv.LINE_AA
        )
    
        # Calcula el ángulo de orientación de la mano
        angulo_mano = angulo_orientacion(points[9], points[0])
        if (points[0][0] < points[9][0]):
            angulo_mano = -angulo_mano # Calcula si el ángulo es positivo o negativo
        putText(imagecam, "Angulo de orientacion de la mano:" + f'{angulo_mano}', (10, 60))
        
        dedosLevantados = fingers[0]+fingers[1]+fingers[2]+fingers[3]+fingers[4]
        
        # Si se levantan 5 dedos, se abre programa.py. Si se cierran, se cierra programa.py
        if (dedosLevantados == 5) and (not programa_abierto):
            proceso = subprocess.Popen(["Python", "programa.py"])
            programa_abierto = True
        if (dedosLevantados == 0) and (programa_abierto):
            proceso.terminate()
            proceso = None
            programa_abierto = False
        
        # Calcula la distancia de la mano a la cámara
        anchoManoPixeles = distancia(points[9], points[0])
        distanciaManoACamara = distanciaACamara(anchoManoPixeles)
        putText(imagecam, "Distancia de la mano a la camara:" + f'{int(distanciaManoACamara)}', (10, 90))
    
    # Muestra el fotograma con las modificaciones hechas anteriormente.
    cv.imshow("mano.py", imagecam)
