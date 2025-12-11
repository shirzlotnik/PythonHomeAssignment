import pandas as pd

from models.chargeback import Chargeback
from models.order import Order
from models.transaction import Transaction
from pandantic import Pandantic

from utils.files_handler import get_transactions_orders_chargebacks


def validate_transactions_total_amount_by_order_id(validated_transactions_df, validated_orders_df):
    transactions_total_amount_by_order_id = (
        validated_transactions_df.groupby("order_id", as_index=False)["total_amount"].sum()).rename(
        columns={"amount": "transactions_total_amount"})
    match_orders_transactions_total = validated_orders_df.merge(transactions_total_amount_by_order_id, on="order_id",
                                                                how="left")
    match_orders_transactions_total["amount_match"] = match_orders_transactions_total["total_amount"] == \
                                                      match_orders_transactions_total["transactions_total"]
    if not match_orders_transactions_total["amount_match"].all():
        raise ValueError("There is at least one mismatched order amount to transactions amount")

    return True


def validate(transactions: pd.DataFrame, orders: pd.DataFrame,
             chargebacks: pd.DataFrame):
    transaction_validator = Pandantic(Transaction)
    order_validator = Pandantic(Order)
    chargeback_validator = Pandantic(Chargeback)

    validated_transactions_df: pd.DataFrame = transaction_validator.validate(transactions)
    validated_orders_df: pd.DataFrame = order_validator.validate(orders)
    validated_chargebacks_df: pd.DataFrame = chargeback_validator.validate(chargebacks)

    valid_orders_transactions_amounts = validate_transactions_total_amount_by_order_id(
        validated_transactions_df, validated_orders_df)

    return valid_orders_transactions_amounts and validated_chargebacks_df

def transform():
    return

def analysis():
    return

def design():
    return

def run_pipeline():
    transactions, orders, chargebacks = get_transactions_orders_chargebacks()
    valid = validate(transactions, orders, chargebacks)

    return

if __name__ == '__main__':
    print('Init')
