import tensorflow.keras
import cv2
import pygame
from PIL import Image, ImageOps
import numpy as np

np.set_printoptions(suppress=True)

def classifying(filename, modelname):
    #loading model
    model = tensorflow.keras.models.load_model(modelname)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(filename)

    # resize the image to a 224x224 with the same strategy as in Teachable Machines
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    #normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)

    d = {}
    with open("labels.txt") as f:
        for line in f:
            (key, val) = line.split()
            d[int(key)] = val

    p_list = prediction.tolist()
    max_index = p_list[0].index(max(p_list[0]))

    return d[max_index]

def convertion(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "RGB")
    img = pygame.transform.scale(img, (320, 240))
    return img