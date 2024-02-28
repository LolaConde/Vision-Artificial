# FILTROS

## Índice

- [Enunciado](#enunciado)
- [Filtros disponibles](#filtros-disponibles)
    - [Blanco y negro](#blanco-y-negro)
    - [Filtro box](#filtro-box)
    - [Filtro gaussiano](#filtro-gaussiano)
    - [Filtro de mediana](#filtro-de-mediana)
    - [Filtro bilateral](#filtro-bilateral)
    - [Filtro del mínimo](#filtro-del-mínimo)
    - [Filtro del máximo](#filtro-del-máximo)
    - [Transformación de valor](#transformación-de-valor)
    - [Ecualizador de histograma](#ecualizador-del-histograma)
    - [CLAHE](#clahe)
    - [Opening](#opening)
- [Qué se ha realizado](#qué-se-ha-realizado)
- [Bibliografía usada](#bibliografía-usada)

## Enunciado
Muestra en vivo el efecto de diferentes filtros, seleccionando con el teclado el filtro deseado y modificando sus parámetros (p.ej. el nivel de suavizado) con trackbars. Aplica el filtro en un ROI para comparar el resultado con el resto de la imagen.

## Filtros disponibles

### Blanco y negro

En primer lugar, con el uso de la librería OpenCV se pasa a gris el color de la región de interés. Esto deja la imagen con 1 canal.

En segundo lugar, se vuelve a pasar a BGR porque este es el formato de la imagen completa. Al sobreescribir la región de interés (seleccionada) con el filtro correspondiente, lo que se escribe debe tener el mismo formato que el resto de la imagen (del fotograma).

### Filtro box

Se utiliza una función de OpenCV que lo realiza. Esta función utiliza un kernel de todos unos para que cada pixel se transforme en una media entre sus vecinos, consiguiendo así un efecto de emborronamiento.

### Filtro gaussiano

Se utiliza una función de OpenCV que lo realiza.

Una función gaussiana tiene una forma tal que los valores centrales tienen un mayor valor en la componente y que los lejanos al centro. El filtro gaussiano hace algo parecido, de forma que tiene valores mayores en el centro de la matriz utilizada, y valores cada vez más pequeños conforme se aleja del centro de la matriz.

Se puede indicar el tamaño de la desviación estándar en x. Si esta es muy pequeña, el filtro no tendrá mucho efecto. Si es muy grande, la imagen se verá muy emborronada.

Esto es beneficioso para suavizar imágenes y reducir el ruido sin perder demasiada información de detalle. Al contrario que ocurría con el filtro box, que podía añadir ruido a la imagen, el filtro gaussiano no añade ruido.

### Filtro de mediana

Se utiliza una función de OpenCV.

Este filtro hace que cada pixel se transforme en la mediana de sus vecinos y él mismo.

También se utiliza para reducir el ruido, eliminando los puntos aislados de alta o baja intensidad.

### Filtro bilateral

Se utiliza una función de OpenCV que lo realiza.

Tal y como indica la [documentación de OpenCV](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga564869aa33e58769b4469101aac458f9), este filtro es muy util para reducir el ruido mientras se mantiene la nitidez de los bordes. El inconveniente es que es más lento que la mayoría de los otros filtros.

Este filtro utiliza dos filtros gaussianos, primero hace que los píxeles cercanos tengan más peso que los lejanos, y segundo hace que los píxeles con valores de intensidad similares tengan más peso. 

De esta forma, se consigue que sólo se escojan para el suavizado los píxeles cercanos y con valores similares, lo que hace que los bordes se mantengan nítidos.

### Filtro del mínimo

Se utiliza una función de la librería SciPy.

Este filtro hace que cada pixel se transforme en el valor mínimo de sus vecinos y él mismo. La cantidad de vecinos viene determinada por un parámetro pasado como argumento a la función.


### Filtro del máximo

Se utiliza una función de la librería SciPy.

Este filtro hace lo contrario que el anterior, ya que en lugar de tomar el valor mínimo de sus vecinos, toma el valor máximo.

La cantidad de vecinos también viene determinada por un parámetro pasado como argumento a la función.

### Transformación de valor

Los píxeles de las imágenes pueden ser modificados individualmente sin tener en cuenta su entorno. En este caso, la modificación implica el aumento constante de la luminancia de los píxeles, lo que resulta en un aclarado u oscurecimiento de la imagen.

### Ecualizador del histograma

Se utiliza una función de OpenCV que lo realiza.

El histograma de una imagen es una representación gráfica de los valores de los píxeles de esta. En este caso, se ha querido ecualizar los valores de luminancia de la imagen, transformando la distribución de los valores para abarcar todo el rango de valores posibles

De esta forma, se se aumenta el contraste de la imagen y haciendo que los detalles sean más visibles. Estos detalles antes podían haber estado ocultos por sobreexposición o subexposición.

Si se quiere leer más información al respecto, se puede consultar la [documentación de OpenCV](https://docs.opencv.org/3.4/d4/d1b/tutorial_histogram_equalization.html).

### CLAHE

Se utiliza una función de OpenCV que implementa CLAHE.

El ecualizador de histogramas global (el anterior) no consigue mejorar en gran medida las zonas de las imágenes muy claras u oscuras en relación con el resto de la imagen. Esto es debido a que el ecualizador de histogramas no tiene en cuenta la distribución de los valores de los píxeles en zonas concretas de la imagen, sino la distribución global.

Por otro lado, CLAHE utiliza varios histogramas locales, en lugar de uno global, para ecualizar la imagen. Esto permite mejorar las zonas de la imagen que antes no se podían mejorar con el ecualizador de histogramas global.

También es importante destacar que CLAHE limita el contraste de las regiones antes de realizar la ecualización, evitando así la amplificación del ruido en áreas con valores constantes.

### Opening

Se utiliza una función de OpenCV. Si se quiere saber más, se puede consultar la [siguiente url](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html#gsc.tab=0).

El opening es una operación morfológica que consiste en aplicar una erosión seguida de una dilatación. Esto es útil para eliminar el ruido de las imágenes.

La erosión en imágenes con solo valores 1 o 0, hace que los píxeles sólo tengan 1 si los píxeles de su alrededor sólo tienen valor 1 (el resto tienen valor 0). La dilatación en ese contexto realiza lo contrario, solo los píxeles que estén rodeados de píxeles de valor 0 se convierten en 0 (el resto son 1s).

Sin embargo, por la manera en la que se implementa en OpenCV, la erosión pone en cada píxel el valor mínimo de los que está rodeado, y la dilatación pone el valor máximo de los que está rodeado.

De esta forma, al aplicar opening a la componente de luminancia de una imagen, se consigue que los píxeles que estén rodeados de píxeles con valores de luminancia muy bajos se conviertan en píxeles con valores de luminancia muy bajos, y los píxeles que estén rodeados de píxeles con valores de luminancia muy altos se conviertan en píxeles con valores de luminancia muy altos, eliminando así los brillos blancos pequeños que puedan formarse en la imagen por la luz.

## Qué se ha realizado

En primer lugar, se ha creado la clase "Filtro" con subclases, cada una representando un filtro mencionado anteriormente. Cada subclase tiene un identificador (la tecla asociada para activarlo), un nombre, un método para aplicar el filtro a una imagen, y otro para agregar los trackbars necesarios a la ventana.

Posteriormente, el flujo de ejecución es el siguiente:

1. Se recibe cada fotograma
2. Si se ha presionado una tecla correspondiente a un filtro, se guarda el filtro seleccionado. Si se cambia de filtro, se vuelve a crear la ventana y se añaden trackbars correpondientes al filtro seleccionado. Esto ocurre porque no se pueden eliminar los trackbars del filtro anterior salvo si se elimina y se vuelve a crear la ventana.
3. Si se ha presionado una tecla para visualizar solo la región de interés o todo el fotograma, o para alternar entre color y blanco y negro, se registra la opción seleccionada.
4. Si se presiona la tecla "h", se muestra u oculta la ayuda.
5. Se guarda la región de interés seleccionada.
6. Se aplica el filtro seleccionado a la sección de interés, y se escribe el nombre del filtro.
8. Se pasa a blanco y negro la región de interés si así se ha seleccionado.
9. Se dibuja un rectángulo alrededor de la sección de interés.
10. Se muestra el fotograma o la región de interés.

## Bibliografía usada

[Filtros usados de OpenCV](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html)

[Más documentación de OpenCV](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga564869aa33e58769b4469101aac458f9)

[Ecualizador de histogramas de OpenCV](https://docs.opencv.org/3.4/d4/d1b/tutorial_histogram_equalization.html)

[Preguntas a ChatGPT para aclarar conceptos](https://chat.openai.com)

[CLAHE](https://en.wikipedia.org/wiki/Adaptive_histogram_equalization)

[Función morphologyEx()](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga67493776e3ad1a3df63883829375201f)

[Función erode()](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gaeb1e0c1033e3f6b891a25d0511362aeb)

[Función dilate()](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga4ff0f3318642c4f469d0e11f242f3b6c)

[Como añadir trackbars a una ventana con OpenCV](https://docs.opencv.org/3.4/da/d6a/tutorial_trackbar.html)

[Acceder a las subclases de una clase en Python](https://stackoverflow.com/questions/3862310/how-to-find-all-the-subclasses-of-a-class-given-its-name)