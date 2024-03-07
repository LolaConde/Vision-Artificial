from clasificadorConstructor import *
# Imports de embedding 
# !wget -O embedder.tflite -q https://storage.googleapis.com/mediapipe-models/image_embedder/mobilenet_v3_small/float32/1/mobilenet_v3_small.tflite
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2 as cv

class embedder(Clasificador):
    def __init__(self):
        options = vision.ImageEmbedderOptions(
            base_options = python.BaseOptions(model_asset_path='../imports/embedder.tflite'),
            l2_normalize = True,
            quantize     = True
        )
        self.embedder = vision.ImageEmbedder.create_from_options(options)
        super().__init__("embedder")
        
    def similarity(self, frame, img_path):
        mp_image = mp.Image.create_from_file(img_path)
        mp_image2 = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        embedding_result = self.embedder.embed(mp_image)
        embedding_result2 = self.embedder.embed(mp_image2)
        return vision.ImageEmbedder.cosine_similarity(embedding_result.embeddings[0], embedding_result2.embeddings[0])
    
