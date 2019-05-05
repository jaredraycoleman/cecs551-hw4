# This fine-tuning code was taken from Keras documentation and modified slightly to have only
# a single dense neuron that is fine-tuned.
 
import argparse
parser = argparse.ArgumentParser(description='Train CatDog Model.')
parser.add_argument('datapath', metavar='PATH', type=str,
                    help='path to data files.')
parser.add_argument('-o', '--output', metavar='PATH', 
                    type=str, default=None,
                    help='path to save the model to.')

from keras.applications import VGG16
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential, Model
from keras.layers import Dropout, Flatten, Dense, Input
 
import os 

def train(datapath: str, savepath: str = None) -> None:
    # dimensions of our images.
    img_width, img_height = 150, 150
    
    train_data_dir = os.path.join(datapath, 'train')
    validation_data_dir = os.path.join(datapath, 'test')
    nb_train_samples = 30000 
    nb_validation_samples = 900 
    epochs = 2
    batch_size = 16
    
    # Build the VGG16 network
    input_tensor = Input(shape=(150,150,3))
    base_model = VGG16(weights='imagenet', include_top=False, input_tensor=input_tensor)
    # Add an additional MLP model at the "top" (end) of the network
    top_model = Sequential()
    top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
    top_model.add(Dense(1, activation='sigmoid'))
    model = Model(input=base_model.input, output=top_model(base_model.output))
    
    # Freeze all the layers in the original model (fine-tune only the added Dense layers)
    for layer in model.layers[:len(model.layers)-1]:       # Freeze all but final layers
        layer.trainable = False

    # Compile the model with a SGD/momentum optimizer and a slow learning rate.
    model.compile(loss='binary_crossentropy',
                optimizer=optimizers.SGD(lr=1e-3, momentum=0.9),
                metrics=['accuracy'])
    
    # Prepare data augmentation configuration
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)
    
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    
    train_generator = train_datagen.flow_from_directory(
        str(train_data_dir),
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary')
    
    validation_generator = test_datagen.flow_from_directory(
        str(validation_data_dir),
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary')
    
    # Fine-tune the model
    model.fit_generator(
        train_generator,
        samples_per_epoch=nb_train_samples//batch_size,
        epochs=epochs,                         
        validation_data=validation_generator,
        validation_steps=nb_validation_samples)      


    if savepath:
        model.save(savepath)

# def tune(lr_range: List[float, float],
#          momentum)

if __name__ == '__main__':
    args = parser.parse_args()
    train(args.datapath, savepath=args.output)