# import cv2
#
# video = cv2.VideoCapture(0)  # đổi theo index bạn tìm được
#
# if not video.isOpened():
#     print("Không thể mở camera!")
#     exit()
#
# while True:
#     ret, frame = video.read()
#     if not ret:
#         break
#     cv2.imshow("DroidCam", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# video.release()
# cv2.destroyAllWindows()
import pyodbc
print(pyodbc.drivers())
