import cv2
# from model import getModel
import numpy as np
# import mysql.connector
import face_recognition
from model import getModel
import connect

conn = connect.connect()
folder_path = 'img'
# Class names: ['face', 'mask', 'phone', 'photo']
face_cascade = cv2.CascadeClassifier("haarcascades/" + 'haarcascade_frontalface_alt.xml')
model = getModel('vgg19_new_dataset_adam_antiSpoofing.h5')

known_face_encodings = []
known_face_names = []

def load_faces():
    global known_face_encodings, known_face_names
    known_face_encodings = []
    known_face_names = []

    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    users = cur.fetchall()

    if(len(users) == 0):
        return

    for x in users:
        # print(x)
        image = face_recognition.load_image_file(folder_path + "/" + str(x[0]) + '.jpg')
        face_encoding = face_recognition.face_encodings(image)
        if(len(face_encoding) > 0):
            # Create arrays of known face encodings and their names
            known_face_encodings.append(face_encoding[0])
            known_face_names.append(x[1])
        # break

# Khởi tạo webcam
cap = cv2.VideoCapture(0)

load_faces()
while True:
    ret, frame = cap.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        if w > 0 and h > 0:
            # croped = frame[y:y + h, x:x + w]
            # croped = cv2.resize(croped, (128, 128))
            # Chuyển đổi ảnh sang định dạng phù hợp cho model.predict
            predFrame = np.expand_dims(cv2.cvtColor(cv2.resize(frame, (128,128)), cv2.COLOR_BGR2RGB), axis=0) / 255
            classes = model.predict(predFrame, verbose=0)

        # fake face
        if np.argmax(classes) != 0:
            name = "Invalid"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, name, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        else:
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                # Compare a list of face encodings against a candidate encoding to see if they match.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)

                name_res = 'Unknown'
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    name_res = name
                    cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 0), thickness=2)
                    cv2.putText(frame, name_res, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng bộ nhớ và đóng webcam khi kết thúc
cap.release()
cv2.destroyAllWindows()