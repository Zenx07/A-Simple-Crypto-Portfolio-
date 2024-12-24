import mysql.connector
from datetime import datetime

def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="crypto_portfolio_db"
    )
    return connection

def add_to_portfolio(coin_name, units_owned, purchase_price, current_price, total_value, transaction_type, transaction_date):
    connection = connect_to_db()
    cursor = connection.cursor()
    
    # Calculate profit/loss
    profit_loss = (float(current_price) - float(purchase_price)) * units_owned

    query = """
        INSERT INTO portfolio (coin_name, units_owned, purchase_price, current_price, total_value, transaction_type, transaction_date, profit_loss)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (coin_name, units_owned, purchase_price, current_price, total_value, transaction_type, transaction_date, profit_loss)
    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


def fetch_portfolio():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM portfolio")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def get_purchase_price(coin_name):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT purchase_price FROM portfolio WHERE coin_name = %s ORDER BY transaction_date DESC LIMIT 1"
    cursor.execute(query, (coin_name,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result:
        return float(result[0]) 
    else:
        return None


def update_current_price(coin_name, current_price):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "UPDATE portfolio SET current_price = %s WHERE coin_name = %s"
    cursor.execute(query, (current_price, coin_name))
    connection.commit()
    cursor.close()
    connection.close()

def update_profit_loss(coin_name, profit_loss):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "UPDATE portfolio SET profit_loss = %s WHERE coin_name = %s ORDER BY transaction_date DESC LIMIT 1"
    cursor.execute(query, (profit_loss, coin_name))
    connection.commit()
    cursor.close()
    connection.close()

def clear_portfolio():
    connection = connect_to_db()
    cursor = connection.cursor()
    
    cursor.execute("TRUNCATE TABLE portfolio")
    cursor.execute("ALTER TABLE portfolio AUTO_INCREMENT = 1")
    
    connection.commit()
    cursor.close()
    connection.close()
    print("All records in the portfolio have been cleared, and the ID counter has been reset.")
