from data_loader import load_price_history, load_latest_prices
import pandas as pd


def test_load_price_history_returns_dataframe():
    df = load_price_history()
    assert isinstance(df, pd.DataFrame)


def test_load_latest_prices_returns_dataframe():
    df = load_latest_prices()
    assert isinstance(df, pd.DataFrame)


def test_load_price_history_columns():
    df = load_price_history()
    required = {"product_id", "product_name", "price", "date"}
    assert required.issubset(df.columns)


def test_load_latest_prices_columns():
    df = load_latest_prices()
    required = {"name", "url", "price", "last_update"}
    assert required.issubset(df.columns)
