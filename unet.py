from keras.models import Model
from keras.layers import Input, Conv2D, Dropout, MaxPooling2D, concatenate, UpSampling2D
from keras.optimizers import Adam

def CreateUnetStep(input_layer, size, useDropout = False):
    conv = Conv2D(size, 3, activation='relu', padding = 'same', kernel_initializer = 'he_normal')(input_layer)
    conv = Conv2D(size, 3, activation='relu', padding = 'same', kernel_initializer = 'he_normal')(conv)
    drop = None
    if useDropout:
        conv = Dropout(0.5)(conv)
    return conv

def CreateUnet(input_size, color_channels = 3):
    input = None
    if color_channels > 1:
        input = Input((input_size, input_size, color_channels))
    else:
        input = Input((input_size, input_size))
    
    convs = []
    pools = []
    input_layer = input
    for i in range(4): #64, 128, 256, 512
        convs.append(CreateUnetStep(input_layer, pow(2, 6 + i), True if i == 3 else False))
        pools.append(MaxPooling2D(pool_size=(2, 2))(convs[-1]))
        input_layer = pools[-1]
    
    generated = CreateUnetStep(pools[-1], 1024, True)
    convs.append(generated)

    input_layer = convs[-1]
    for i in range(3, -1, -1):
        up = Conv2D(pow(2, 6 + i), 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(input_layer))
        merge = concatenate([convs[i], up], axis=3)
        convs.append(CreateUnetStep(merge, pow(2, 6 + i), False))
        input_layer = convs[-1]

    final_conv = Conv2D(2, 3,  activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(convs[-1])
    final_conv = Conv2D(1, 1, activation='sigmoid')(final_conv)

    model = Model(input=input, output=final_conv)
    model.compile(optimizer=Adam(learning_rate=1e-4), loss='binary_crossentropy', metrics = ['accuracy'])
    model.summary()