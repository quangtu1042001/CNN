from PyQt6 import QtGui,QtWidgets,QtCore,uic
from PyQt6.QtWidgets import *
import sys
from PyQt6.uic import loadUi
import connect





class Home_w(QMainWindow):
    def __init__(self, stacked_widget):
        super(Home_w, self).__init__()
        loadUi("test.ui", self)


        # Khi nút "Login" được nhấn, chuyển sang màn hình login
        self.login.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))


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
    Login_f = Login_w(stacked_widget)
    Home_f = Home_w(stacked_widget)
    Admin_f = Admin_w()


    stacked_widget.addWidget(Home_f)
    stacked_widget.addWidget(Login_f)
    stacked_widget.addWidget(Admin_f)

    stacked_widget.setCurrentIndex(0)


    stacked_widget.show()
    print("QStackedWidget đã được hiển thị")
    app.exec()


# def homeUI():
#     global ui
#     ui = home.Ui_MainWindow()
#     ui.setupUi(Home)
#     ui.login.clicked.connect(loginUI)
#     Home.show()
#
# def loginUI():
#     global ui
#     ui = login.Ui_Login()
#     ui.setupUi(Home)
#     ui.backMain.clicked.connect(homeUI)
#     Home.show()
#
#
# #run app
# homeUI()
# sys.exit(app.exec())

