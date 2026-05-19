import streamlit as st
import data as d
import charts as c

st.set_page_config(page_title="Análise de Ações 2025", layout="wide")
st.title("Análise de Ações 2025 — ITUB4 | PETR4 | VALE3")
st.caption("Dados: Yahoo Finance  •  Período: 01/01/2025 – 31/12/2025")


@st.cache_data(show_spinner="Buscando dados de mercado...")
def load_data():
    prices = d.get_prices()
    returns = d.get_returns(prices)
    summary = d.get_dividends_summary()
    detail = d.get_dividends_detail()
    return prices, returns, summary, detail


prices, returns, div_summary, div_detail = load_data()

aba1, aba2, aba3 = st.tabs(["Cotação Diária", "Rentabilidade", "Dividendos"])

with aba1:
    st.plotly_chart(c.chart_prices(prices), width="stretch")

    st.subheader("Resumo do período")
    rows = []
    for col in prices.columns:
        s = prices[col].dropna()
        rows.append({
            "Ação": col,
            "Abertura (R$)": f"{s.iloc[0]:.2f}",
            "Fechamento (R$)": f"{s.iloc[-1]:.2f}",
            "Máximo (R$)": f"{s.max():.2f}",
            "Mínimo (R$)": f"{s.min():.2f}",
        })
    import pandas as pd
    st.dataframe(pd.DataFrame(rows).set_index("Ação"), width="stretch")

with aba2:
    st.plotly_chart(c.chart_returns(returns), width="stretch")

    st.subheader("Rentabilidade total no ano")
    cols = st.columns(len(returns.columns))
    for i, col in enumerate(returns.columns):
        final = returns[col].dropna().iloc[-1]
        sinal = "+" if final >= 0 else ""
        cols[i].metric(label=col, value=f"{sinal}{final:.2f}%")

with aba3:
    if div_summary["Total Dividendos (R$)"].sum() == 0:
        st.warning("Nenhum dividendo encontrado para o período 2025.")
    else:
        st.plotly_chart(c.chart_dividends(div_summary), width="stretch")

        st.subheader("Dividend Yield 2025")
        dy_cols = st.columns(len(prices.columns))
        for i, col in enumerate(prices.columns):
            first_price = prices[col].dropna().iloc[0]
            total_divs = div_summary.loc[div_summary["Ação"] == col, "Total Dividendos (R$)"].values[0]
            dy = (total_divs / first_price) * 100
            dy_cols[i].metric(label=col, value=f"{dy:.2f}%", help=f"R$ {total_divs:.4f} / R$ {first_price:.2f}")

        st.subheader("Resumo de dividendos")
        st.dataframe(div_summary.set_index("Ação"), width="stretch")

        st.subheader("Pagamentos detalhados")
        st.dataframe(div_detail.set_index("Ação"), width="stretch")
