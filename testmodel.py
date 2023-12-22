# import cv2
#
# # Sử dụng OpenCV để chụp ảnh từ webcam hoặc camera được kết nối
# cap = cv2.VideoCapture(0)
#
# while True:
#     ret, frame = cap.read()
#     cv2.imshow('Capture', frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         cv2.imwrite('captured_image.jpg', frame)
#         break
#
# cap.release()
# cv2.destroyAllWindows()


from keras.models import load_model
import cv2
import numpy as np

# Load mô hình đã huấn luyện
model = load_model('model-facereg.h5')

# Đọc ảnh được chụp
image = cv2.imread('captured_image.jpg')

# Resize ảnh về kích thước mong muốn (189, 189)
image = cv2.resize(image, (189, 189))

# Chuẩn hóa giá trị pixel về khoảng [0, 1]
image = image / 255.0

# Thêm một chiều để phản ánh batch size (1 ảnh)
image = np.expand_dims(image, axis=0)

# Dự đoán
predictions = model.predict(image)

# Chuyển đổi dự đoán thành nhãn
if predictions[0][0] > predictions[0][1]:
    label = 'tu'
else:
    label = 'soi'

print(f'Dự đoán: {label}')