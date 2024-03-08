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
    if subclase().method == args.method:
        clasificador_actual = subclase()
        break
if clasificador_actual is None:
    print(f"El método {args.method} no existe.")
    sys.exit(1)

for key,frame in autoStream():
    # Obtener la similitud más alta de las imágenes en la carpeta
    similarity = -1
    file = ""
    for filename in os.listdir(args.models):
        similarity_i = clasificador_actual.similarity(frame, os.path.join(args.models, filename))
        if(similarity < similarity_i):
            similarity = similarity_i
            file = filename
    # Mostrar la similitud del frame con la imagen más similar
    W = frame.shape[1]
    cv.rectangle(frame,(0,0),(int(similarity*W), 20), color=(0,255,0), thickness=-1)
    cv.putText(frame, f"{similarity:.2f}", (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
    # Mostrar el nombre del archivo con la similitud más alta
    cv.putText(frame, file, (0, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)

    cv.imshow("similarity", frame)
