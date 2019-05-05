
import argparse
parser = argparse.ArgumentParser(description='Train CatDog Model.')
parser.add_argument('modelpath', metavar='PATH', type=str,
                    help='path to saved h5 model.')
parser.add_argument('imagepath', metavar='PATH', type=str,
                    help='path to saved image to test.')

from keras.applications import VGG16
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras import optimizers
from keras.models import Sequential, Model, load_model
from keras.layers import Dropout, Flatten, Dense, Input

import numpy as np

classes = ['cat', 'dog']

def test(modelpath: str, imagepath: str) -> str:
    # dimensions of our images.
    img_width, img_height = 150, 150
    model: Model = load_model(modelpath)
    image = load_img(imagepath, target_size=(img_height, img_width))
    image = np.expand_dims(img_to_array(image), axis=0)

    return 'cat' if model.predict(image) < 0.5 else 'dog'


if __name__ == '__main__':
    args = parser.parse_args()
    prediction = test(args.modelpath, args.imagepath)
    print(f'That\'s a {prediction}!')
