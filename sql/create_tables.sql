CREATE DATABASE IF NOT EXISTS orderlytics;
USE orderlytics;

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Country VARCHAR(50)
);

CREATE TABLE Products (
    StockCode VARCHAR(20) PRIMARY KEY,
    Description VARCHAR(255),
    UnitPrice DECIMAL(10,2)
);

CREATE TABLE Sales (
    InvoiceNo VARCHAR(20),
    InvoiceDate DATETIME,
    StockCode VARCHAR(20),
    Quantity INT,
    CustomerID INT,
    FOREIGN KEY (StockCode) REFERENCES Products(StockCode),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
