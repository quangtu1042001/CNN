CREATE DATABASE timekeeping

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL
); 
CREATE TABLE attendance (
    id INT PRIMARY KEY IDENTITY(1,1),
    employee_id INT,
    check_in_time DATETIME,
    check_out_time DATETIME,
    attendance_date DATE
);
CREATE TABLE admin_accounts (
    admin_id INT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO employees (employee_id, name, department)
VALUES
    (1, 'John Doe', 'IT'),
    (2, 'Jane Smith', 'HR'),
    (3, 'Bob Johnson', 'Finance');


INSERT INTO attendance (employee_id, check_in_time, check_out_time, attendance_date)
VALUES
    (1, GETDATE(), GETDATE(), CONVERT(DATE, GETDATE())),
    (2, GETDATE(), GETDATE(), CONVERT(DATE, GETDATE())),
    (3, GETDATE(), GETDATE(), CONVERT(DATE, GETDATE()));

INSERT INTO admin_accounts(admin_id ,username,  password)
VALUES
    (1, 'admin', '123456')
    

