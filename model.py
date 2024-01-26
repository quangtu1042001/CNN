from keras.models import Model
from keras.layers import Flatten, Dense, Input
from keras.applications import VGG16, VGG19
from keras import optimizers
def getModel(path):
  model_vgg19_conv = VGG19(weights='imagenet', include_top=False)
  model_vgg19_conv.summary()

  input = Input(shape=(128,128,3),name = 'image_input')

  for layer in model_vgg19_conv.layers:
      layer.trainable = False

  #Use the generated model
  output_vgg19_conv = model_vgg19_conv(input)

  #Add the fully-connected layers
  x = Flatten(name='flatten')(output_vgg19_conv)
  x = Dense(4096, activation='relu', name='fc1')(x)
  x = Dense(4096, activation='relu', name='fc2')(x)
  x = Dense(4, activation='softmax', name='predictions')(x)

  model = Model(inputs=input, outputs=x)
  model.compile(optimizer=optimizers.Nadam(learning_rate=1e-4), loss='binary_crossentropy',metrics='accuracy')

  if path:
     print('load check point: ' + path)
     model.load_weights(path)

  return model