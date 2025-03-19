import json
import tkinter as tk
from tkinter import messagebox, PhotoImage, Scrollbar, Listbox
from datetime import datetime, time

class TokenSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Token Trading System")
        self.root.geometry("800x800")
        self.data_file = "token_data.json"
        self.default_halls = ["Zia Hall", "Hamid Hall", "Shahidul Hall", "Bongobandhu Hall", "Selim Hall"]
        self.load_data()
        self.current_user = None 
        self.admin_username = "admin" 
        self.admin_roll = "000000"  
        self.admin_mobile = "01111111111" 
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_data(self):
        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)
                self.users = data.get("users", {})
                self.halls = {hall: data.get("halls", {}).get(hall, []) for hall in self.default_halls}
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.users = {}
            self.halls = {hall: [] for hall in self.default_halls}
        self.save_data()

    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump({"users": self.users, "halls": self.halls}, file, indent=4)

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to Token Trading System", fg="white", bg="black",
                 font=("Arial", 20, "bold"), padx=20, pady=10, borderwidth=5, relief=tk.RIDGE).pack(pady=10)

        try:
            self.photo = PhotoImage(file="RUET.png")
            img_label = tk.Label(self.root, image=self.photo)
            img_label.image = self.photo
            img_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading image: {e}")

        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Roll Number:").pack()
        self.roll_entry = tk.Entry(self.root)
        self.roll_entry.pack()

        tk.Label(self.root, text="Mobile Number:").pack()
        self.mobile_entry = tk.Entry(self.root)
        self.mobile_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get().strip()
        roll = self.roll_entry.get().strip()
        mobile = self.mobile_entry.get().strip()

        if not username or not roll or not mobile:
            messagebox.showerror("Error", "All fields are required!")
            return

        if roll in [info["roll"] for info in self.users.values()] and username not in self.users:
            messagebox.showerror("Error", "Roll number already registered with a different username!")
            return

        if username in self.users or any(info["roll"] == roll for info in self.users.values()):
            messagebox.showinfo("Login", f"Welcome back, {username}!")
        else:
            self.users[username] = {"roll": roll, "mobile": mobile}
            messagebox.showinfo("Success", f"User '{username}' registered successfully.")
            self.save_data()

        self.current_user = username
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Main Menu", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Button(self.root, text="Sell Tokens", command=self.create_sell_token_screen, bg="blue", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Display Available Tokens", command=self.display_tokens, bg="purple", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Buy Token", command=self.buy_token, bg="green", fg="white", font=("Arial", 12)).pack(pady=5)

        if (self.current_user == self.admin_username and
            self.users[self.current_user]["roll"] == self.admin_roll and
            self.users[self.current_user]["mobile"] == self.admin_mobile):
            self.remove_users_button = tk.Button(self.root, text="Remove Users", command=self.remove_users, bg="orange", fg="white", font=("Arial", 12))
        else:
            self.remove_users_button = tk.Button(self.root, text="Remove Users", state=tk.DISABLED, bg="orange", fg="white", font=("Arial", 12))
        self.remove_users_button.pack(pady=5)

        tk.Button(self.root, text="Exit", command=self.root.quit, bg="red", fg="white", font=("Arial", 12)).pack(pady=5)

    def create_sell_token_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Sell Tokens", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.root, text="Select Hall:").pack()
        self.hall_var = tk.StringVar(self.root)
        self.hall_var.set(self.default_halls[0])
        self.hall_menu = tk.OptionMenu(self.root, self.hall_var, *self.default_halls)
        self.hall_menu.pack()

        tk.Label(self.root, text="Meal Type:").pack()
        self.meal_type_var = tk.StringVar(self.root)
        self.meal_type_var.set("Lunch")
        self.meal_type_menu = tk.OptionMenu(self.root, self.meal_type_var, "Lunch", "Dinner")
        self.meal_type_menu.pack()

        tk.Label(self.root, text="Number of Tokens:").pack()
        self.token_entry = tk.Entry(self.root)
        self.token_entry.pack()

        tk.Button(self.root, text="Sell", command=self.sell_token, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, bg="red", fg="white", font=("Arial", 12)).pack(pady=5)

    def sell_token(self):
        hall = self.hall_var.get()
        meal_type = self.meal_type_var.get()
        tokens = self.token_entry.get().strip()

        if not tokens.isdigit():
            messagebox.showerror("Error", "Invalid token number!")
            return

        tokens = int(tokens)
        current_time = datetime.now().time()

        if (meal_type == "Lunch" and current_time > time(14, 0)) or (meal_type == "Dinner" and current_time > time(22, 0)):
            messagebox.showerror("Error", f"Cannot sell {meal_type} tokens after { '2 PM' if meal_type == 'Lunch' else '10 PM' }.")
            return

        self.halls[hall].append({
            "username": self.current_user,
            "meal_type": meal_type,
            "tokens": tokens,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_data()
        messagebox.showinfo("Success", f"Successfully sold {tokens} tokens for {meal_type} at {hall}.")
        self.create_main_menu()

    def display_tokens(self):
        self.clear_screen()
        tk.Label(self.root, text="Available Tokens", font=("Arial", 16, "bold")).pack(pady=10)

        self.remove_expired_tokens()

        for hall, tokens in self.halls.items():
            tk.Label(self.root, text=hall, font=("Arial", 14, "bold")).pack()
            for token in tokens:
                tk.Label(self.root, text=f"Seller: {token['username']} | Meal: {token['meal_type']} | Tokens: {token['tokens']} | Time: {token['timestamp']}").pack()
        tk.Button(self.root, text="Back", command=self.create_main_menu, bg="red", fg="white", font=("Arial", 12)).pack(pady=5)

    def remove_expired_tokens(self):
        current_time = datetime.now().time()
        for hall in self.halls:
            self.halls[hall] = [
                token for token in self.halls[hall]
                if not (
                    (token['meal_type'] == "Lunch" and current_time > time(14, 10)) or
                    (token['meal_type'] == "Dinner" and current_time > time(22, 10))
                )
            ]
        self.save_data()

    def buy_token(self):
        self.clear_screen()
        tk.Label(self.root, text="Buy Tokens", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.root, text="Select Hall:").pack()
        self.buy_hall_var = tk.StringVar(self.root)
        self.buy_hall_var.set(self.default_halls[0])
        self.buy_hall_menu = tk.OptionMenu(self.root, self.buy_hall_var, *self.default_halls)
        self.buy_hall_menu.pack()

        tk.Label(self.root, text="Meal Type:").pack()
        self.buy_meal_type_var = tk.StringVar(self.root)
        self.buy_meal_type_var.set("Lunch")
        self.buy_meal_type_menu = tk.OptionMenu(self.root, self.buy_meal_type_var, "Lunch", "Dinner")
        self.buy_meal_type_menu.pack()

        tk.Label(self.root, text="Number of Tokens to Buy:").pack()
        self.buy_token_entry = tk.Entry(self.root)
        self.buy_token_entry.pack()

        tk.Button(self.root, text="Buy", command=self.process_buy_token, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, bg="red", fg="white", font=("Arial", 12)).pack(pady=5)

    def process_buy_token(self):
        hall = self.buy_hall_var.get()
        meal_type = self.buy_meal_type_var.get()
        tokens_to_buy = self.buy_token_entry.get().strip()

        if not tokens_to_buy.isdigit():
            messagebox.showerror("Error", "Invalid token number!")
            return

        tokens_to_buy = int(tokens_to_buy)
        available_tokens = [token for token in self.halls[hall] if token['meal_type'] == meal_type]

        if not available_tokens:
            messagebox.showerror("Error", f"No tokens available for {meal_type} at {hall}.")
            return

        total_available = sum(token['tokens'] for token in available_tokens)
        if tokens_to_buy > total_available:
            messagebox.showerror("Error", f"Not enough tokens available. Only {total_available} tokens are available.")
            return

        sellers_info = []
        for token in available_tokens:
            if tokens_to_buy <= 0:
                break
            if token['tokens'] >= tokens_to_buy:
                sellers_info.append({
                    "username": token['username'],
                    "mobile": self.users[token['username']]['mobile'],
                    "tokens_sold": tokens_to_buy
                })
                token['tokens'] -= tokens_to_buy
                tokens_to_buy = 0
            else:
                sellers_info.append({
                    "username": token['username'],
                    "mobile": self.users[token['username']]['mobile'],
                    "tokens_sold": token['tokens']
                })
                tokens_to_buy -= token['tokens']
                token['tokens'] = 0


        self.halls[hall] = [token for token in self.halls[hall] if token['tokens'] > 0]

        self.save_data()

        seller_info_message = "Tokens purchased successfully! Contact the seller(s) for further details:\n\n"
        for seller in sellers_info:
            seller_info_message += (
                f"Seller Name: {seller['username']}\n"
                f"Mobile Number: {seller['mobile']}\n"
                f"Tokens Sold: {seller['tokens_sold']}\n\n"
            )
        seller_info_message += "Please contact the seller(s) to complete the transaction."

        messagebox.showinfo("Success", seller_info_message)
        self.create_main_menu()

    def remove_users(self):
        self.clear_screen()
        tk.Label(self.root, text="Remove Users", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.root, text="Select User to Remove:").pack()
        self.user_listbox = Listbox(self.root)
        for user in self.users:
            self.user_listbox.insert(tk.END, user)
        self.user_listbox.pack()

        tk.Button(self.root, text="Remove Selected User", command=self.process_remove_user, bg="red", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, bg="red", fg="white", font=("Arial", 12)).pack(pady=5)

    def process_remove_user(self):
        selected_user = self.user_listbox.get(tk.ACTIVE)
        if selected_user:
            del self.users[selected_user]
            for hall in self.halls:
                self.halls[hall] = [token for token in self.halls[hall] if token['username'] != selected_user]
            self.save_data()
            messagebox.showinfo("Success", f"User '{selected_user}' has been removed.")
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "No user selected!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TokenSystemGUI(root)
    root.mainloop()