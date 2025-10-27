import pyodbc


def connect():
    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=emTuXM;DATABASE=timekeeping;UID=sa;PWD=123;TrustServerCertificate=yes'
    try:
        conn = pyodbc.connect(connectionString)
        return conn
    except Exception as e:
        print(f"Lỗi kết nối đến cơ sở dữ liệu: {e}")
        return None
