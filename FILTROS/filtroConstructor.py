class Filtro:
    def __init__(self, nombre, id): # Constructor
        self.nombre = nombre
        self.id = id
    def applyFilter(self, frame): # Aplica el filtro a un frame
        return frame
    def crearTrackbar(self, nombreVentana): # Crea los trackbars necesarios para el filtro
        return