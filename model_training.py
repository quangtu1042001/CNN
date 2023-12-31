import os
import cv2
import numpy as np
from PIL import Image
from keras import layers, models
from sklearn.model_selection import train_test_split

TRAIN_DATA = 'dataset/data_train'
TRAIN_TEST = 'dataset/data_test'

x_train = []
y_train = []

label_dict = {'tu': [1, 0], 'soi': [0, 1]}

x_test = []
y_test = []


def load_data(directory, data_list):
    for category in os.listdir(directory):
        category_path = os.path.join(directory, category)
        for filename in os.listdir(category_path):
            file_path = os.path.join(category_path, filename)
            label = label_dict[category]
            img = cv2.resize(np.array(Image.open(file_path)), (189, 189))
            data_list.append((img, label))
    return data_list

x_train = load_data(TRAIN_DATA, x_train)
x_test = load_data(TRAIN_TEST, x_test)

# Shuffle the data
np.random.shuffle(x_train)

# Split the data into training and testing sets
# x_train, x_test = train_test_split(x_train, test_size=0.2, random_state=42)

# tach data va labels
x_train_images, x_train_labels = zip(*x_train)
x_test_images, x_test_labels = zip(*x_test)

# Convert NumPy array
x_train_images = np.array(x_train_images)
x_train_labels = np.array(x_train_labels)
x_test_images = np.array(x_test_images)
x_test_labels = np.array(x_test_labels)

# convert to 0 - 1
x_train_images = x_train_images / 255.0
x_test_images = x_test_images / 255.0

# Define the model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), input_shape=(189, 189, 3), activation='relu'),
    layers.MaxPool2D((2, 2)),
    layers.Dropout(0.15),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPool2D((2, 2)),
    layers.Dropout(0.2),

    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPool2D((2, 2)),
    layers.Dropout(0.2),

    layers.Flatten(),
    layers.Dense(1024, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(2, activation='softmax'),
])

# Compile model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()
# Train model
model.fit(x_train_images, x_train_labels, epochs=10, batch_size=64)

model.save('model-nonesang.h5')


# models = models.load_model('model-facereg.h5')