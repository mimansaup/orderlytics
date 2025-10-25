import pandas as pd
import mysql.connector

# Load dataset
df = pd.read_csv('../Data/OnlineRetail.csv', encoding='ISO-8859-1')

# Data Cleaning
df = df.dropna(subset=['CustomerID'])
df = df[df['InvoiceNo'].str.startswith('C') == False]
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]
df = df[df['Country'] == 'United Kingdom']

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Database Connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='orderlytics'
)
cursor = conn.cursor()

# Insert Products (deduped)
products = df[['StockCode','Description','UnitPrice']].drop_duplicates()
for _, row in products.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Products (StockCode, Description, UnitPrice)
        VALUES (%s, %s, %s);
    """, tuple(row))

# Insert Customers (deduped)
customers = df[['CustomerID','Country']].drop_duplicates()
for _, row in customers.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Customers (CustomerID, Country)
        VALUES (%s, %s);
    """, tuple(row))

# Insert Sales
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO Sales (InvoiceNo, InvoiceDate, StockCode, Quantity, CustomerID)
        VALUES (%s, %s, %s, %s, %s)
    """, tuple(row[['InvoiceNo','InvoiceDate','StockCode','Quantity','CustomerID']]))

conn.commit()
cursor.close()
conn.close()

print("✅ Data cleaned and loaded successfully!")
