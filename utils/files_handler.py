import json

import pandas as pd


def get_transactions_orders_chargebacks() -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    transactions = pd.read_json('data/transactions.json')
    # orders = pd.read_json('orders.json')
    # chargebacks = pd.read_csv('chargebacks.csv')
    #
    # return transactions, orders, chargebacks

    return transactions, transactions, transactions
