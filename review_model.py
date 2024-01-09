import os
import numpy as np
from pycocotools.coco import COCO
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input

# Đường dẫn đến file annotation COCO
annotation_file_path = 'datatest\_annotations.coco.json'

# Tạo đối tượng COCO
coco = COCO(annotation_file_path)

# Lấy danh sách các ảnh trong tập dữ liệu kiểm thử
image_ids = coco.getImgIds()

# Load mô hình đã được huấn luyện từ tệp h5
model = load_model('testanti.h5')

# Đường dẫn đến thư mục chứa ảnh trong tập kiểm thử
images_folder = 'D:/LamViec/tai-lieu-hoc-may/DO-AN/CNN/datatest/'

# Dự đoán nhãn cho từng ảnh trong tập kiểm thử
predictions = []
true_labels = []
class_names = ['face', 'device', 'live', 'mask', 'photo']
# Dự đoán nhãn cho từng ảnh trong tập kiểm thử
for img_id in image_ids:
    img_data = coco.loadImgs(img_id)[0]
    img_path = os.path.join(images_folder, img_data['file_name'])
    img = image.load_img(img_path, target_size=(128, 128))  # Điều chỉnh kích thước ảnh đầu vào
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)[0]
    predicted_label_id = np.argmax(prediction)

    # Lấy nhãn thực tế từ annotation
    ann_ids = coco.getAnnIds(imgIds=img_id)
    img_anns = coco.loadAnns(ann_ids)
    true_label_id = img_anns[0]['category_id']  # Giả sử mỗi ảnh chỉ có một đối tượng

    # Lấy tên nhãn từ category_id (nếu tồn tại)
    true_label_name = coco.loadCats(true_label_id)[0]['name']

    # Lấy tên nhãn dự đoán từ tên class của mô hình
    predicted_label_name = class_names[predicted_label_id] if predicted_label_id < len(class_names) else str(
        predicted_label_id)

    # Hiển thị ảnh với nhãn dự đoán và nhãn thực tế
    plt.figure(figsize=(6, 6))
    plt.imshow(img)
    plt.title(f"True Label: {true_label_name}, Predicted Label: {predicted_label_name}")
    plt.axis("off")
    plt.show()

