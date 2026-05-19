import yfinance as yf
import pandas as pd

TICKERS = ["ITUB4.SA", "PETR4.SA", "VALE3.SA"]
START = "2025-01-01"
END = "2025-12-31"


def get_prices(tickers=TICKERS) -> pd.DataFrame:
    raw = yf.download(tickers, start=START, end=END, auto_adjust=True, progress=False)
    prices = raw["Close"].copy()
    prices.columns = [t.replace(".SA", "") for t in prices.columns]
    prices.index = pd.to_datetime(prices.index)
    return prices.dropna(how="all")


def get_returns(prices: pd.DataFrame) -> pd.DataFrame:
    first = prices.iloc[0]
    returns = (prices / first - 1) * 100
    return returns


def get_dividends(ticker: str) -> pd.Series:
    t = yf.Ticker(ticker)
    divs = t.dividends
    if divs.empty:
        return pd.Series(dtype=float)
    divs.index = divs.index.tz_localize(None)
    return divs[(divs.index >= START) & (divs.index <= END)]


def get_dividends_summary(tickers=TICKERS) -> pd.DataFrame:
    records = []
    for ticker in tickers:
        divs = get_dividends(ticker)
        label = ticker.replace(".SA", "")
        records.append({
            "Ação": label,
            "Total Dividendos (R$)": round(divs.sum(), 4),
            "Nº de Pagamentos": len(divs),
        })
    return pd.DataFrame(records)


def get_dividends_detail(tickers=TICKERS) -> pd.DataFrame:
    rows = []
    for ticker in tickers:
        divs = get_dividends(ticker)
        label = ticker.replace(".SA", "")
        for date, value in divs.items():
            rows.append({"Ação": label, "Data": date.date(), "Valor (R$)": round(value, 4)})
    if not rows:
        return pd.DataFrame(columns=["Ação", "Data", "Valor (R$)"])
    return pd.DataFrame(rows).sort_values("Data")
