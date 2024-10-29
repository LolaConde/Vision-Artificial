# Ejercicios de Visión Artificial

Este repositorio contiene los ejercicios realizados en la asignatura de Visión Artificial del grado de Ingeniería Informática de la Universidad de Murcia. 

Hay ejercicios de detección de una mano, clasificador de objetos, rectificación de imágenes para toma de medidas, desplazamiento de un objeto virtual en tiempo real, etc.

## Tecnologías

Los ejercicios han sido realizados en **Python**, utilizando librerías como **OpenCV** y **Numpy**. Para la documentación de los ejercicios se ha utilizado **Jupyter Notebook**.

## Organización

Cada ejercicio se encuentra en una carpeta distinta, con el nombre del ejercicio. Dentro de cada carpeta, se encuentra:

- La documentación en un notebook con el mismo nombre que la carpeta (y en formato HTML)
- Una carpeta llamada *img* con las imágenes usadas en la documentación
- Archivos necesarios para la realización del ejercicio
 
 A su vez, se encuentra con el nombre de "Memoria" un documento ipynb y el correspondiente HTML con todo el contenido de las memorias individuales de cada ejercicio, de modo que se pueda acceder a ellas de forma conjunta si así se desea.
## Ejercicios realizados

- [**HANDS**](./HANDS): **Detecta una mano** en la cámara e indica su distancia a la cámara, los dedos levantados, y su ángulo de orientación. Además, se controla una aplicación abriendo y cerrando la mano.

- [**FILTROS**](./FILTROS): **Muestra en vivo distintos filtros**, seleccionando con el teclado el filtro deseado. Se pueden modificar los parámetros de los filtros. Los filtros utilizados se explican en la memoria.

- [**CLASIFICADOR+SIFT**](./CLASIFICADOR%20+%20SIFT/): **Clasificador en tiempo real** de objetos o escenas. Se indica el directorio de imágenes a reconocer y el método de comparación, y el programa clasifica los objetos o escenas en tiempo real.

- [**RECTIF**](./RECTIF): **Calculo de la distancia real entre dos puntos clicados sobre una imagen**. Se debe incluir referencias conocidas en la imagen (coordenadas de puntos conocidos tanto en la imagen como en el mundo real).

- [**RA**](./RA): **Desplazamiento de un objeto virtual** clicando donde se debe desplazar. Se debe de mostrar en la cámara un marcador como punto de referencia.

- [**MAPA**](./MAPA): A partir de una imagen con dos puntos de los que se conoce su localización, **se calcula la posición desde la que se ha tomado una imagen**. No se trata de un programa, sino de un ejercicio realizado en un notebook.

- [**FILTROSII**](./FILTROSII/): (Notebook)
    - Se comprueba la propiedad de "cascading" y "separabilidad" del filtro gaussiano
    - Se **implementa** desde cero el **algoritmo de convolución** con una máscara general
    - Se **implementa el box filter con la imagen integral**

- [**POLYGON**](./POLYGON/): Implementa un procedimiento para **mejorar la aproximación poligonal** obtenida por el método cv.approxPolyDP permitiendo vértices fuera del contorno de entrada. Todo se muestra en un notebook.

- [**MODEL3D**](./MODEL3D/): Utiliza la herramientas **COLMAP** para construir un modelo 3D de un objeto.