import tensorflow as tf
import matplotlib.pyplot as plt

# Load and preprocess an example image
image_path = "copy.jpg"  # Thay đổi đường dẫn đến ảnh của bạn
image = tf.keras.preprocessing.image.load_img(image_path, target_size=(128, 128))
image_array = tf.keras.preprocessing.image.img_to_array(image)
image_array = tf.expand_dims(image_array, 0)  # Thêm chiều batch_size

# Build your model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), input_shape=(128, 128, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Dropout(0.15),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(4, activation='softmax'),
])

# Extract intermediate layers for visualization
layer_names = ['conv2d', 'max_pooling2d', 'dropout', 'conv2d_1', 'max_pooling2d_1', 'dropout_1', 'conv2d_2', 'max_pooling2d_2', 'dropout_2']
intermediate_layers = [model.get_layer(name).output for name in layer_names]

# Create a new model for feature extraction
feature_extraction_model = tf.keras.models.Model(inputs=model.input, outputs=intermediate_layers)

# Get the feature maps
feature_maps = feature_extraction_model.predict(image_array)

# Display the original image
plt.figure(figsize=(8, 8))
plt.subplot(1, len(intermediate_layers) + 1, 1)
plt.imshow(image_array[0] / 255.0)
plt.title('Original Image')

# Display the feature maps
for i, feature_map in enumerate(feature_maps):
    plt.subplot(1, len(intermediate_layers) + 1, i + 2)
    plt.imshow(feature_map[0, :, :, 0], cmap='viridis')  # Display the first channel of each feature map
    plt.title(layer_names[i])

plt.show()
