# CLASIFICADOR
## Enunciado
Prepara una aplicación sencilla de reconocimiento de imágenes. Debe admitir (al menos) dos argumentos:

`--models=<directorio>`, la carpeta donde hemos guardado un conjunto de imágenes de objetos o escenas que queremos reconocer.

`--method=<nombre>`, el nombre de un método de comparación. 

Cada fotograma de entrada se compara con los modelos utilizando el método seleccionado y se muestra información sobre el resultado (el modelo más parecido o probable, las distancias a los diferentes modelos, alguna medida de confianza, etc.). Implementa inicialmente un método basado en el "embedding" obtenido por [mediapipe](https://developers.google.com/mediapipe/solutions/vision/image_embedder) (`code/DL/embbeder`).

## Ficheros
- Carpeta code: Aquí se encuentran los ficheros de código
- Carpeta images: Aquí se encuentran imágenes de prueba para el clasificador.
- Carpeta imports: Aquí se encuentran los ficheros importantes para el funcionamiento del programa.


## Código
### clasificadorConstructor.py
En este fichero se encuentra la clase 'Clasificador' cuyas subclases son los distintos métodos de clasificación que se pueden aplicar.

Esta clase tiene un atributo llamado method que tiene el nombre del método. Este es el nombre con el que se llama a ese método concreto en los parámetros de entrada del programa.

Tiene un método llamado similarity, que devuelve la similaridad del frame pasado como parámetro, con la imagen cuya ruta se pasa como parámetro.

### clasificadorColeccion.py

Contiene las subclases de la clase Clasificador. Cada subclase implementa similarity.

### clasificador.py
Es la clase principal del programa, es la que se ejecuta para que funcione el clasificador.

En primer lugar, se recogen los parámetros de entrada del programa (directorio de modelos y método de comparación). Se comprueba que se han pasado los dos parámetros necesarios, que no se han escrito parámetros no conocidos, y que el directorio de modelos existe.

Se obtiene el clasificador (de la clase Clasificador). Para ello, se recorren las subclases y se queda con la subclase cuyo atributo método coincide con el método pasado como parámetro. Si este no existe, se muestra un mensaje indicándolo y se cierra el programa.

Se empieza a capturar el vídeo. Por cada frame que se captura, se llama al método similarity del clasificador con el frame y cada una de las imágenes del directorio de modelos. Se almacena la similaridad de la imagen con mayor similaridad. Se muestra por pantalla el frame, el valor de similaridad mayor y el nombre de la imagen con mayor similaridad.