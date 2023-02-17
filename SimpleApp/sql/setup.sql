CREATE DATABASE sanic_app;
GO

USE sanic_app;
GO

CREATE TABLE Employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(30) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(50)
);
GO

INSERT INTO Employees (username, password, email)
VALUES ('PhamHongPhuc', '123456789', 'php@gmail.com'),
        ('PhamHongPhuc1', '123456789', 'php1@gmail.com'),
        ('PhamHongPhuc2', '123456789', 'php2@gmail.com'),
        ('PhamHongPhuc3', '123456789', 'php3@gmail.com'),
        ('PhamHongPhuc4', '123456789', 'php4@gmail.com'),
        ('PhamHongPhuc5', '123456789', 'php5@gmail.com'),
        ('PhamHongPhuc6', '123456789', 'php6@gmail.com'),
        ('PhamHongPhuc7', '123456789', 'php7@gmail.com'),
        ('PhamHongPhuc8', '123456789', 'php8@gmail.com'),
        ('PhamHongPhuc9', '123456789', 'php9@gmail.com'),
        ('PhamHongPhuc10', '123456789', 'php10@gmail.com');
GO

CREATE TABLE Productions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    amount INT NOT NULL,
    employeeId INT,
    FOREIGN KEY (employeeId) REFERENCES Employees(id)
);
GO

INSERT INTO Productions (name, amount, employeeId)
VALUES ('production1', 100, 1),
        ('production2', 200, 2),
        ('production3', 1000, 3);
