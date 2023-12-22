import cv2
import os

# Tên thư mục chính
dataset_folder = 'dataset'

# Kiểm tra xem thư mục chính đã tồn tại chưa, nếu chưa thì tạo mới
if not os.path.exists(dataset_folder):
    os.makedirs(dataset_folder)

# Lấy tên thư mục con từ người dùng
subfolder_name = input("Nhập tên thư mục con để lưu ảnh: ")

# Tạo đường dẫn đầy đủ cho thư mục con
subfolder_path = os.path.join(dataset_folder, subfolder_name)

# Lấy đường dẫn đến thư mục data_train
data_train_path = os.path.join(dataset_folder, 'data_train')

# Tạo thư mục con trong data_train
os.makedirs(os.path.join(data_train_path, subfolder_name))

# Lấy đường dẫn đến thư mục data_test
data_test_path = os.path.join(dataset_folder, 'data_test')

# Tạo thư mục con trong data_test
os.makedirs(os.path.join(data_test_path, subfolder_name))

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')
cap = cv2.VideoCapture(0)
sampleNum = 0

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Lưu khuôn mặt đã phát hiện vào thư mục con
        if sampleNum <= 300:
            # Lưu ảnh vào data_test/tu123
            cv2.imwrite(os.path.join(data_test_path, subfolder_name, 'peo_{}.jpg'.format(sampleNum)),
                        frame[y:y + h, x:x + w])
        else:
            # Lưu ảnh vào data_train/tu123
            cv2.imwrite(os.path.join(data_train_path, subfolder_name, 'peo_{}.jpg'.format(sampleNum)),
                        frame[y:y + h, x:x + w])
        sampleNum += 1
        if sampleNum > 1000:
            break
    if sampleNum > 1000:
        break

cap.release()
cv2.destroyAllWindows()
