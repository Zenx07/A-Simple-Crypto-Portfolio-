from db import add_to_portfolio, fetch_portfolio, clear_portfolio, get_purchase_price
from main import fetch_top_100_coins, get_crypto_price
from tkinter import messagebox
from datetime import datetime
import tkinter as tk
from tkinter import ttk


def buy_crypto_gui(top_100_coins):
    def on_buy():
        coin_name = coin_name_entry.get().lower()
        units = units_entry.get()
        
        if not coin_name or not units:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            units = float(units)
            current_price = get_crypto_price(coin_name, top_100_coins)
            if current_price is None:
                raise ValueError("Price not available.")
            
            transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_value = units * current_price
            add_to_portfolio(coin_name, units, current_price, current_price, total_value, 'buy', transaction_date)
            
            messagebox.showinfo("Success", f"Bought {units} units of {coin_name.title()} at ${current_price:.2f}/unit.")
            buy_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    buy_window = tk.Toplevel(root)
    buy_window.title("Buy Crypto")
    buy_window.geometry("300x200")
    buy_window.configure(bg="#fff7ee")

    tk.Label(buy_window, text="Coin Name:", font=("Courier New", 12), bg="#fff7ee").pack(pady=5)
    coin_name_entry = tk.Entry(buy_window, font=("Courier New", 12))
    coin_name_entry.pack(pady=5)

    tk.Label(buy_window, text="Units:", font=("Courier New", 12), bg="#fff7ee").pack(pady=5)
    units_entry = tk.Entry(buy_window, font=("Courier New", 12))
    units_entry.pack(pady=5)

    tk.Button(buy_window, text="Buy", font=("Courier New", 12), command=on_buy, bg="#4CAF50", fg="white").pack(pady=15)

def sell_crypto_gui(top_100_coins):
    def on_sell():
        coin_name = coin_name_entry.get().lower()
        units = units_entry.get()
        
        if not coin_name or not units:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            units = float(units)
            current_price = get_crypto_price(coin_name, top_100_coins)
            if current_price is None:
                raise ValueError("Price not available.")

            purchase_price = get_purchase_price(coin_name)
            if purchase_price is None:
                raise ValueError("No purchase record found for this coin.")

            transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            profit_loss = (current_price - purchase_price) * units
            total_value = units * current_price

            add_to_portfolio(coin_name, units, purchase_price, current_price, total_value, 'sell', transaction_date)
            messagebox.showinfo("Success", f"Sold {units} units of {coin_name.title()}.\nProfit/Loss: ${profit_loss:.2f}.")
            sell_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    sell_window = tk.Toplevel(root)
    sell_window.title("Sell Crypto")
    sell_window.geometry("300x200")
    sell_window.configure(bg="#fff7ee")

    tk.Label(sell_window, text="Coin Name:", font=("Courier New", 12), bg="#fff7ee").pack(pady=5)
    coin_name_entry = tk.Entry(sell_window, font=("Courier New", 12))
    coin_name_entry.pack(pady=5)

    tk.Label(sell_window, text="Units:", font=("Courier New", 12), bg="#fff7ee").pack(pady=5)
    units_entry = tk.Entry(sell_window, font=("Courier New", 12))
    units_entry.pack(pady=5)

    tk.Button(sell_window, text="Sell", font=("Courier New", 12), command=on_sell, bg="#FF5733", fg="white").pack(pady=15)

def view_portfolio_gui():
    portfolio = fetch_portfolio()
    
    portfolio_window = tk.Toplevel(root)
    portfolio_window.title("Portfolio")
    portfolio_window.geometry("900x500")
    portfolio_window.configure(bg="#fff7ee")
    
    # Add Profit/Loss column to the Treeview
    columns = ("Coin", "Units", "Purchase Price", "Current Price", "Total Value", "Transaction", "Date", "Profit/Loss")
    tree = ttk.Treeview(portfolio_window, columns=columns, show="headings", height=15)

    # Configure the headings and column widths
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, anchor="center", width=100)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Populate the Treeview with data
    for entry in portfolio:
        tree.insert("", "end", values=entry[1:9])  # Skip the ID column and include Profit/Loss
    
    portfolio_window.mainloop()


def clear_portfolio_gui():
    if messagebox.askyesno("Confirm", "Are you sure you want to clear the portfolio?"):
        clear_portfolio()
        messagebox.showinfo("Success", "Portfolio cleared!")

def main_gui():
    global root
    top_100_coins = fetch_top_100_coins()
    if not top_100_coins:
        messagebox.showerror("Error", "Unable to fetch top 100 coins.")
        return

    root = tk.Tk()
    root.title("Crypto Portfolio Manager")
    root.geometry("500x400")
    root.configure(bg="#fff7ee")

    tk.Label(root, text="Crypto Portfolio Manager", font=("Courier New", 16), bg="#fff7ee").pack(pady=20)

    tk.Button(root, text="Buy Crypto", font=("Courier New", 12), command=lambda: buy_crypto_gui(top_100_coins), bg="#c8ff49", fg="black").pack(pady=10)
    tk.Button(root, text="Sell Crypto", font=("Courier New", 12), command=lambda: sell_crypto_gui(top_100_coins), bg="#c8ff49", fg="black").pack(pady=10)
    tk.Button(root, text="View Portfolio", font=("Courier New", 12), command=view_portfolio_gui, bg="#c8ff49", fg="black").pack(pady=10)
    tk.Button(root, text="Clear Portfolio", font=("Courier New", 12), command=clear_portfolio_gui, bg="#FF0000", fg="white").pack(pady=10)
    tk.Button(root, text="Exit", font=("Courier New", 12), command=root.quit, bg="#333333", fg="white").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
