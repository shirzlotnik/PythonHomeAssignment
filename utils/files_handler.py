import json

import pandas as pd
import json

def get_transactions_orders_chargebacks():
    with open('data/transactions.json', 'r') as file:
        transactions = json.load(file)

        return transactions, transactions, transactions

    # transactions = pd.read_json('data/transactions.json')
    # orders = pd.read_json('orders.json')
    # chargebacks = pd.read_csv('chargebacks.csv')
    #
    # return transactions, orders, chargebacks

    # return transactions, transactions, transactions
