import pandas as pd
# from models.chargeback import Chargeback
# from models.order import Order
from models.transaction import Transaction, PaymentMethod
from pandantic import Pandantic

from utils.files_handler import get_transactions_orders_chargebacks


CURRENCIES_EXCHANGE = {
        "currency": ["USD", "EUR", "GBP", "ILS"],
        "rate_to_usd": [1.0, 1.08, 1.25, 3.8]
    }


def validate_transactions_total_amount_by_order_id(validated_transactions_df, validated_orders_df):
    transactions_total_amount_by_order_id = (
        validated_transactions_df.groupby("order_id", as_index=False)["total_amount"].sum()).rename(
        columns={"amount": "transactions_total_amount"})
    match_orders_transactions_total = validated_orders_df.merge(transactions_total_amount_by_order_id, on="order_id",
                                                                how="left")
    match_orders_transactions_total["amount_match"] = match_orders_transactions_total["total_amount"] == \
                                                      transactions_total_amount_by_order_id["transactions_total"]

    return


def validate(transactions, orders,
             chargebacks):
    # transaction_validator = Pandantic(Transaction)
    # validated_transactions = [Transaction() for row in transactions.to_dict(orient='records')]

    trs = []
    for tr in transactions:
        trs.append(Transaction(**tr))

    # order_validator = Pandantic(Order)
    # chargeback_validator = Pandantic(Chargeback)

    # validated_transactions_df: pd.DataFrame = transaction_validator.validate(transactions)
    # validated_orders_df: pd.DataFrame = order_validator.validate(orders)
    # validated_chargebacks_df: pd.DataFrame = chargeback_validator.validate(chargebacks)

    # validate_transactions_total_amount_by_order_id(validated_transactions_df, validated_orders_df)

    return


def get_normalize_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    transactions = transactions.rename(columns={
        "payment_method.type": "payment_method_type",
        "payment_method.provider": "payment_method_provider"
    })
    transactions["amount"] = transactions["amount"].astype(float)
    transactions["timestamp"] = pd.to_datetime(transactions["timestamp"])

    return transactions


def get_normalize_chargebacks(chargebacks: pd.DataFrame) -> pd.DataFrame:
    chargebacks["dispute_date"] = pd.to_datetime(chargebacks["dispute_date"])
    chargebacks["resolution_date"] = pd.to_datetime(chargebacks["resolution_date"])
    chargebacks["amount"] = chargebacks["amount"].astype(float)

    return chargebacks


def get_normalize_orders(orders: pd.DataFrame) -> pd.DataFrame:
    orders["timestamp"] = pd.to_datetime(orders["timestamp"])

    return orders


def transform(transactions: pd.DataFrame, orders: pd.DataFrame,
              chargebacks: pd.DataFrame):
    normalize_transactions = get_normalize_transactions(transactions)
    normalize_orders = get_normalize_orders(orders)
    normalize_chargebacks = get_normalize_chargebacks(chargebacks)

    success_rate = (normalize_transactions["status"] == "completed").mean()
    success_by_method = (
        normalize_transactions
        .groupby("payment_method_type")["status"]
        .apply(lambda s: (s == "completed").mean())
        .reset_index(name="success_rate")
    )

    currencies_exchange = pd.DataFrame(CURRENCIES_EXCHANGE)

    for currency in CURRENCIES_EXCHANGE["currency"]:
        normalize_transactions[f"amount_{currency.lower()}"] = normalize_transactions["amount"] * currencies_exchange["rate_to_usd"]
        normalize_orders[f"total_amount_{currency.lower()}"] = normalize_orders["total_amount"] * currencies_exchange["rate_to_usd"]

    return


def analysis():
    return


def design():
    return


def run_pipeline():
    transactions, orders, chargebacks = get_transactions_orders_chargebacks()
    validate(transactions, orders, chargebacks)

    return


if __name__ == '__main__':
    run_pipeline()
