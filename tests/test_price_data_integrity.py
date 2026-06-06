from data_loader import load_price_history
import datetime
import pandas as pd


def test_price_non_negative():
    df = load_price_history()
    assert (df["price"] >= 0).all()


def test_product_name_not_empty():
    df = load_price_history()
    assert df["product_name"].str.len().min() > 0


def test_timestamp_not_future():
    df = load_price_history()
    now = datetime.datetime.now()

    # 最新仕様では timestamp ではなく date カラム
    df["date"] = pd.to_datetime(df["date"])

    assert (df["date"] <= now).all()
