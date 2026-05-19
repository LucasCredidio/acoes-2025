# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
cd acoes-2025
pip install -r requirements.txt
streamlit run app.py
```

The app runs at `http://localhost:8501` by default.

## Project Overview

A Streamlit dashboard analyzing three Brazilian stocks (ITUB4, PETR4, VALE3) for the 2025 calendar year. Data is fetched live from Yahoo Finance on each run — there is no database or persistence layer.

## Architecture

Three-module structure with clear separation of concerns:

- **`data.py`** — All Yahoo Finance interaction (`yfinance`). Fetches prices, computes cumulative returns, and aggregates dividends. Hardcoded tickers (`ITUB4.SA`, `PETR4.SA`, `VALE3.SA`) and date range (2025-01-01 to 2025-12-31).
- **`charts.py`** — Plotly chart builders. Each function receives a DataFrame and returns a `go.Figure`. Defines the per-stock color palette (ITUB4: #FF6B35, PETR4: #004E89, VALE3: #1A936F).
- **`app.py`** — Streamlit entry point. Orchestrates the other two modules, implements the three-tab UI (Cotação Diária / Rentabilidade / Dividendos), and uses `@st.cache_data` to avoid redundant API calls.

Data flows one way: `data.py` → `app.py` → `charts.py` → rendered in `app.py`.

## Dependencies

`streamlit`, `yfinance`, `pandas`, `plotly` — all listed in `acoes-2025/requirements.txt`. No build step required.

## GitHub Repository

Repository: https://github.com/LucasCredidio/acoes-2025

Changes are synced automatically to GitHub after every Claude response via a Stop hook configured in `.claude/settings.local.json`. The hook runs:

```powershell
git add .
git diff --cached --quiet
# if there are staged changes:
git commit -m "auto: sync yyyy-MM-dd HH:mm"
git push
```

To manage the hook, open `/hooks` in Claude Code. GitHub CLI (`gh`) is installed at `C:\Program Files\GitHub CLI\gh.exe` and authenticated as `LucasCredidio`.
