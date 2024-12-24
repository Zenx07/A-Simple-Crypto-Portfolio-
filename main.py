from db import add_to_portfolio, fetch_portfolio, get_purchase_price, update_current_price, update_profit_loss, clear_portfolio
from datetime import datetime
import requests
#API integration
def fetch_top_100_coins():
    url = "https://api.coinpaprika.com/v1/coins"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        top_100_coins = {coin['name'].lower(): coin['id'] for coin in data[:100]}
        return top_100_coins
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinPaprika API: {e}")
        return None

def get_crypto_price(crypto_name, top_100_coins):
    crypto_name = crypto_name.lower()
    if crypto_name in top_100_coins:
        crypto_id = top_100_coins[crypto_name]
    else:
        print(f"Sorry, we don't have data for {crypto_name}.")
        return None

    url = f"https://api.coinpaprika.com/v1/tickers/{crypto_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = data['quotes']['USD']['price']
        return price
    except KeyError:
        print(f"Sorry, we couldn't find any data for {crypto_name}.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinPaprika API: {e}")
        return None

def calculate_total_value(units, current_price):
    return units * current_price

def calculate_profit_loss(purchase_price, current_price, units_owned):
    return (float(current_price) - float(purchase_price)) * units_owned

def user_menu():
    top_100_coins = fetch_top_100_coins()
    if top_100_coins is None:
        return

    while True:
        print("\n1. Buy crypto")
        print("2. Sell crypto")
        print("3. View portfolio")
        print("4. Clear database")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            coin_name = input("Enter coin name (e.g., Bitcoin): ").lower()
            current_price = get_crypto_price(coin_name, top_100_coins)
            if current_price is None:
                print(f"Error: Could not fetch the price for {coin_name}. Please try again.")
                continue

            units_owned = float(input("Enter units to buy: "))
            purchase_price = current_price  
            total_value = calculate_total_value(units_owned, current_price)
            transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            add_to_portfolio(coin_name, units_owned, purchase_price, current_price, total_value, 'buy', transaction_date)
            print(f"Added {units_owned} units of {coin_name} to your portfolio at {purchase_price:.2f} USD per unit.")

        elif choice == '2': 
            coin_name = input("Enter coin name (e.g., Bitcoin): ").lower()
            current_price = get_crypto_price(coin_name, top_100_coins)
            if current_price is None:
                print(f"Error: Could not fetch the price for {coin_name}. Please try again.")
                continue

            units_owned = float(input("Enter units to sell: "))
            purchase_price = get_purchase_price(coin_name)
            if purchase_price is None:
                print(f"Error: No purchase record found for {coin_name}.")
                continue

            profit_loss = calculate_profit_loss(purchase_price, current_price, units_owned)
            total_value = calculate_total_value(units_owned, current_price)
            transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            add_to_portfolio(coin_name, units_owned, purchase_price, current_price, total_value, 'sell', transaction_date)
            update_profit_loss(coin_name, profit_loss)
            print(f"Sold {units_owned} units of {coin_name}. Profit/Loss: {profit_loss:.2f} USD.")

        elif choice == '3': 
            portfolio = fetch_portfolio()
            print("\n--- Your Portfolio ---")
            for entry in portfolio:
                print(f"Coin: {entry[1]}, Units Owned: {entry[2]}, Purchase Price: {entry[3]:.2f} USD, "
                      f"Current Price: {entry[4]:.2f} USD, Total Value: {entry[5]:.2f} USD, "
                      f"Transaction: {entry[6]}, Date: {entry[7]}")

        elif choice == '4':  
            clear_portfolio()

        elif choice == '5':  
            print("Exiting the portfolio manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    user_menu()
