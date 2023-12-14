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

# Kiểm tra xem thư mục con đã tồn tại chưa, nếu chưa thì tạo mới
if not os.path.exists(subfolder_path):
    os.makedirs(subfolder_path)

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
        cv2.imwrite(os.path.join(subfolder_path, 'peo_{}.jpg'.format(sampleNum)), frame[y:y + h, x:x + w])
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        sampleNum += 1
        if sampleNum > 20:
            break
    if sampleNum > 20:
        break

cap.release()
cv2.destroyAllWindows()
