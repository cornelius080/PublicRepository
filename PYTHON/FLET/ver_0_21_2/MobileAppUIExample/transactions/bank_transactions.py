from faker import Faker
import random
Faker.seed(0)
fake = Faker()

class BankTransactions:
    def __init__(self, length=10):
        unsorted = [self.generate_transaction() for _ in range(length)]
        self.transactions = sorted(unsorted, key=lambda x: x['date'], reverse=True)
    
    def generate_transaction(self):        

        transaction_types = ["deposit", "withdrawal", "transfer", "payment"]
        transaction_type = random.choice(transaction_types)
        amount = round(random.uniform(10, 5000), 2)
        
        date = fake.date_time_between(start_date="-3M", end_date="now")
        
        return {
            "transaction_id": fake.aba(),
            #"date": date.isoformat(),
            "date": date.strftime('%Y-%b-%d %H:%M:%S'),
            "type": transaction_type,
            "amount": amount,
            "currency": fake.currency_code(),
            "company": fake.company() if transaction_type in ["payment", "transfer"] else "",
            "category": fake.word(ext_word_list=["food", "transport", "entertainment", "utilities", "shopping"]) if transaction_type in ["payment", "transfer"] else "",
            "description": fake.bs() if transaction_type in ["payment", "transfer"] else "",
        }