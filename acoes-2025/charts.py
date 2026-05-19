import plotly.graph_objects as go
import pandas as pd

COLORS = {"ITUB4": "#FF6B35", "PETR4": "#004E89", "VALE3": "#1A936F"}


def chart_prices(prices: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for col in prices.columns:
        fig.add_trace(go.Scatter(
            x=prices.index, y=prices[col],
            name=col, line=dict(color=COLORS.get(col), width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>R$ %{y:.2f}<extra>" + col + "</extra>",
        ))
    fig.update_layout(
        title="Cotação Diária 2025 (Preço de Fechamento)",
        xaxis_title="Data", yaxis_title="Preço (R$)",
        hovermode="x unified", legend_title="Ação",
        template="plotly_white",
    )
    return fig


def chart_returns(returns: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for col in returns.columns:
        fig.add_trace(go.Scatter(
            x=returns.index, y=returns[col],
            name=col, line=dict(color=COLORS.get(col), width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>%{y:.2f}%<extra>" + col + "</extra>",
        ))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.update_layout(
        title="Rentabilidade Acumulada 2025 (%)",
        xaxis_title="Data", yaxis_title="Rentabilidade (%)",
        hovermode="x unified", legend_title="Ação",
        template="plotly_white",
    )
    return fig


def chart_dividends(summary: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=summary["Ação"],
        y=summary["Total Dividendos (R$)"],
        marker_color=[COLORS.get(a, "#888") for a in summary["Ação"]],
        text=summary["Total Dividendos (R$)"].apply(lambda v: f"R$ {v:.4f}"),
        textposition="outside",
        hovertemplate="%{x}<br>R$ %{y:.4f}<extra></extra>",
    ))
    fig.update_layout(
        title="Total de Dividendos Pagos em 2025 (por ação)",
        xaxis_title="Ação", yaxis_title="R$ por ação",
        template="plotly_white",
    )
    return fig
