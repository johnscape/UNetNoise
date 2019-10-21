from ImageHandler import ImageGenerator
from unet import CreateUnet
from PIL import Image
import numpy as np
from keras import Model
import random
from keras.callbacks import ModelCheckpoint

def ConvertImage(imageObject: Image):
    return np.array(imageObject)

def WhiteWash(imageObject):
    conv = imageObject.convert('L')
    array = np.array(conv)
    return np.where(array>0,1,0)


#generate images
#generator = ImageGenerator("masks", "noise", "gen")
#generator.GenerateImages(500, 20)

training_set = []
mask_set = []
for i in range(30):
    file_name = str(i + 1).zfill(3) + ".png"
    img = Image.open("gen/generated/" + file_name).convert('RGB')
    orig = ConvertImage(img)
    training_set.append(orig.reshape((1, 512, 512, 3)))
    img = Image.open("gen/original/" + file_name).convert('RGB')
    whash = WhiteWash(img)
    mask_set.append(whash.reshape((1, 512, 512, 1)))


model = CreateUnet(512)
    
training = np.concatenate(training_set, axis=0)
masks = np.concatenate(mask_set, axis=0)


#model.load_weights("weights.best.hdf5")


filepath="weights.best.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

model.fit(training, masks, validation_split=0.3, batch_size=3, epochs=3, verbose=1, callbacks=callbacks_list)