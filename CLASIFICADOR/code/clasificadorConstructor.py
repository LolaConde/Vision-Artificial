class Clasificador:
    def __init__(self, imgPath, nombreImg): # Constructor
        self.nombreImg = nombreImg
    def similarity(self): # Devuelve la similaridad entre la imagen (pasada en el constructor) y el frame almacenado
        return 0
    def getNombreImg(self): # Devuelve el nombre de la imagen
        return self.nombreImg
    @staticmethod
    def getMethod(): # Devuelve el nombre del método de comparación
        return ""
    @classmethod
    def changeFrame(cls, frame): # Guarda el frame actual en la clase (para comparar con la imagen)
        return