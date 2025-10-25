-- Total Revenue
SELECT ROUND(SUM(s.Quantity * p.UnitPrice), 2) AS TotalRevenue
FROM Sales s JOIN Products p USING (StockCode);

-- Monthly Revenue Trend
SELECT DATE_FORMAT(InvoiceDate, '%Y-%m') AS Month,
       ROUND(SUM(Quantity * UnitPrice), 2) AS Revenue
FROM Sales s JOIN Products p USING(StockCode)
GROUP BY Month
ORDER BY Month;

-- Top 10 Revenue Customers
SELECT s.CustomerID,
       ROUND(SUM(s.Quantity * p.UnitPrice), 2) AS Revenue
FROM Sales s JOIN Products p USING (StockCode)
GROUP BY s.CustomerID
ORDER BY Revenue DESC
LIMIT 10;

-- Top 10 Best Selling Products
SELECT s.StockCode,
       p.Description,
       SUM(s.Quantity) AS UnitsSold,
       ROUND(SUM(s.Quantity * p.UnitPrice), 2) AS Revenue
FROM Sales s JOIN Products p USING(StockCode)
GROUP BY s.StockCode
ORDER BY Revenue DESC
LIMIT 10;
