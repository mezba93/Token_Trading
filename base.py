import json
from datetime import datetime


class TokenSystem:
    def __init__(self):
        self.data_file = "token_data.json"
        self.default_halls = ["Zia Hall", "Hamid Hall", "Shahidul Hall", "Bongobandhu Hall", "Selim Hall"]
        self.load_data()

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

    def login(self, username, roll, mobile):
        for user, info in self.users.items():
            if info["roll"] == roll:
                print(f"A user with roll number {roll} already exists as '{user}'. Please log in.")
                return

        if username in self.users:
            print(f"Welcome back, {username}!")
        else:
            self.users[username] = {"roll": roll, "mobile": mobile}
            print(f"User '{username}' registered successfully.")
            self.save_data()

    def sell_tokens(self, username, hall, token_count, meal_type):
        if username not in self.users:
            print(f"User '{username}' does not exist. Please log in first.")
            return

        if hall not in self.halls:
            print(f"Hall '{hall}' does not exist.")
            return

        try:
            token_count = int(token_count)
            if token_count <= 0:
                print("Token count must be a positive number.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        while True:
            user_time = input("Enter timestamp (DD/MM/YY hh:mm AM/PM): ").strip()
            try:
                now = datetime.strptime(user_time, "%d/%m/%y %I:%M %p")  

                if meal_type.lower() == "lunch" and now.hour >= 14:
                    print("You cannot add lunch tokens after 2 PM.")
                    return
                elif meal_type.lower() == "dinner" and (now.hour > 22 or (now.hour == 22 and now.minute > 15)):
                    print("You cannot add dinner tokens after 10:15 PM.")
                    return

                break
            except ValueError:
                print("Invalid format! Please enter in DD/MM/YY hh:mm AM/PM format.")

        timestamp = now.strftime("%d/%m/%y %I:%M %p")

        seller_info = {
            "username": username,
            "roll": self.users[username]["roll"],
            "mobile": self.users[username]["mobile"],
            "tokens": token_count,
            "meal_type": meal_type,
            "timestamp": timestamp
        }
        self.halls[hall].append(seller_info)
        print(f"{token_count} {meal_type} tokens added to {hall} by {username} at {timestamp}.")
        self.save_data()

    def display_hall_tokens(self):
        now = datetime.now()
        today_str = now.strftime("%d/%m/%y")

        print("\n--- Available Tokens in Halls ---")
        for hall, sellers in self.halls.items():
            print(f"\n {hall}:")
            valid_sellers = []

            for seller in sellers:
                try:
                    token_time = datetime.strptime(seller["timestamp"], "%d/%m/%y %I:%M %p")  
                except ValueError:
                    continue

                token_date_str = token_time.strftime("%d/%m/%y")

                if token_date_str != today_str:
                    continue

                expiry_time = token_time.replace(hour=14, minute=0) if seller["meal_type"].lower() == "lunch" \
                    else token_time.replace(hour=22, minute=30)

                if now < expiry_time:
                    valid_sellers.append(seller)

            self.halls[hall] = valid_sellers

            if not valid_sellers:
                print("   No valid tokens available.")
            else:
                print("  ---------------------------------")
                for i, seller in enumerate(valid_sellers, start=1):
                    print(
                        f"  {i}. {seller['tokens']} {seller['meal_type']} tokens - Seller: {seller['username']} at {seller['timestamp']}")
                print("  ---------------------------------")

        self.save_data()

    def buy_tokens(self, buyer_username, hall, seller_index):
        if buyer_username not in self.users:
            print(f"User '{buyer_username}' does not exist. Please log in first.")
            return

        if hall not in self.halls or not self.halls[hall]:
            print(f"No available tokens in {hall}.")
            return

        if not (1 <= seller_index <= len(self.halls[hall])):
            print(f"Invalid seller selection for {hall}.")
            return

        seller_info = self.halls[hall].pop(seller_index - 1)
        print(f"Contact {seller_info['username']} for tokens:")
        print(f"  Roll: {seller_info['roll']}")
        print(f"  Mobile: {seller_info['mobile']}")
        self.save_data()

    def reset_users(self):
        self.users = {}
        self.save_data()
        print("All users have been erased.")


def main():
    system = TokenSystem()

    while True:
        print("\n--- Token System Menu ---")
        print("1. Login")
        print("2. Sell Tokens")
        print("3. Display Available Tokens")
        print("4. Buy Tokens")
        print("5. Reset Users")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            username = input("Enter username: ").strip()
            roll = input("Enter roll number: ").strip()
            mobile = input("Enter mobile number: ").strip()
            system.login(username, roll, mobile)
        elif choice == '2':
            username = input("Enter username: ").strip()
            hall = input(
                "Enter hall name (Zia Hall, Hamid Hall, Shahidul Hall, Bongobandhu Hall, Selim Hall): ").strip()
            token_count = input("Enter number of tokens to sell: ").strip()
            meal_type = input("Enter meal type (Lunch/Dinner): ").strip()
            system.sell_tokens(username, hall, token_count, meal_type)
        elif choice == '3':
            system.display_hall_tokens()
        elif choice == '4':
            buyer_username = input("Enter your username: ").strip()
            hall = input("Enter hall name: ").strip()
            system.display_hall_tokens()
            try:
                seller_index = int(input(f"Enter the seller index for {hall}: "))
                system.buy_tokens(buyer_username, hall, seller_index)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif choice == '5':
            system.reset_users()
        elif choice == '6':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
