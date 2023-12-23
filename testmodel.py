import cv2
import numpy as np
from PIL import Image
from keras import layers, models

# Load the trained model
model = models.load_model('model-nonesang.h5')

# Preprocess the test image
test_image_path = 'soi.jpg'  # Replace with the actual path to your test image
test_image = cv2.resize(np.array(Image.open(test_image_path)), (189, 189))
test_image = test_image / 255.0

# Reshape the test image to match the input shape of the model
test_image = np.reshape(test_image, (1, 189, 189, 3))

# Make predictions
predictions = model.predict(test_image)

# Set a threshold for confidence
confidence_threshold = 0.7  # Adjust this threshold as needed

# Check if the highest predicted probability is below the confidence threshold
if np.max(predictions) < confidence_threshold:
    print("Mô hình không tự tin về dự đoán của mình.")
else:
    # Assuming 'tu' corresponds to index 0 and 'soi' corresponds to index 1
    predicted_class_index = np.argmax(predictions)
    predicted_class = 'tu' if predicted_class_index == 0 else 'soi'
    print(f"The model predicts: {predicted_class}")
