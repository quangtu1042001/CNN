from PyQt6 import QtGui, QtWidgets, QtCore, uic
from PyQt6.QtWidgets import *
import sys
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
import connect
import cv2


class Home_w(QMainWindow):
    def __init__(self, stacked_widget):
        super(Home_w, self).__init__()
        loadUi("test.ui", self)

        self.setFixedSize(850, 550)
        # Khi nút "Login" được nhấn, chuyển sang màn hình login
        self.login.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))

        self.btnAdd.clicked.connect(lambda :stacked_widget.setCurrentIndex(3))



class add_w(QMainWindow):
    def __init__(self, stacked_widget):
        super(add_w, self).__init__()
        loadUi("add.ui", self)
        self.stacked_widget = stacked_widget
        self.addEmp.clicked.connect(self.addEmployess)
        self.showCam.clicked.connect(self.show_cam)

    def show_cam(self):
        cam = True
        if cam:
            self.vid = cv2.VideoCapture(0)
        else:
            self.vid = cv2.VideoCapture('dothi.mp4')

        while True:
            ok, frame = self.vid.read()
            if not ok:
                break

            self.update(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.vid.release()

    def update(self, frame):
        self.setPhoto(frame)

    def setPhoto(self, image):
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.camAdd.setPixmap(pixmap)












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

    # def openCam(self):
    #     cap = cv2.VideoCapture(0)
    #     while True :
    #         OK ,self.frame = self.cap.read()
    #         self.update()
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break

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
    def __init__(self):
        super(Admin_w, self).__init__()
        loadUi("admin.ui", self)
        self.searchData.clicked.connect(self.search)

    def search(self):
        id = self.idSearch.text()
        name = self.nameSearch.text()
        db = connect.connect()
        query = db.cursor()

        sql_query = """
                SELECT
                    e.employee_id,
                    e.name,
                    e.department,
                    a.check_in_time,
                    a.check_out_time
                FROM
                    employees e
                LEFT JOIN
                    attendance a ON e.employee_id = a.employee_id
            """

        # Thêm điều kiện WHERE nếu id hoặc name được cung cấp
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

        if conditions:
            sql_query += " WHERE " + " OR ".join(conditions)

        query.execute(sql_query, tuple(params))
        rows = query.fetchall()
        table_widget = self.findChild(QTableWidget, 'tableData')

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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stacked_widget = QStackedWidget()
    add_f = add_w(stacked_widget)
    Login_f = Login_w(stacked_widget)
    Home_f = Home_w(stacked_widget)
    Admin_f = Admin_w()




    stacked_widget.addWidget(Home_f)
    stacked_widget.addWidget(Login_f)
    stacked_widget.addWidget(Admin_f)
    stacked_widget.addWidget(add_f)

    stacked_widget.setCurrentIndex(0)

    stacked_widget.show()
    app.exec()


