import tkinter as tk
from tkinter import messagebox
import random

class MarketGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Black Market & Regular Market Trading Game")
        self.root.geometry("800x600")
        self.root.config(bg="#282828")  # Dark background color

        self.base_currency = 1000  # Initial currency
        self.normal_market_stock = 0  # Regular market stock
        self.black_market_stock = 0  # Black market stock
        self.normal_market_price = 10  # Initial price for regular market
        self.black_market_price = 15  # Initial price for black market
        self.loss_limit = 500  # Loss limit
        self.arrest_probability = 0.2  # Probability of being arrested in the black market

        self.create_intro_screen()  # Create the introduction screen

    def create_intro_screen(self):
        intro_frame = tk.Frame(self.root, bg="#282828")
        intro_frame.pack(pady=50)

        intro_label = tk.Label(intro_frame, text="Welcome to the Black Market & Regular Market Trading Game!", 
                               font=("Arial", 18, "bold"), bg="#282828", fg="#FFD700")
        intro_label.pack(pady=20)

        rules_label = tk.Label(intro_frame, text="""
        Game Rules:
        1. You are a merchant operating in both the regular market and the black market.
        2. Each round, you can decide the supply quantity and price for both markets.
        3. The demand in both markets is random.
        4. There is a risk of being arrested when operating in the black market.
        5. If you exceed the loss limit of 500 currency units or get arrested, the game ends.
        6. Good luck!
        """, font=("Arial", 12), bg="#282828", fg="#FFFFFF", justify="left")
        rules_label.pack(pady=20)

        start_button = tk.Button(intro_frame, text="Start Game", font=("Arial", 14), command=self.start_game, 
                                 bg="#FFA500", fg="white")
        start_button.pack(pady=20)

    def start_game(self):
        self.create_game_screen()

    def create_game_screen(self):
        # Clear the introduction screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create the game screen
        self.game_frame = tk.Frame(self.root, bg="#282828")
        self.game_frame.pack(pady=20)

        self.currency_label = tk.Label(self.game_frame, text=f"Currency: {self.base_currency}", 
                                       font=("Arial", 14), bg="#282828", fg="#FFD700")
        self.currency_label.pack(pady=10)

        # Regular market section
        self.normal_frame = tk.Frame(self.game_frame, bg="#006400")
        self.normal_frame.pack(pady=10, padx=20, ipady=10)

        tk.Label(self.normal_frame, text="Regular Market", font=("Arial", 14, "bold"), bg="#006400", fg="#FFFFFF").grid(row=0, column=0, columnspan=2)
        tk.Label(self.normal_frame, text="Stock:", font=("Arial", 12), bg="#006400", fg="#FFFFFF").grid(row=1, column=0)
        self.normal_stock_label = tk.Label(self.normal_frame, text=str(self.normal_market_stock), font=("Arial", 12), bg="#006400", fg="#FFFFFF")
        self.normal_stock_label.grid(row=1, column=1)
        tk.Label(self.normal_frame, text="Price:", font=("Arial", 12), bg="#006400", fg="#FFFFFF").grid(row=2, column=0)
        self.normal_price_entry = tk.Entry(self.normal_frame, width=10, font=("Arial", 12), bg="#008000", fg="#FFFFFF")
        self.normal_price_entry.insert(0, str(self.normal_market_price))
        self.normal_price_entry.grid(row=2, column=1)
        tk.Label(self.normal_frame, text="Supply Quantity:", font=("Arial", 12), bg="#006400", fg="#FFFFFF").grid(row=3, column=0)
        self.normal_supply_entry = tk.Entry(self.normal_frame, width=10, font=("Arial", 12), bg="#008000", fg="#FFFFFF")
        self.normal_supply_entry.grid(row=3, column=1)
        tk.Button(self.normal_frame, text="Supply", command=self.supply_normal_market, font=("Arial", 12), 
                  bg="#00FF00", fg="white").grid(row=4, column=0, columnspan=2)

        # Black market section
        self.black_frame = tk.Frame(self.game_frame, bg="#8B0000")
        self.black_frame.pack(pady=10, padx=20, ipady=10)

        tk.Label(self.black_frame, text="Black Market", font=("Arial", 14, "bold"), bg="#8B0000", fg="#FFFFFF").grid(row=0, column=0, columnspan=2)
        tk.Label(self.black_frame, text="Stock:", font=("Arial", 12), bg="#8B0000", fg="#FFFFFF").grid(row=1, column=0)
        self.black_stock_label = tk.Label(self.black_frame, text=str(self.black_market_stock), font=("Arial", 12), bg="#8B0000", fg="#FFFFFF")
        self.black_stock_label.grid(row=1, column=1)
        tk.Label(self.black_frame, text="Price:", font=("Arial", 12), bg="#8B0000", fg="#FFFFFF").grid(row=2, column=0)
        self.black_price_entry = tk.Entry(self.black_frame, width=10, font=("Arial", 12), bg="#FF0000", fg="#FFFFFF")
        self.black_price_entry.insert(0, str(self.black_market_price))
        self.black_price_entry.grid(row=2, column=1)
        tk.Label(self.black_frame, text="Supply Quantity:", font=("Arial", 12), bg="#8B0000", fg="#FFFFFF").grid(row=3, column=0)
        self.black_supply_entry = tk.Entry(self.black_frame, width=10, font=("Arial", 12), bg="#FF0000", fg="#FFFFFF")
        self.black_supply_entry.grid(row=3, column=1)
        tk.Button(self.black_frame, text="Supply", command=self.supply_black_market, font=("Arial", 12), 
                  bg="#FF4500", fg="white").grid(row=4, column=0, columnspan=2)

        # Trade button
        self.trade_button = tk.Button(self.game_frame, text="Make Trade", command=self.trade, font=("Arial", 14), 
                                      bg="#FFA500", fg="white")
        self.trade_button.pack(pady=20)

        # Market status display
        self.market_status_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#282828", fg="#FFFFFF", wraplength=700)
        self.market_status_label.pack(pady=20)

    def supply_normal_market(self):
        try:
            supply = int(self.normal_supply_entry.get())
            price = float(self.normal_price_entry.get())
            if supply <= 0 or price <= 0:
                raise ValueError("Supply quantity and price must be greater than 0")
            cost = supply * price
            if cost > self.base_currency:
                raise ValueError("Insufficient currency")
            self.base_currency -= cost
            self.normal_market_stock += supply
            self.normal_market_price = price
            self.update_labels()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def supply_black_market(self):
        try:
            supply = int(self.black_supply_entry.get())
            price = float(self.black_price_entry.get())
            if supply <= 0 or price <= 0:
                raise ValueError("Supply quantity and price must be greater than 0")
            cost = supply * price
            if cost > self.base_currency:
                raise ValueError("Insufficient currency")
            self.base_currency -= cost
            self.black_market_stock += supply
            self.black_market_price = price
            self.update_labels()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def trade(self):
        # Simulate regular market trade
        self.normal_demand = random.randint(0, self.normal_market_stock)
        self.normal_revenue = self.normal_demand * self.normal_market_price
        self.normal_market_stock -= self.normal_demand
        self.base_currency += self.normal_revenue

        # Simulate black market trade
        self.black_demand = random.randint(0, self.black_market_stock)
        self.black_revenue = self.black_demand * self.black_market_price
        self.black_market_stock -= self.black_demand
        self.base_currency += self.black_revenue

        # Check if arrested in the black market (only if black market trade occurred)
        if self.black_demand > 0 and random.random() < self.arrest_probability:
            messagebox.showerror("Game Over", "You have been arrested in the black market! Game Over.")
            self.root.destroy()
            return

        # Check if loss exceeds limit
        if self.base_currency < -self.loss_limit:
            messagebox.showerror("Game Over", "Loss exceeds limit! Game Over.")
            self.root.destroy()
            return

        self.update_labels()
        self.update_market_status()

    def update_labels(self):
        self.currency_label.config(text=f"Currency: {self.base_currency}")
        self.normal_stock_label.config(text=str(self.normal_market_stock))
        self.black_stock_label.config(text=str(self.black_market_stock))

    def update_market_status(self):
        status_text = f"""
        Market Status:
        - Regular Market:
          - Demand: {self.normal_demand}
          - Remaining Stock: {self.normal_market_stock}
          - Revenue: {self.normal_revenue}
        - Black Market:
          - Demand: {self.black_demand}
          - Remaining Stock: {self.black_market_stock}
          - Revenue: {self.black_revenue}
        """
        self.market_status_label.config(text=status_text)

if __name__ == "__main__":
    root = tk.Tk()
    game = MarketGame(root)
    root.mainloop()