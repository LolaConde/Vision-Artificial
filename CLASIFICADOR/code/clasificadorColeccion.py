from clasificadorConstructor import *
# Imports de embedding 
# !wget -O embedder.tflite -q https://storage.googleapis.com/mediapipe-models/image_embedder/mobilenet_v3_small/float32/1/mobilenet_v3_small.tflite
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2 as cv
# Imports de hog
from skimage.feature import hog
from umucv.util import putText

class embedder(Clasificador):
    def __init__(self, imgPath, nombreImg):
        # Si la clase aún no ha sido inicializada, se inicializa
        cls = self.__class__
        if not hasattr(cls, 'embedder'):
            cls.inicializoClase()
        # Guarda el embedding de la imagen
        img = mp.Image.create_from_file(imgPath)
        self.embeddingImg = cls.embedder.embed(img).embeddings[0]
        self.img = cv.imread(imgPath, cv.IMREAD_COLOR)
        super().__init__(imgPath, nombreImg)
        
    def getMethod():
        return "embedder"
    
    @classmethod
    def inicializoClase(cls):
        # Guardar el modelo de la carpeta imports
        options = vision.ImageEmbedderOptions(
            base_options = python.BaseOptions(model_asset_path='../imports/embedder.tflite'),
            l2_normalize = True,
            quantize     = True
        )
        cls.embedder = vision.ImageEmbedder.create_from_options(options)
    
    @classmethod
    def changeFrame(cls, frame):
        # Guarda el embedding del frame
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        cls.embeddingFrame = cls.embedder.embed(mp_image).embeddings[0]
        cls.frame = frame
    
    def similarity(self):
        cls = self.__class__
        # Similaridad entre la imagen y el frame
        similarity = vision.ImageEmbedder.cosine_similarity(self.embeddingImg, self.__class__.embeddingFrame)
        # Mostrar la similitud del frame con la imagen más similar
        frame_modificado = self.__class__.frame.copy()
        W = frame_modificado.shape[1]
        cv.rectangle(frame_modificado,(0,0),(int(similarity*W), 20), color=(0,255,0), thickness=-1)
        cv.putText(frame_modificado, f"{similarity:.2f}", (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
        # Mostrar la imagen en la esquina superior izquierda
        h = int(cls.frame.shape[0] * 0.2)
        w = int(self.img.shape[1] * h / self.img.shape[0])
        imgSmall = cv.resize(self.img, (w, h))
        frame_modificado[22:22+h, 1:1+w] = imgSmall
        return similarity, frame_modificado
    
class skimageHog(Clasificador):
    
    PPC = 16 # Tamaño de la celda (16 * 16)
    CPB = 2 # Tamaño del bloque (2 * 2)
    
    def __init__(self, imgPath, nombreImg):
        # HOG aplanado de la imagen
        self.img = cv.imread(imgPath, cv.IMREAD_COLOR)
        img = cv.imread(imgPath, cv.IMREAD_GRAYSCALE)
        hog_imagen = hog( img,
            visualize = False, # Solo devuelve el HOG
            transform_sqrt=True, # Normaliza la imagen antes de procesarla
            feature_vector=False, # No transforma el HOG en un vector antes de retornarlo
            orientations = 8, # Número de orientaciones
            pixels_per_cell = (self.PPC,self.PPC),
            cells_per_block = (self.CPB,self.CPB),
            block_norm = 'L1' # Método de normalización de los bloques
            )
        self.hog_aplanado_Img = hog_imagen.flatten()
        # Altura y anchura del hog
        self.hImg, self.wImg = hog_imagen.shape[:2]
        super().__init__(imgPath, nombreImg)
    
    @classmethod
    def changeFrame(cls, frame):
        # HOG del frame aplanado
        cls.hog_frame = hog( cv.cvtColor(frame, cv.COLOR_BGR2GRAY), visualize = False, transform_sqrt=True, feature_vector=False, orientations = 8, pixels_per_cell = (cls.PPC,cls.PPC), cells_per_block = (cls.CPB,cls.CPB), block_norm = 'L1' )
        # altura y anchura del hog
        cls.hFrame, cls.wFrame = cls.hog_frame.shape[:2]
        cls.frame = frame
    
    def getMethod():
        return "skimageHog"
        
    def similarity(self):
        cls = self.__class__
        # La imagen podría estar en cualquier parte del frame, por lo que se recorre el hog del frame. 
        # Se guarda en detected todos los lugares observados y su diferencia con la imagen
        detected = []
        for j in range(cls.hFrame-self.hImg):
            for k in range(cls.wFrame-self.wImg):
                # Comparación de la imagen con un trozo del frame
                vr = cls.hog_frame[j:j+self.hImg , k:k+self.wImg].flatten()
                detected.append((sum(abs(vr-self.hog_aplanado_Img))/len(vr), j, k))
        # Si no se ha podido comparar porque la imagen es más grande que el frame
        if (len(detected) == 0):
            return 0, cls.frame 
        # Se guarda la menor diferencia y donde empieza en el frame
        dmin, jmin , kmin = min(detected)
        # Inicio (en píxeles)
        x1 = kmin*self.PPC
        y1 = jmin*self.PPC
        # Final (en píxeles)
        x2 = x1 + (self.wImg+self.CPB-1)*self.PPC
        y2 = y1 + (self.hImg+self.CPB-1)*self.PPC
        # Se dibuja un rectángulo en el frame que indica donde se ha encontrado la imagen
        frame_modificado = cls.frame.copy()
        cv.rectangle(frame_modificado, (x1,y1), (x2,y2), color=(255,255,255), thickness=2)
        # Modifica el frame para mostrar la diferencia
        putText(frame_modificado, "Distancia entre el frame y la imagen: " + f'{dmin:.2f}', orig=(5,15), color=(200,255,200))
        # Mostrar la imagen en la esquina superior izquierda
        h = int(cls.frame.shape[0] * 0.2)
        w = int(self.img.shape[1] * h / self.img.shape[0])
        imgSmall = cv.resize(self.img, (w, h))
        frame_modificado[22:22+h, 1:1+w] = imgSmall
        return 1-dmin, frame_modificado 

class sift(Clasificador):
    def __init__ (self, imgPath, nombreImg):
        # Si la clase aún no ha sido inicializada, se inicializa
        cls = self.__class__
        if not hasattr(cls, 'sift'):
            cls.inicializoClase()
        # Keypoints de la imagen
        img = cv.imread(imgPath, cv.IMREAD_GRAYSCALE)
        self.img = cv.imread(imgPath, cv.IMREAD_COLOR)
        self.keypoints_img, self.descriptors_img = cls.sift.detectAndCompute(img, None)
        super().__init__(imgPath, nombreImg)
        
    @classmethod
    def inicializoClase(cls):
        # Comparador de keypoints
        cls.bf = cv.BFMatcher()
        # Detector de keypoints
        cls.sift = cv.SIFT_create(nfeatures = 500)
    
    def getMethod():
        return "sift"
    
    @classmethod
    def changeFrame(cls, frame):
        # Keypoints del frame
        cls.keypoints_frame, cls.descriptors_frame = cls.sift.detectAndCompute(frame, None)
        cls.frame = frame

    def similarity(self):
        cls = self.__class__
        # Solicitamos las dos mejores coincidencias de cada punto
        matches = cls.bf.knnMatch(self.descriptors_img, cls.descriptors_frame, k=2)
        # Se guardan los matches que pasan el test de ratio
        good = []
        for m in matches:
            if len(m) >= 2:
                best, second = m
                if best.distance < 0.75*second.distance:
                    good.append(best)
        # Redimensiona la imagen pequeña
        h = int(cls.frame.shape[0] * 0.2)
        w = int(self.img.shape[1] * h / self.img.shape[0])
        imgSmall = cv.resize(self.img, (w, h))
        # Se dibujan los matches
        imgm = cv.drawMatches(imgSmall, self.keypoints_img, cls.frame, cls.keypoints_frame, good,
            flags=0,
            matchColor=(128,255,128),
            singlePointColor = (128,128,128),
            outImg=None)

        putText(imgm ,f'{len(good)} matches', 
            orig=(5,36), color=(200,255,200)) 
        # Se devuelve la similaridad (porcentaje de matches respecto a los keypoints de la imagen)
        return len(good)/(len(self.keypoints_img)), imgm