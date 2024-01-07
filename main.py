from PyQt6 import QtGui, QtWidgets, QtCore, uic
from PyQt6.QtWidgets import *
import sys
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QThread, pyqtSignal,QDate
from PyQt6.QtGui import QImage, QPixmap
import pandas as pd
import numpy as np
import connect
import cv2
import os
import face_recognition
from keras import models
from datetime import datetime


conn = connect.connect()
class Home_w(QMainWindow):
    def __init__(self, stacked_widget):
        super(Home_w, self).__init__()
        loadUi("test.ui", self)



        self.setFixedSize(850, 550)
        # Khi nút "Login" được nhấn, chuyển sang màn hình login
        self.login.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
        self.btnAdd.clicked.connect(lambda :stacked_widget.setCurrentIndex(3))
        self.atten_dance.clicked.connect(self.atten)

    def atten(self):
        conn = connect.connect()
        folder_path = 'img'
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
        model = models.load_model('testanti.h5')
        known_face_encodings = []
        known_face_names = []

        def load_faces():
            nonlocal known_face_encodings, known_face_names
            known_face_encodings = []
            known_face_names = []

            cur = conn.cursor()
            cur.execute("SELECT * FROM employees")
            users = cur.fetchall()

            if(len(users) == 0):
                return

            for x in users:
                image = face_recognition.load_image_file(folder_path + "/" + str(x[0]) + '.jpg')
                face_encoding = face_recognition.face_encodings(image)
                if(len(face_encoding) > 0):
                    known_face_encodings.append(face_encoding[0])
                    known_face_names.append(x[1])

        load_faces()

        cap = cv2.VideoCapture(0)
        name_res = 'Unknown'
        while True:
            ret, frame = cap.read()
            if not ret:
                # Đọc frame không thành công, thoát khỏi vòng lặp
                break
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                if w > 0 and h > 0:
                    croped = frame[y:y + h, x:x + w]
                    croped = cv2.resize(croped, (128, 128))
                    croped = np.expand_dims(croped, axis=0) / 255.0
                    classes = model.predict(croped, verbose=0)
                    face_accuracy = classes[0][2]

                    # Lưu ý: Bạn có thể thêm các điều kiện kiểm tra tại đây để xác định
                    # xem người này có phải là người đã đăng ký không.

                    if face_accuracy > 0.85:
                        employee_id = self.get_employee_id_by_name(name_res)

                        if employee_id is not None:
                            attendance_record = self.get_attendance_record(employee_id)
                            current_time = datetime.now()
                            # print(attendance_record)
                            if attendance_record is None or attendance_record[3] > current_time:
                                # Điểm danh lần đầu hoặc đã điểm danh nhưng chưa checkout
                                self.check_in(employee_id)
                            else:
                                # Đã điểm danh và đã checkout, thêm mới
                                self.check_in_and_out(employee_id)





                            # Hiển thị thông báo khi thêm thành công
                            QMessageBox.information(self, 'Thông báo',
                                                    f'Thêm thành công cho nhân viên có ID {employee_id}')
                            # Dừng camera
                            cap.release()
                            cv2.destroyAllWindows()



                    if np.argmax(classes) != 2:
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

                            name_res = name
                            for (top, right, bottom, left), name in zip(face_locations, face_names):
                                name_res = name
                                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), thickness=2)
                                cv2.putText(frame, name_res, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                            (0, 0, 255), 2)


                    cv2.putText(frame, f'Accuracy: {face_accuracy:.2%}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow('Face Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def get_employee_id_by_name(self, employee_name):
        cur = conn.cursor()
        cur.execute("SELECT employee_id FROM employees WHERE name = ?", (employee_name,))
        result = cur.fetchone()
        if result:
            return result[0]
        return None
    def get_attendance_record(self, employee_id):

        cur = conn.cursor()
        cur.execute("SELECT TOP 1 * FROM attendance WHERE employee_id = ? ORDER BY attendance_date DESC",
                    (employee_id,))
        return cur.fetchone()

    def check_in(self, employee_id):
        cur = conn.cursor()
        cur.execute("INSERT INTO attendance (employee_id, check_in_time, attendance_date) VALUES (?, ?, ?)",
                    (employee_id, datetime.now(), datetime.now().date()))
        conn.commit()

    def check_in_and_out(self, employee_id):
        cur = conn.cursor()

        # Kiểm tra xem đã có bản ghi cho ngày hiện tại chưa
        cur.execute("SELECT * FROM attendance WHERE employee_id = ? AND attendance_date = ?",
                    (employee_id, datetime.now().date()))
        existing_record = cur.fetchone()
        print(existing_record)

        if existing_record:
            # Đã có bản ghi cho ngày hiện tại, so sánh và cập nhật check_out_time nếu cần
            if existing_record[3] is None or existing_record[3] < datetime.now():
                # Thực hiện cập nhật
                cur.execute("UPDATE attendance SET check_out_time = ? WHERE employee_id = ? AND attendance_date = ?",
                            (datetime.now(), employee_id, datetime.now().date()))
                conn.commit()
                QMessageBox.information(self, 'Thông báo', f'Đã cập nhật check_out cho nhân viên có ID {employee_id}')
            else:
                QMessageBox.warning(self, 'Cảnh báo', f'Nhân viên có ID {employee_id} đã check_out trong ngày.')
        else:
            # Chưa có bản ghi cho ngày hiện tại, thêm mới
            cur.execute("INSERT INTO attendance (employee_id, check_in_time, attendance_date) VALUES (?, ?, ?)",
                        (employee_id, datetime.now(), datetime.now().date()))
            conn.commit()
            QMessageBox.information(self, 'Thông báo', f'Đã thêm mới check_in cho nhân viên có ID {employee_id}')

        cur.close()


class add_w(QMainWindow):
    def __init__(self, stacked_widget):
        super(add_w, self).__init__()
        loadUi("add.ui", self)
        self.stacked_widget = stacked_widget
        self.addEmp.clicked.connect(self.addEmployess)
        self.showCam.clicked.connect(self.show_cam)
        self.closeCam.clicked.connect(self.exit_cam)
        self.backTime.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        self.Screenshot.clicked.connect(self.capture_screenshot)

    def show_cam(self):
        cam = True
        if cam:
            self.vid = cv2.VideoCapture(0)
        else:
            self.vid = cv2.VideoCapture('dothi.mp4')

        self.is_cam_running = True

        while self.is_cam_running:
            ok, frame = self.vid.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if not ok:
                break

            self.update(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_cam()  # Dừng camera khi nhấn 'q'

        self.vid.release()

    def update(self, frame):
        self.setPhoto(frame)

    def setPhoto(self, image):
        image = cv2.resize(image, (531,481))
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.camAdd.setPixmap(pixmap)

    def exit_cam(self):
        self.is_cam_running = False

    def capture_screenshot(self):
        idEmp = self.addId.text()

        # Kiểm tra xem idEmp có giá trị hay không
        if idEmp:
            img_folder = 'img'
            os.makedirs(img_folder, exist_ok=True)  # Tạo thư mục 'img' nếu chưa tồn tại
            screenshot_name = f"{img_folder}/{idEmp}.jpg"
            frame = self.vid.read()[1]
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite(screenshot_name, frame)
            QMessageBox.information(self, 'Thông báo', f'Đã chụp ảnh với ID {idEmp} và lưu vào thư mục {img_folder}')
        else:
            QMessageBox.warning(self, 'Cảnh báo', 'Vui lòng nhập ID trước khi chụp ảnh.')



    def addEmployess(self):
        name = self.addName.text()
        depart = self.addDepart.text()
        idEmp = self.addId.text()
        db = connect.connect()
        if name and depart and idEmp:
            query = db.cursor()
            query.execute("INSERT INTO employees (employee_id, department, name) VALUES (?, ?, ?)", (idEmp, depart, name))
            db.commit()

            self.addName.clear()
            self.addDepart.clear()
            self.addId.clear()
            QMessageBox.information(self, 'Success', 'Thêm nhân viên thành công!')
        else:
            QMessageBox.warning(self, 'Warning', 'Vui lòng nhập đầy đủ thông tin')



class Login_w(QMainWindow):
    def __init__(self, stacked_widget):
        super(Login_w, self).__init__()
        loadUi("login.ui", self)
        self.stacked_widget = stacked_widget
        self.btn_login.clicked.connect(self.login)
        self.backMain.clicked.connect(self.go_to_home)

    def go_to_home(self):
        # Chuyển sang trang Home khi nhấn nút backmain
        self.stacked_widget.setCurrentIndex(0)  # 0 là index của trang Home trong stacked_widget

    def login(self):
        un = self.user.text()
        pw = self.password.text()

        # Kết nối đến cơ sở dữ liệu
        db = connect.connect()

        if db:
            # Thực hiện truy vấn kiểm tra username và password
            query = db.cursor()
            query.execute("SELECT * FROM admin_accounts WHERE username = ? AND password = ?", (un, pw))

            # Lấy dòng đầu tiên từ kết quả truy vấn
            result = query.fetchone()

            # Kiểm tra kết quả
            if result:
                QMessageBox.information(self, "Thành công", "Đăng nhập thành công")
                # Chuyển sang trang Admin khi đăng nhập thành công
                self.stacked_widget.setCurrentIndex(2)  # (2 là index của trang Admin trong stacked_widget)
            else:
                QMessageBox.warning(self, "Lỗi", "Tài khoản hoặc mật khẩu không đúng")
        else:
            QMessageBox.warning(self, "Lỗi", "Không thể kết nối đến cơ sở dữ liệu")


class Admin_w(QMainWindow):
    def __init__(self,stacked_widget):
        super(Admin_w, self).__init__()
        loadUi("admin.ui", self)
        self.stacked_widget = stacked_widget
        self.searchData.clicked.connect(self.search)
        self.caleSearch.selectionChanged.connect(self.search)  # Connect dateChanged signal to search function
        self.backAdmin.clicked.connect(self.back_admin)
        self.EpExcel.clicked.connect(self.exportToExcel)



    def back_admin(self):
        # Chuyển sang trang Home khi nhấn nút backmain
        self.stacked_widget.setCurrentIndex(0)  # 0 là index của trang Home trong stacked_widget

    def search(self):
        id = self.idSearch.text()
        name = self.nameSearch.text()
        selected_date = self.caleSearch.selectedDate()

        db = connect.connect()
        query = db.cursor()

        sql_query = """
                SELECT
                    e.employee_id,
                    e.name,
                    e.department,
                    a.check_in_time,
                    a.check_out_time,
                    a.attendance_date
                FROM
                    employees e
                LEFT JOIN
                    attendance a ON e.employee_id = a.employee_id
                """

        # Thêm điều kiện WHERE nếu id, name hoặc date được cung cấp
        conditions = []
        params = []

        if id and name:
            conditions.append("(e.employee_id = ? OR e.name = ?)")
            params.extend([id, name])
        elif id:
            conditions.append("e.employee_id = ?")
            params.append(id)
        elif name:
            conditions.append("e.name = ?")
            params.append(name)

        if selected_date.isValid():  # Kiểm tra xem ngày đã chọn từ QCalendarWidget có hợp lệ hay không
            conditions.append("a.attendance_date = ?")
            params.append(selected_date.toString("yyyy-MM-dd"))

        if conditions:
            sql_query += " WHERE " + " AND ".join(conditions)

        query.execute(sql_query, tuple(params))
        rows = query.fetchall()
        table_widget = self.findChild(QTableWidget, 'tableData')

        if rows:
            # Đặt dữ liệu vào QTableWidget
            table_widget.setRowCount(len(rows))
            table_widget.setColumnCount(len(rows[0]))

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    table_widget.setItem(i, j, item)

            # Đặt tiêu đề cột
            column_headers = [column[0] for column in query.description]
            table_widget.setHorizontalHeaderLabels(column_headers)


        else:
            # Nếu không có dữ liệu, xóa dữ liệu cũ trong QTableWidget
            table_widget.clearContents()
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)

    def exportToExcel(self):
        table_widget = self.findChild(QTableWidget, 'tableData')

        if not table_widget.rowCount() or not table_widget.columnCount():
            return  # Không có dữ liệu hoặc không có cột

        # Lấy dữ liệu từ QTableWidget
        data = []
        for row in range(table_widget.rowCount()):
            row_data = []
            for column in range(table_widget.columnCount()):
                item = table_widget.item(row, column)
                row_data.append(item.text())
            data.append(row_data)

        # Tạo DataFrame từ dữ liệu
        df = pd.DataFrame(data)

        # Chọn vị trí lưu tệp Excel
        excel_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Excel file", "", "Excel Files (*.xlsx)")

        if excel_path:
            # Xuất DataFrame vào tệp Excel
            df.to_excel(excel_path, index=False)

            # Thông báo thành công
            success_message = f"Data exported to {excel_path}"
            print(success_message)

            # Thông báo trên giao diện người dùng
            # QMessageBox.information(self, "Export Successful", success_message, QMessageBox.ButtonRole.AcceptRole)
            QMessageBox.information(self, 'Success', 'Xuất Excel thành công!')
                        


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stacked_widget = QStackedWidget()
    add_f = add_w(stacked_widget)
    Login_f = Login_w(stacked_widget)
    Home_f = Home_w(stacked_widget)
    Admin_f = Admin_w(stacked_widget)




    stacked_widget.addWidget(Home_f)
    stacked_widget.addWidget(Login_f)
    stacked_widget.addWidget(Admin_f)
    stacked_widget.addWidget(add_f)

    stacked_widget.setCurrentIndex(0)

    stacked_widget.show()
    app.exec()


