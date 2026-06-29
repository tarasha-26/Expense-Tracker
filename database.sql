CREATE DATABASE expense_tracker;

USE expense_tracker;

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255),
    category VARCHAR(100),
    expense_date DATE,
    amount DECIMAL(10,2)
);