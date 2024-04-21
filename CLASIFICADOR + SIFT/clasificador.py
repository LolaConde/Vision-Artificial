#!/usr/bin/env python

import cv2 as cv
from umucv.stream import autoStream
from umucv.stream import sourceArgs
import os
import argparse, sys
from clasificadorConstructor import *
from clasificadorColeccion import *

# Argumentos
parser = argparse.ArgumentParser()
parser.add_argument('--models', help='Imágenes de los objetos o escenas que se quieren reconocer', type=str, default=None) # args.models
parser.add_argument('--method', help='Nombre del método de comparación', type=str, default=None) # args.method
sourceArgs(parser)
args, rest = parser.parse_known_args(sys.argv)
assert len(rest)==1, 'Parámetros desconocidos: '+str(rest[1:])
# Comprobaciones
if args.models is None or args.method is None:
    print("Falta alguno de los parámetros obligatorios")
    sys.exit(1)
if not os.path.isdir(args.models):
    print(f"La carpeta {args.models} no existe.")
    sys.exit(1)

# Obtener el clasificador
clasificador_actual = None
for subclase in Clasificador.__subclasses__():
    if subclase.getMethod() == args.method: # Si el método coincide con el argumento pasado por línea de comandos
        clasificador_actual = subclase
        break
if clasificador_actual is None:
    print(f"El método {args.method} no existe.")
    sys.exit(1)
    
# Creación de una lista de clasificadores (uno por cada imagen en la carpeta)
clasificadores = []
for filename in os.listdir(args.models):
    clasificadores.append(clasificador_actual(os.path.join(args.models, filename), filename))

for key,frame in autoStream():
    clasificador_actual.changeFrame(frame.copy())
    # Obtener la similitud más alta de las imágenes en la carpeta
    similarity = -1
    for clasificador in clasificadores:
        similarity_i, frame_i = clasificador.similarity()
        if(similarity < similarity_i):
            similarity = similarity_i
            frame = frame_i

    cv.imshow("similarity", frame)
