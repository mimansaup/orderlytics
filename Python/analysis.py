import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='orderlytics'
)

query = """
SELECT DATE_FORMAT(InvoiceDate, '%Y-%m') AS Month,
       ROUND(SUM(Quantity * UnitPrice), 2) AS Revenue
FROM Sales s JOIN Products p USING(StockCode)
GROUP BY Month
ORDER BY Month;
"""
df = pd.read_sql(query, conn)
conn.close()

plt.figure(figsize=(10, 5))
plt.plot(df['Month'], df['Revenue'])
plt.xticks(rotation=60)
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig('../Dashboard/monthly_revenue.png')
plt.show()
