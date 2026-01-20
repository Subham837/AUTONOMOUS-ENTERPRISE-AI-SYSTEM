#!/usr/bin/env python3
"""Initialize database with sample sales data for SQL agent."""

import sqlite3
from datetime import datetime, timedelta
import random

def init_database():
    """Create database and populate with sample data."""
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    
    # Create sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL,
            product TEXT,
            region TEXT,
            salesperson TEXT
        )
    ''')
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            industry TEXT,
            lifetime_value REAL,
            created_date TEXT
        )
    ''')
    
    # Clear existing data
    cursor.execute('DELETE FROM sales')
    cursor.execute('DELETE FROM customers')
    
    # Insert sample sales data
    products = ['Product A', 'Product B', 'Product C', 'Product D']
    regions = ['North', 'South', 'East', 'West']
    salespersons = ['John Smith', 'Jane Doe', 'Bob Johnson', 'Alice Brown']
    
    base_date = datetime.now() - timedelta(days=365)
    
    for i in range(365):
        current_date = base_date + timedelta(days=i)
        # Generate 2-5 sales per day
        for _ in range(random.randint(2, 5)):
            amount = random.uniform(5000, 50000)
            product = random.choice(products)
            region = random.choice(regions)
            salesperson = random.choice(salespersons)
            
            cursor.execute('''
                INSERT INTO sales (date, amount, product, region, salesperson)
                VALUES (?, ?, ?, ?, ?)
            ''', (current_date.strftime('%Y-%m-%d'), amount, product, region, salesperson))
    
    # Insert sample customer data
    industries = ['Technology', 'Finance', 'Healthcare', 'Retail', 'Manufacturing']
    
    customers = [
        ('Acme Corp', 'contact@acme.com', 'Technology', 500000),
        ('Global Industries', 'sales@global.com', 'Manufacturing', 750000),
        ('Finance Plus', 'info@financeplus.com', 'Finance', 600000),
        ('Health Solutions', 'hello@healthsol.com', 'Healthcare', 450000),
        ('Retail Mega', 'support@retailmega.com', 'Retail', 550000),
        ('Tech Innovators', 'contact@techinnovators.com', 'Technology', 700000),
        ('Smart Finance', 'info@smartfinance.com', 'Finance', 650000),
    ]
    
    for name, email, industry, ltv in customers:
        cursor.execute('''
            INSERT INTO customers (name, email, industry, lifetime_value, created_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, industry, ltv, base_date.strftime('%Y-%m-%d')))
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully with sample data")

if __name__ == '__main__':
    init_database()
