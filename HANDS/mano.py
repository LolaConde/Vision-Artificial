#!/usr/bin/env python

import cv2 as cv
import numpy as np
from umucv.stream import autoStream
from umucv.util import putText
import math # Calcula el arcotangente
import subprocess # Abre y cierra la terminal
import os

# Calcular distancia entre 2 puntos
def distancia(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def angulo_orientacion(p1, p2):
    # Vector que va de p1 a p2 = u1, u2
    u1 = p2[0] - p1[0]
    u2 = p2[1] - p1[1]
    # Vector horizontal = v1, v2
    v1 = 0
    v2 = 1
    # Devuelve el ángulo entre el vector que va de p1 a p2 y el vector horizontal
    return int(math.acos((u1*v1 + u2*v2)/(math.sqrt(u1**2 + u2**2)*math.sqrt(v1**2 + v2**2)))*180/math.pi)

# Usar el detector de manos de mediapipe
import mediapipe as mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

terminal_abierta = False # Si es True, la terminal está abierta. Si es False, la terminal está cerrada
proceso = None # Proceso de la terminal
dedosLevantados = 0

# Distancia focal de la cámara en píxeles
distFocal = 738
# Ancho de la palma en la vida real (cm)
anchoPalma = 9

def distanciaACamara(anchoManoPixeles):
    # Devuelve la distancia de la mano a la cámara en cm
    return (distFocal*anchoPalma)/anchoManoPixeles

# Recorrer todos los fotogramas del flujo de entrada
for key, frame in autoStream():
    H,W,_ = frame.shape # Alto y ancho de la imagen
    
    # Es mejor trabajar con imagen espejo
    imagecam = cv.flip(frame, 1) # Con modo espejo
    
    # El detector necesita tener los canales de color en el orden correcto
    image = cv.cvtColor(imagecam, cv.COLOR_BGR2RGB)
    
    # Lanzamos el proceso de detección principal mágico que hace mediapipe
    results = hands.process(image)
    
    # Array donde se meterán los puntos de la mano
    points = []
    
    # Si detecta manos
    if results.multi_hand_landmarks:
        # Para cada mano detectada
        for hand_landmarks in results.multi_hand_landmarks:
            # Meter los "landmarks" en un array de numpy
            for k in range(21):
                x = hand_landmarks.landmark[k].x # Entre 0 y 1
                y = hand_landmarks.landmark[k].y
                points.append([int(x*W), int(y*H)]) # int para dibujar en cv
            # Solo se procesa una mano
            break

        points = np.array(points) # Mejor un array para poder operar matemáticamente
        
        # Calcula el centro de la palma. 
        center = np.mean(
            # Hace la media de los puntos 5, 17 y 0.
            [
                points[5], 
                points[17], 
                points[0]
            ], 
            # axis=0 para que de valores en x e y
            axis=0
        ) 
        
        # Dibuja un circulo en la palma de la mano
        cv.circle(
            img = imagecam, # En imagecam
            center = center.astype(int), # Centro del circulo = centro de la palma
            radius = int(distancia(points[17], center)), # radio = distancia entre el centro de la plama y el punto 17.
            color = (255,0,0), # Color = 255 0 0
            thickness=-1 # -1->Rellenar
        )  
        
        # Dibuja líneas en los dedos
        cv.line(imagecam, points[5], points[8], (0,0,155), thickness=3) # Dibuja la línea entre los puntos 5 y 8. Color = 0 0 155. Grosor = 3
        cv.line(imagecam, points[9], points[12], (0,0,155), thickness=3)
        cv.line(imagecam, points[13], points[16], (0,0,155), thickness=3)
        cv.line(imagecam, points[17], points[20], (0,0,155), thickness=3)
        cv.line(imagecam, points[1], points[4], (0,0,155), thickness=3)
        
        # Qué dedos hay levantados:
        # 0: Pulgar, 1: Índice, 2: Corazón, 3: Anular, 4: Meñique
        fingers = [0, 0, 0, 0, 0]
        # Pulgar
        if distancia(points[4], points[0]) > distancia(points[5], points[0]) :
            fingers[0] = 1
        # Índice
        if distancia(points[8], points[0]) > distancia(points[5], points[0]) :
            fingers[1] = 1
        # Corazón
        if distancia(points[12], points[0]) > distancia(points[9], points[0]) :
            fingers[2] = 1
        # Anular
        if distancia(points[16], points[0]) > distancia(points[13], points[0]) :
            fingers[3] = 1
        # Meñique
        if distancia(points[20], points[0]) > distancia(points[17], points[0]) :
            fingers[4] = 1
        
        #Si pones ñ o tildes en el texto, sale ??
        # ¿Qué dedos hay levantados? Escribe el texto (cv.putText) sobre un rectángulo blanco (cv.rectangle)
        cv.rectangle(
            img = imagecam, # En imagecam 
            pt1 = (1, 10), # El rectángulo empieza en el punto (1,10)
            pt2 = (500, 40), # El rectángulo acaba en el punto (500,40)
            color = (255,255,255), # El rectángulo es blanco (255,255,255)
            thickness = -1 # Rellena el rectángulo (no sólo el borde)
        )
        cv.putText(
            img = imagecam, # En imagecam
            text = str(fingers) + " = [Pulgar, Indice, Corazon, Anular, Menique]", # Escribe el texto
            org = (10, 30), #El texto empieza en el punto (10,30)
            fontFace = cv.FONT_HERSHEY_SIMPLEX, # Fuente del texto
            fontScale = 0.5, # Tamaño del texto
            color = (10,10,10), # Color del texto
            thickness = 1, # Grosor del texto
            lineType = cv.LINE_AA # Tipo de línea
        )
    
        # Calcula el ángulo de orientación de la mano
        angulo_mano = angulo_orientacion(points[9], points[0])
        # Calcula si el ángulo es positivo o negativo
        if (points[0][0] < points[9][0]):
            angulo_mano = -angulo_mano
        # Escribe el ángulo de orientación de la mano
        putText(imagecam, "Angulo de orientacion de la mano:" + f'{angulo_mano}', (10, 60))
        
        # Calcula cuantos dedos hay levantados
        dedosLevantados = fingers[0]+fingers[1]+fingers[2]+fingers[3]+fingers[4]
        
        # Si se levantan 5 dedos, se abre programa.py. Si se cierran, se cierra programa.py
        if (dedosLevantados == 5) and (not terminal_abierta):
            proceso = subprocess.Popen(["Python", "programa.py"])
            terminal_abierta = True
        if (dedosLevantados == 0) and (terminal_abierta):
            proceso.terminate()
            proceso = None
            terminal_abierta = False
        
        # Calcula la distancia de la mano a la cámara
        anchoManoPixeles = distancia(points[9], points[0])
        distanciaManoACamara = distanciaACamara(anchoManoPixeles)
        # Imprime la distancia de la mano a la cámara
        putText(imagecam, "Distancia de la mano a la camara:" + f'{int(distanciaManoACamara)}', (10, 90))
    
    # Muestra el fotograma con las modificaciones hechas anteriormente. La ventana en la que se ve este se llama "mano.py"
    cv.imshow("mano.py", imagecam)
