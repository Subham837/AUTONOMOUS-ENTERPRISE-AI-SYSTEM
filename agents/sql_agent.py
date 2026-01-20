import sqlite3

def sql_agent(state):
    """SQL agent for database queries and historical analysis."""
    try:
        conn = sqlite3.connect('sales.db')
        cursor = conn.cursor()
        
        # Get average sales from database
        cursor.execute('SELECT AVG(amount) FROM sales')
        result = cursor.fetchone()
        avg_sales = result[0] if result and result[0] else 0
        
        state["sql_avg_sales"] = avg_sales
        conn.close()
    except Exception as e:
        state["sql_avg_sales"] = 0
    
    return state
