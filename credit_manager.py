import json

class CreditManager:
    def __init__(self, filename="credits.json"):
        self.filename = filename
        self.credit_data = {}
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                self.credit_data = json.load(file)
        except FileNotFoundError:
            # Fichier non trouvé, on initialise avec un dictionnaire vide
            self.credit_data = {}

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.credit_data, file, indent=4)

    def get_balance(self, user_id):
        return self.credit_data.get(user_id, 0)

    def set_balance(self, user_id, amount):
        self.credit_data[user_id] = amount
        self.save_data()

    def add_balance(self, user_id, amount):
        current_balance = self.get_balance(user_id)
        new_balance = current_balance + amount
        self.credit_data[user_id] = new_balance
        self.save_data()

    def remove_balance(self, user_id, amount):
        current_balance = self.get_balance(user_id)
        if current_balance >= amount:
            new_balance = current_balance - amount
            self.credit_data[user_id] = new_balance
            self.save_data()
            return True
        return False